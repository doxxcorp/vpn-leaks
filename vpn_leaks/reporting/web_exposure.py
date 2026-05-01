"""Rollup helpers for website-exposure methodology outputs (HAR + provider DNS + surface matrix)."""

from __future__ import annotations

import ipaddress
import re
import socket
import subprocess
from pathlib import Path
from typing import Any

_DIG_TIMEOUT_S = 6
_WHOIS_TIMEOUT_S = 8
_MAX_TXT_VALUES = 4
_MAX_RESOLVED_IPS = 12


def _is_public_ip(value: str) -> bool:
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return False
    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_multicast
        or ip.is_link_local
        or ip.is_unspecified
        or ip.is_reserved
    )


def _run_cmd(args: list[str], timeout_s: int) -> tuple[str, str | None]:
    try:
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except FileNotFoundError:
        return "", f"missing_command:{args[0]}"
    except subprocess.TimeoutExpired:
        return "", f"timeout:{args[0]}"
    if proc.returncode != 0 and not proc.stdout.strip():
        return "", f"{args[0]}_exit_{proc.returncode}"
    return proc.stdout.strip(), None


def _parse_asn(text: str) -> str:
    match = re.search(r"\bAS(\d{1,10})\b", text, flags=re.IGNORECASE)
    if match:
        return f"AS{match.group(1)}"
    for key in ("origin:", "originas:", "aut-num:"):
        for line in text.splitlines():
            if line.lower().startswith(key):
                match = re.search(r"(\d{1,10})", line)
                if match:
                    return f"AS{match.group(1)}"
    return "—"


def _parse_owner(text: str) -> str:
    keys = (
        "orgname:",
        "organization:",
        "org-name:",
        "owner:",
        "netname:",
        "descr:",
    )
    for line in text.splitlines():
        low = line.lower().strip()
        for key in keys:
            if low.startswith(key):
                return line.split(":", 1)[1].strip()[:200] or "—"
    return "—"


def _whois_summary(text: str) -> str:
    keys = (
        "orgname:",
        "organization:",
        "org-name:",
        "owner:",
        "netname:",
        "country:",
        "origin:",
        "originas:",
        "aut-num:",
    )
    picked: list[str] = []
    for line in text.splitlines():
        low = line.lower().strip()
        if any(low.startswith(k) for k in keys):
            picked.append(line.strip())
        if len(picked) >= 6:
            break
    if not picked:
        return "—"
    return " | ".join(picked)[:700]


def _dig_summary_for_host(host: str, *, is_ip: bool) -> tuple[str, dict[str, list[str]], list[str]]:
    out_parts: list[str] = []
    resolved: dict[str, list[str]] = {"a": [], "aaaa": [], "cname": [], "mx": [], "txt": [], "ptr": []}
    errs: list[str] = []

    if is_ip:
        ptr, err = _run_cmd(["dig", "+short", "-x", host], _DIG_TIMEOUT_S)
        if err:
            errs.append(f"dig_ptr:{err}")
        resolved["ptr"] = [x.strip(".") for x in ptr.splitlines() if x.strip()]
        out_parts.append(f"PTR={', '.join(resolved['ptr']) if resolved['ptr'] else '—'}")
        return "; ".join(out_parts), resolved, errs

    for rtype, key in (
        ("A", "a"),
        ("AAAA", "aaaa"),
        ("CNAME", "cname"),
        ("MX", "mx"),
        ("TXT", "txt"),
    ):
        raw, err = _run_cmd(["dig", "+short", host, rtype], _DIG_TIMEOUT_S)
        if err:
            errs.append(f"dig_{rtype.lower()}:{err}")
            continue
        vals = [v.strip().strip('"') for v in raw.splitlines() if v.strip()]
        if rtype == "TXT":
            vals = vals[:_MAX_TXT_VALUES]
        resolved[key] = vals
        shown = ", ".join(vals[:6]) if vals else "—"
        out_parts.append(f"{rtype}={shown}")
    return "; ".join(out_parts), resolved, errs


def _decode_flow_ip(proto: str, encoded: str) -> str | None:
    if not isinstance(encoded, str):
        return None
    raw = encoded.strip().lower()
    if proto.startswith("ip4") and len(raw) == 8:
        try:
            return str(ipaddress.IPv4Address(bytes.fromhex(raw)))
        except ValueError:
            return None
    if proto.startswith("ip6") and len(raw) == 32:
        try:
            return str(ipaddress.IPv6Address(bytes.fromhex(raw)))
        except ValueError:
            return None
    return None


def _pcap_candidate_hosts(pcap: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    rows: dict[str, dict[str, Any]] = {}
    host_sources: dict[str, set[str]] = {}

    def ensure_ip(ip: str) -> None:
        if ip not in rows:
            rows[ip] = {
                "host": ip,
                "source": "pcap_peer_ip",
                "ip": ip,
                "ips": [ip],
                "bytes_observed": 0,
                "flow_count": 0,
            }

    for flow in pcap.get("flows_sample") or []:
        if not isinstance(flow, dict):
            continue
        key = flow.get("key")
        if not isinstance(key, list) or len(key) < 3:
            continue
        proto = str(key[0] or "")
        sip = _decode_flow_ip(proto, str(key[1]))
        dip = _decode_flow_ip(proto, str(key[2]))
        b = int(flow.get("bytes") or 0)
        for ip in (sip, dip):
            if not ip or not _is_public_ip(ip):
                continue
            ensure_ip(ip)
            rows[ip]["bytes_observed"] += b
            rows[ip]["flow_count"] += 1

    for pair in pcap.get("top_inet_pairs_sample") or []:
        if not isinstance(pair, dict):
            continue
        b = int(pair.get("bytes") or 0)
        for ip in (pair.get("src"), pair.get("dst")):
            if not isinstance(ip, str) or not _is_public_ip(ip):
                continue
            ensure_ip(ip)
            rows[ip]["bytes_observed"] += b
            rows[ip]["flow_count"] += 1

    for source_key, source_name in (
        ("dns_hostnames_unique", "pcap_dns"),
        ("tls_clienthello_snis_unique", "pcap_sni"),
    ):
        for host in pcap.get(source_key) or []:
            if not isinstance(host, str):
                continue
            h = host.strip().lower().strip(".")
            if not h:
                continue
            if _is_public_ip(h):
                ensure_ip(h)
                continue
            if h not in host_sources:
                host_sources[h] = set()
            host_sources[h].add(source_name)
    return rows, host_sources


def pcap_host_intelligence(data: dict[str, Any]) -> dict[str, Any]:
    """Build per-location PCAP host intelligence rows with live dig/whois enrichment."""
    pcap = data.get("pcap_derived")
    if not isinstance(pcap, dict) or not pcap:
        return {"has_inventory": False, "rows": [], "errors": [], "notes": []}

    ip_rows, host_sources = _pcap_candidate_hosts(pcap)
    rows = list(ip_rows.values())
    errors: list[str] = []
    notes = [
        "Scope: public peer IPs from PCAP flows/pairs plus DNS/SNI hostnames from PCAP.",
        "Live lookups are fail-soft and may vary by resolver/time.",
    ]

    rdns_cache: dict[str, str] = {}
    whois_cache: dict[str, dict[str, str]] = {}
    dig_cache: dict[tuple[str, bool], tuple[str, dict[str, list[str]], list[str]]] = {}

    def reverse_dns(ip: str) -> tuple[str, str | None]:
        if ip in rdns_cache:
            return rdns_cache[ip], None
        try:
            ptr = socket.gethostbyaddr(ip)[0].strip(".").lower()
            rdns_cache[ip] = ptr
            return ptr, None
        except Exception:
            rdns_cache[ip] = "—"
            return "—", "reverse_dns_failed"

    def whois_for_ip(ip: str) -> tuple[dict[str, str], str | None]:
        if ip in whois_cache:
            return whois_cache[ip], None
        raw, err = _run_cmd(["whois", ip], _WHOIS_TIMEOUT_S)
        if err:
            whois_cache[ip] = {"asn": "—", "owner": "—", "whois_summary": "—"}
            return whois_cache[ip], f"whois:{err}"
        parsed = {
            "asn": _parse_asn(raw),
            "owner": _parse_owner(raw),
            "whois_summary": _whois_summary(raw),
        }
        whois_cache[ip] = parsed
        return parsed, None

    for row in rows:
        ip = str(row.get("ip") or "")
        if not ip:
            continue
        row_errors: list[str] = []

        rdns, rdns_err = reverse_dns(ip)
        row["reverse_dns"] = rdns
        if rdns_err:
            row_errors.append(rdns_err)

        dig_key = (ip, True)
        if dig_key not in dig_cache:
            dig_cache[dig_key] = _dig_summary_for_host(ip, is_ip=True)
        dig_summary, _resolved, dig_errs = dig_cache[dig_key]
        row["dig_summary"] = dig_summary or "—"
        row_errors.extend(dig_errs)

        whois, werr = whois_for_ip(ip)
        row["asn"] = whois["asn"]
        row["owner"] = whois["owner"]
        row["whois_summary"] = whois["whois_summary"]
        if werr:
            row_errors.append(werr)
        row["lookup_errors"] = row_errors

    for host in sorted(host_sources.keys()):
        srcs = sorted(host_sources[host])
        dig_key = (host, False)
        if dig_key not in dig_cache:
            dig_cache[dig_key] = _dig_summary_for_host(host, is_ip=False)
        dig_summary, resolved, dig_errs = dig_cache[dig_key]
        ips = [ip for ip in (resolved["a"] + resolved["aaaa"]) if _is_public_ip(ip)]
        if len(ips) > _MAX_RESOLVED_IPS:
            ips = ips[:_MAX_RESOLVED_IPS]

        asns: set[str] = set()
        owners: set[str] = set()
        whois_lines: list[str] = []
        row_errors = list(dig_errs)
        rdns_list: list[str] = []

        for ip in ips:
            rdns, rdns_err = reverse_dns(ip)
            if rdns != "—":
                rdns_list.append(rdns)
            if rdns_err:
                row_errors.append(f"{ip}:{rdns_err}")
            whois, werr = whois_for_ip(ip)
            if whois["asn"] != "—":
                asns.add(whois["asn"])
            if whois["owner"] != "—":
                owners.add(whois["owner"])
            if whois["whois_summary"] != "—":
                whois_lines.append(f"{ip}=>{whois['whois_summary']}")
            if werr:
                row_errors.append(f"{ip}:{werr}")

        rows.append(
            {
                "host": host,
                "source": "+".join(srcs),
                "ip": "—",
                "ips": ips,
                "bytes_observed": 0,
                "flow_count": 0,
                "reverse_dns": ", ".join(sorted(set(rdns_list))) if rdns_list else "—",
                "asn": ", ".join(sorted(asns)) if asns else "—",
                "owner": ", ".join(sorted(owners)) if owners else "—",
                "whois_summary": " || ".join(whois_lines)[:1000] if whois_lines else "—",
                "dig_summary": dig_summary or "—",
                "lookup_errors": row_errors,
            },
        )

    rows_sorted = sorted(
        rows,
        key=lambda r: (
            -(int(r.get("bytes_observed") or 0)),
            -(int(r.get("flow_count") or 0)),
            str(r.get("host") or ""),
        ),
    )
    for row in rows_sorted:
        row["ips_text"] = ", ".join(row.get("ips") or []) if row.get("ips") else "—"
        row["lookup_errors_text"] = "; ".join(row.get("lookup_errors") or []) or "—"

    if not rows_sorted:
        errors.append("no_pcap_host_candidates")
    return {
        "has_inventory": bool(rows_sorted),
        "rows": rows_sorted,
        "errors": errors,
        "notes": notes,
    }


def merge_har_signals_from_normalized(data: dict[str, Any]) -> dict[str, Any]:
    """Union HAR-derived fields from competitor_surface and extra.surface_probe."""
    hosts: set[str] = set()
    trackers: set[str] = set()
    cdns: set[str] = set()

    cs = data.get("competitor_surface")
    if isinstance(cs, dict):
        hs = cs.get("har_summary") or {}
        if isinstance(hs, dict):
            for h in hs.get("merged_unique_hosts") or []:
                if isinstance(h, str) and h.strip():
                    hosts.add(h.strip())
            for t in (
                (hs.get("merged_tracker_candidates") or [])
                + (hs.get("tracker_candidates") or [])
            ):
                if isinstance(t, str) and t.strip():
                    trackers.add(t.strip())
            for c in (
                (hs.get("merged_cdn_candidates") or [])
                + (hs.get("cdn_candidates") or [])
            ):
                if isinstance(c, str) and c.strip():
                    cdns.add(c.strip())

    extra = data.get("extra") or {}
    if isinstance(extra, dict):
        sp = extra.get("surface_probe") or {}
        if isinstance(sp, dict):
            hs = sp.get("har_summary") or {}
            if isinstance(hs, dict):
                for h in hs.get("merged_unique_hosts") or []:
                    if isinstance(h, str) and h.strip():
                        hosts.add(h.strip())
                for t in (
                    (hs.get("merged_tracker_candidates") or [])
                    + (hs.get("tracker_candidates") or [])
                ):
                    if isinstance(t, str) and t.strip():
                        trackers.add(t.strip())
                for c in (
                    (hs.get("merged_cdn_candidates") or [])
                    + (hs.get("cdn_candidates") or [])
                ):
                    if isinstance(c, str) and c.strip():
                        cdns.add(c.strip())

    return {
        "merged_unique_hosts": sorted(hosts),
        "merged_tracker_candidates": sorted(trackers),
        "merged_cdn_candidates": sorted(cdns),
    }


def merge_har_signals(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Merge HAR signals across all benchmark rows for one provider."""
    hosts: set[str] = set()
    trackers: set[str] = set()
    cdns: set[str] = set()
    for _rid, _p, data in rows:
        m = merge_har_signals_from_normalized(data)
        hosts.update(m["merged_unique_hosts"])
        trackers.update(m["merged_tracker_candidates"])
        cdns.update(m["merged_cdn_candidates"])
    return {
        "merged_unique_hosts": sorted(hosts),
        "merged_tracker_candidates": sorted(trackers),
        "merged_cdn_candidates": sorted(cdns),
    }


def _truncate_join(items: list[str], *, max_items: int, max_chars: int) -> str:
    """Join with comma; cap list length and total length."""
    if not items:
        return "—"
    chunk = items[:max_items]
    s = ", ".join(chunk)
    if len(items) > max_items:
        s += f" (+{len(items) - max_items} more)"
    if len(s) > max_chars:
        return s[: max_chars - 3] + "..."
    return s


def provider_dns_summary_rows(
    provider_dns: dict[str, Any] | None,
    *,
    ns_max: int = 4,
    mx_max: int = 3,
    txt_max: int = 2,
) -> list[dict[str, Any]]:
    """One row per apex domain for Markdown/HTML tables."""
    if not isinstance(provider_dns, dict):
        return []
    doms = provider_dns.get("domains") or {}
    if not isinstance(doms, dict):
        return []
    rows: list[dict[str, Any]] = []
    for dname in sorted(doms.keys()):
        entry = doms.get(dname) or {}
        if not isinstance(entry, dict):
            continue
        ns = [str(x) for x in (entry.get("ns") or []) if x]
        mx = [str(x) for x in (entry.get("mx") or []) if x]
        txt = [str(x) for x in (entry.get("txt") or []) if x]
        a_list = entry.get("a") or []
        aaaa_list = entry.get("aaaa") or []
        has_v4 = bool(a_list)
        has_v6 = bool(aaaa_list)
        if has_v6:
            ipv6_note = "yes"
        elif has_v4:
            ipv6_note = "no AAAA (IPv4-only apex)"
        else:
            ipv6_note = "—"
        rows.append(
            {
                "domain": str(dname),
                "ns": _truncate_join(ns, max_items=ns_max, max_chars=240),
                "mx": _truncate_join(mx, max_items=mx_max, max_chars=200),
                "txt_sample": _truncate_join(txt, max_items=txt_max, max_chars=180),
                "ipv6_note": ipv6_note,
            },
        )
    return rows


def surface_probe_rows(extra: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Rows for surface URL matrix (page_type, url, status, error)."""
    if not isinstance(extra, dict):
        return []
    sp = extra.get("surface_probe") or {}
    if not isinstance(sp, dict):
        return []
    probes = sp.get("probes") or []
    if not isinstance(probes, list):
        return []
    out: list[dict[str, Any]] = []
    for row in probes:
        if not isinstance(row, dict):
            continue
        out.append(
            {
                "page_type": str(row.get("page_type") or "—"),
                "url": str(row.get("url") or ""),
                "status": row.get("status"),
                "error": row.get("error"),
            },
        )
    return out


def collect_surface_probe_urls(extra: dict[str, Any] | None) -> list[str]:
    """URLs from surface matrix for dashboard display."""
    return [r["url"] for r in surface_probe_rows(extra) if r.get("url")]


def methodology_and_pcap_sections(data: dict[str, Any]) -> dict[str, Any]:
    """Compact tables for automated methodology + PCAP-derived metadata."""
    wm = data.get("website_exposure_methodology")
    if not isinstance(wm, dict):
        meth = {"has_methodology": False, "inventory_preview": [], "errors": []}
    else:
        inv = wm.get("phase9_third_party_inventory") or []
        inv_preview: list[dict[str, Any]] = []
        if isinstance(inv, list):
            for row in inv[:40]:
                if isinstance(row, dict):
                    inv_preview.append(
                        {
                            "company": row.get("company_hypothesis", ""),
                            "role": row.get("role", ""),
                            "how": row.get("how_discovered", ""),
                        },
                    )
        p8 = wm.get("phase8_dns_infra") or {}
        per_dom = p8.get("per_domain") if isinstance(p8, dict) else {}
        dom_count = len(per_dom) if isinstance(per_dom, dict) else 0
        meth = {
            "has_methodology": True,
            "tier_note": str(wm.get("evidence_tier_note") or "")[:800],
            "phase9_count": len(inv) if isinstance(inv, list) else 0,
            "phase8_domains": dom_count,
            "inventory_preview": inv_preview,
            "limits": wm.get("limits") or [],
            "errors": wm.get("errors") or [],
        }

    pc = data.get("pcap_derived")
    if not isinstance(pc, dict) or not pc:
        cap: dict[str, Any] = {"has_pcap": False, "finalize_notes": []}
    else:
        cap = {
            "has_pcap": True,
            "flows_unique_estimate": pc.get("flows_unique_estimate"),
            "packet_total": (pc.get("packet_counts") or {}).get("total"),
            "snis": (pc.get("tls_clienthello_snis_unique") or [])[:48],
            "dns_hosts": (pc.get("dns_hostnames_unique") or [])[:48],
            "limits": pc.get("limits") or [],
            "errors": pc.get("errors") or [],
            "finalize_notes": [],
        }

    fin = data.get("capture_finalize")
    if isinstance(fin, dict) and fin:
        meth_cap_note: list[str] = []
        sid = fin.get("session_id")
        if sid:
            meth_cap_note.append(f"session_id={sid}")
        ferr = fin.get("finalize_errors") or []
        if ferr:
            meth_cap_note.extend([str(x) for x in ferr[:6]])
        cap["finalize_notes"] = meth_cap_note
    host_inventory = pcap_host_intelligence(data)
    return {"methodology": meth, "pcap": cap, "pcap_hosts": host_inventory}


def per_location_web_exposure(data: dict[str, Any]) -> dict[str, Any]:
    """Compact payload for one detailed run section."""
    cs = data.get("competitor_surface")
    pd: dict[str, Any] = {}
    if isinstance(cs, dict):
        pd = cs.get("provider_dns") or {}
    if not isinstance(pd, dict):
        pd = {}

    extra = data.get("extra") or {}
    if not isinstance(extra, dict):
        extra = {}

    har = merge_har_signals_from_normalized(data)
    dns_rows = provider_dns_summary_rows(pd)
    surf_rows = surface_probe_rows(extra)

    has_any = bool(
        har["merged_unique_hosts"]
        or har["merged_tracker_candidates"]
        or har["merged_cdn_candidates"]
        or dns_rows
        or surf_rows
        or (isinstance(cs, dict) and (cs.get("web_probes") or cs.get("portal_probes")))
    )

    return {
        "har": har,
        "dns_rows": dns_rows,
        "surface_rows": surf_rows,
        "has_any": has_any,
    }


def rollup_web_exposure(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Provider-level rollup for report templates."""
    merged = merge_har_signals(rows)

    dns_domains: dict[str, Any] = {}
    for _rid, _p, data in rows:
        cs = data.get("competitor_surface")
        if not isinstance(cs, dict):
            continue
        pd = cs.get("provider_dns") or {}
        if not isinstance(pd, dict):
            continue
        doms = pd.get("domains") or {}
        if not isinstance(doms, dict):
            continue
        for k, v in doms.items():
            if isinstance(k, str) and k not in dns_domains:
                dns_domains[k] = v

    dns_rows = provider_dns_summary_rows({"domains": dns_domains})

    surface_all: list[dict[str, Any]] = []
    seen_surf: set[tuple[str, str]] = set()
    for _rid, _p, data in rows:
        ex = data.get("extra") or {}
        if isinstance(ex, dict):
            for r in surface_probe_rows(ex):
                key = (r.get("url") or "", r.get("page_type") or "")
                if key in seen_surf:
                    continue
                seen_surf.add(key)
                surface_all.append(r)

    portal_hosts: set[str] = set()
    probe_urls: list[str] = []
    for _rid, _p, data in rows:
        cs = data.get("competitor_surface")
        if not isinstance(cs, dict):
            continue
        for prow in cs.get("portal_probes") or []:
            if isinstance(prow, dict):
                h = prow.get("host")
                if isinstance(h, str) and h.strip():
                    portal_hosts.add(h.strip().lower())
        for w in cs.get("web_probes") or []:
            if isinstance(w, dict):
                u = w.get("url")
                if isinstance(u, str) and u.strip():
                    probe_urls.append(u.strip())

    has_any = bool(
        merged["merged_unique_hosts"]
        or merged["merged_tracker_candidates"]
        or merged["merged_cdn_candidates"]
        or dns_rows
        or surface_all
        or portal_hosts
        or probe_urls
    )

    return {
        "merged_har": merged,
        "dns_rows": dns_rows,
        "surface_rows": surface_all,
        "portal_hosts": sorted(portal_hosts),
        "probe_urls_sample": probe_urls[:24],
        "has_any": has_any,
    }
