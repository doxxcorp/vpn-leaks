"""Summarize PCAP to JSON metadata (Python + dpkt only; no tshark)."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import dpkt


def _parse_server_name_extension(ext: bytes, out: list[str]) -> None:
    if len(ext) < 2:
        return
    list_len = int.from_bytes(ext[:2], "big")
    p = 2
    end = min(len(ext), 2 + list_len)
    while p + 3 <= end:
        ntype = ext[p]
        nlen = int.from_bytes(ext[p + 1 : p + 3], "big")
        p += 3
        if p + nlen > len(ext):
            break
        if ntype == 0:
            hn = ext[p : p + nlen].decode("ascii", errors="replace").lower().strip(".")
            if hn:
                out.append(hn)
        p += nlen


def _snis_from_client_hello_body(ch: bytes) -> list[str]:
    snis: list[str] = []
    if len(ch) < 43:
        return snis
    sess_id_len = int(ch[34])
    o = 35 + sess_id_len
    if o + 2 > len(ch):
        return snis
    csuites_len = int.from_bytes(ch[o : o + 2], "big")
    o += 2 + csuites_len
    if o + 1 > len(ch):
        return snis
    comp_len = int(ch[o])
    o += 1 + comp_len
    if o + 2 > len(ch):
        return snis
    ext_len = int.from_bytes(ch[o : o + 2], "big")
    o += 2
    ext_end = min(o + ext_len, len(ch))
    eo = o
    while eo + 4 <= ext_end:
        etype = int.from_bytes(ch[eo : eo + 2], "big")
        elen = int.from_bytes(ch[eo + 2 : eo + 4], "big")
        eo += 4
        if eo + elen > ext_end:
            break
        edata = ch[eo : eo + elen]
        if etype == 0:
            _parse_server_name_extension(edata, snis)
        eo += elen
    return snis


def _snis_from_tls_records(blob: bytes) -> list[str]:
    """Parse TLS handshake records for ClientHello SNI extensions."""
    snis: list[str] = []
    i = 0
    n = len(blob)
    while i + 5 <= n:
        if blob[i] != 0x16:
            i += 1
            continue
        rec_len = int.from_bytes(blob[i + 3 : i + 5], "big")
        body_start = i + 5
        body_end = body_start + rec_len
        if body_end > n:
            i += 1
            continue
        body = blob[body_start:body_end]
        if len(body) < 4 or body[0] != 0x01:
            i = body_start
            continue
        hslen = int.from_bytes(body[1:4], "big")
        ch = body[4 : 4 + hslen]
        snis.extend(_snis_from_client_hello_body(ch))
        i = body_end
    return snis


def _dns_queries(dns_blob: bytes) -> list[str]:
    out: list[str] = []
    try:
        d = dpkt.dns.DNS(dns_blob)
    except Exception:
        return out
    for q in getattr(d, "qd", ()) or []:
        nm_raw = getattr(q, "name", None)
        if isinstance(nm_raw, str) and nm_raw.strip():
            out.append(nm_raw.lower().strip("."))
            continue
        labels = getattr(q, "labels", None)
        if labels:
            parts: list[str] = []
            for p in labels:
                if isinstance(p, bytes):
                    parts.append(p.decode("ascii", errors="replace"))
                else:
                    parts.append(str(p))
            joined = ".".join(parts).lower().strip(".")
            if joined:
                out.append(joined)
    return out


def _flow_key(protocol: str, sip: bytes, dip: bytes, sport: int, dport: int) -> tuple[str, ...]:
    return (
        protocol,
        sip.hex(),
        dip.hex(),
        str(sport),
        str(dport),
    )


def summarize_pcap_file(pcap_path: Path, *, max_flows_kept: int = 512) -> dict[str, Any]:
    errors: list[str] = []
    flows: Counter[tuple[str, ...]] = Counter()
    sni_all: Counter[str] = Counter()
    dns_names: Counter[str] = Counter()
    quic_hints = 0
    udp_443_packets = 0
    opaque_tls_hints = 0
    ip_pair_bytes: Counter[tuple[str, str]] = Counter()
    packet_counts = {"total": 0, "l3_seen": 0}

    path = Path(pcap_path)
    missing = not path.is_file()
    empty_out: dict[str, Any] = {
        "schema_version": "1.0",
        "source_pcap": str(path.resolve()),
        "packet_counts": packet_counts,
        "flows_unique_estimate": 0,
        "flows_sample": [],
        "tls_clienthello_snis_unique": [],
        "dns_hostnames_unique": [],
        "quic_udp_443_packets": 0,
        "quic_heuristic_notes": 0,
        "opaque_tls_hints": 0,
        "top_inet_pairs_sample": [],
        "limits": [],
        "errors": [],
    }
    if missing:
        empty_out["errors"] = ["pcap_not_found"]
        return empty_out

    try:
        fh = path.open("rb")
    except OSError as e:
        empty_out["errors"] = [str(e)[:400]]
        return empty_out

    with fh:
        try:
            rdr = dpkt.pcap.Reader(fh)
        except Exception as e:
            empty_out["errors"] = [f"pcap_reader_failed:{e}"[:400]]
            return empty_out

        for _, buf in rdr:
            packet_counts["total"] += 1
            ip: dpkt.ip.IP | dpkt.ip6.IP6 | None = None
            proto = ""

            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if isinstance(eth.data, dpkt.ip.IP):
                    ip = eth.data
                    proto = "ip4"
                elif isinstance(eth.data, dpkt.ip6.IP6):
                    ip = eth.data
                    proto = "ip6"
            except Exception:
                pass

            if ip is None:
                try:
                    ip_try = dpkt.ip.IP(buf)
                    ip = ip_try
                    proto = "ip4_raw"
                except Exception:
                    try:
                        ip_try = dpkt.ip6.IP6(buf)
                        ip = ip_try
                        proto = "ip6_raw"
                    except Exception:
                        continue

            packet_counts["l3_seen"] += 1

            def ip_txt(addr: bytes) -> str:
                if len(addr) == 4:
                    return ".".join(str(b) for b in addr)
                if len(addr) == 16:
                    return ":".join(f"{i:02x}" for i in addr)  # weak display
                return addr.hex()

            sip = ip.src
            dip = ip.dst
            sip_s = ip_txt(sip)
            dip_s = ip_txt(dip)

            try:
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    sp, dp = int(tcp.sport), int(tcp.dport)
                    pl = bytes(tcp.data) if tcp.data else b""
                    flows[_flow_key(proto, sip, dip, sp, dp)] += len(buf)
                    ip_pair_bytes[(sip_s, dip_s)] += len(buf)
                    snis = _snis_from_tls_records(pl)
                    if snis:
                        for s in snis:
                            sni_all[s] += 1
                    elif pl.startswith(b"\x16\x03"):
                        opaque_tls_hints += 1

                elif isinstance(ip.data, dpkt.udp.UDP):
                    udp = ip.data
                    sp, dp = int(udp.sport), int(udp.dport)
                    udata = bytes(udp.data) if udp.data else b""
                    flows[_flow_key(proto, sip, dip, sp, dp)] += len(buf)
                    ip_pair_bytes[(sip_s, dip_s)] += len(buf)
                    if sp == 53 or dp == 53:
                        for qn in _dns_queries(udata):
                            dns_names[qn] += 1
                    if sp == 443 or dp == 443:
                        udp_443_packets += 1
                        if len(udata) > 8 and (udata[0] & 0xC0) == 0xC0:
                            quic_hints += 1
                else:
                    flows[_flow_key(proto, sip, dip, 0, 0)] += len(buf)
                    ip_pair_bytes[(sip_s, dip_s)] += len(buf)
            except Exception as ex:
                errors.append(f"pkt:{packet_counts['total']}:{type(ex).__name__}")

    top_flow_items = flows.most_common(max_flows_kept)
    flows_sample = [{"key": list(k), "bytes": cnt} for k, cnt in top_flow_items]

    limits: list[str] = [
        "ECH_ESNI_not_visible",
        "DoH_not_inferred_from_udp_53",
        "tcp_segmentation_may_fragment_clienthello",
        "inner_vpn_payload_may_be_opaque",
    ]
    if len(flows) > max_flows_kept:
        limits.append(f"flows_sample_kept_top_{max_flows_kept}")

    return {
        "schema_version": "1.0",
        "source_pcap": str(path.resolve()),
        "packet_counts": packet_counts,
        "flows_unique_estimate": len(flows),
        "flows_sample": flows_sample,
        "tls_clienthello_snis_unique": sorted(sni_all.keys()),
        "opaque_tls_hints": opaque_tls_hints,
        "dns_hostnames_unique": sorted(dns_names.keys())[:4096],
        "quic_udp_443_packets": udp_443_packets,
        "quic_heuristic_notes": quic_hints,
        "top_inet_pairs_sample": [
            {"src": s, "dst": d, "bytes": c} for (s, d), c in ip_pair_bytes.most_common(32)
        ],
        "limits": limits,
        "errors": errors[:64],
        "ja3_ja4": [],
    }


def write_pcap_summary_json(pcap_path: Path, out_path: Path) -> dict[str, Any]:
    summary = summarize_pcap_file(pcap_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary
