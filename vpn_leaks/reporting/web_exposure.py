"""Rollup helpers for website-exposure methodology outputs (HAR + provider DNS + surface matrix)."""

from __future__ import annotations

import ipaddress
import json
import re
import socket
import subprocess
import time
from pathlib import Path
from typing import Any

from vpn_leaks.attribution import bgp_lookup as _bgp_module

_DIG_TIMEOUT_S = 6
_WHOIS_TIMEOUT_S = 8
_MAX_TXT_VALUES = 4
_MAX_RESOLVED_IPS = 12
_IP_INTEL_CACHE_TTL_S: int = 30 * 86400  # 30 days

# Module-level persistent IP intelligence cache (loaded lazily from disk)
_ip_intel_disk_cache: dict[str, dict[str, Any]] = {}
_ip_intel_cache_loaded: bool = False


def _ip_cache_path() -> Path:
    from vpn_leaks.config_loader import repo_root  # avoid circular at module load

    return repo_root() / ".cache" / "vpn_leaks" / "ip_intel.json"


def _load_ip_intel_cache() -> dict[str, dict[str, Any]]:
    global _ip_intel_disk_cache, _ip_intel_cache_loaded
    if _ip_intel_cache_loaded:
        return _ip_intel_disk_cache
    _ip_intel_cache_loaded = True
    try:
        p = _ip_cache_path()
        if p.is_file():
            _ip_intel_disk_cache = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return _ip_intel_disk_cache


def _save_ip_intel_cache() -> None:
    try:
        p = _ip_cache_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(
            json.dumps(_ip_intel_disk_cache, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except Exception:
        pass


def _ip_cache_fresh(entry: dict[str, Any]) -> bool:
    return (time.time() - float(entry.get("cached_at", 0))) < _IP_INTEL_CACHE_TTL_S


def _cymru_asn_bulk(ips: list[str]) -> dict[str, str]:
    """Batch BGP origin ASN lookup via Team Cymru whois (single TCP connection).

    Returns {ip: "ASnnnn"} for each IP that has a routing origin.
    Falls back to empty dict on any network error — callers should handle "—" gracefully.
    """
    if not ips:
        return {}
    try:
        query = "begin\nverbose\n" + "\n".join(ips) + "\nend\n"
        s = socket.create_connection(("whois.cymru.com", 43), timeout=15)
        s.sendall(query.encode())
        chunks: list[str] = []
        while True:
            data = s.recv(8192)
            if not data:
                break
            chunks.append(data.decode("utf-8", errors="replace"))
        s.close()
        result: dict[str, str] = {}
        for line in "".join(chunks).splitlines():
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2 and parts[0].isdigit():
                result[parts[1]] = f"AS{parts[0]}"
        return result
    except Exception:
        return {}


def _cymru_asn_names_bulk(asns: list[str]) -> dict[str, str]:
    """Lookup org names for ASN strings via Team Cymru whois bulk API.

    Returns {asn: "Org Name"} e.g. {"AS3356": "Level 3 Parent, LLC"}.
    Falls back to empty dict on network error.
    Response format (verbose): ASN | CC | registry | date | Handle - Name, CC
    """
    if not asns:
        return {}
    nums = [a.lstrip("ASas") for a in asns if a.lstrip("ASas").isdigit()]
    if not nums:
        return {}
    try:
        query = "begin\nverbose\n" + "\n".join(f"AS{n}" for n in nums) + "\nend\n"
        s = socket.create_connection(("whois.cymru.com", 43), timeout=15)
        s.sendall(query.encode())
        chunks: list[str] = []
        while True:
            data = s.recv(8192)
            if not data:
                break
            chunks.append(data.decode("utf-8", errors="replace"))
        s.close()
        result: dict[str, str] = {}
        for line in "".join(chunks).splitlines():
            parts = [p.strip() for p in line.split("|")]
            # verbose ASN line: asn | CC | registry | date | Handle - Name, CC
            if len(parts) >= 5 and parts[0].isdigit():
                raw = parts[4].strip()
                # "ATT-INTERNET4 - AT&T Enterprises, LLC, US" → "AT&T Enterprises, LLC"
                if " - " in raw:
                    raw = raw.split(" - ", 1)[1]
                raw = re.sub(r",\s+[A-Z]{2}$", "", raw).strip()
                result[f"AS{parts[0]}"] = raw or f"AS{parts[0]}"
        return result
    except Exception:
        return {}


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
    """Build per-location PCAP host intelligence rows with whois/dig enrichment.

    Results are cached to disk (.cache/vpn_leaks/ip_intel.json, 30-day TTL) so
    subsequent report runs skip live lookups for already-seen IPs.
    ASN is resolved via standard whois first, then a single bulk Team Cymru TCP
    query for any IPs where whois didn't return a routing origin.
    """
    pcap = data.get("pcap_derived")
    if not isinstance(pcap, dict) or not pcap:
        return {"has_inventory": False, "rows": [], "errors": [], "notes": []}

    ip_rows, host_sources = _pcap_candidate_hosts(pcap)
    rows = list(ip_rows.values())
    errors: list[str] = []
    notes = [
        "Scope: public peer IPs from PCAP flows/pairs plus DNS/SNI hostnames from PCAP.",
        "Live lookups cached 30 days in .cache/vpn_leaks/ip_intel.json.",
    ]

    disk_cache = _load_ip_intel_cache()
    now_ts = time.time()

    rdns_cache: dict[str, str] = {}
    whois_cache: dict[str, dict[str, str]] = {}
    dig_cache: dict[tuple[str, bool], tuple[str, dict[str, list[str]], list[str]]] = {}
    bgp_cache: dict[str, dict[str, Any]] = {}

    # Pre-populate local caches from fresh disk entries (skips live lookups)
    _empty_resolved: dict[str, list[str]] = {
        "a": [], "aaaa": [], "cname": [], "mx": [], "txt": [], "ptr": []
    }
    for ip, entry in disk_cache.items():
        if ip.startswith("__") or not _ip_cache_fresh(entry):
            continue
        if "rdns" in entry:
            rdns_cache[ip] = entry["rdns"]
        if "asn" in entry:
            whois_cache[ip] = {
                "asn": entry.get("asn", "—"),
                "owner": entry.get("owner", "—"),
                "whois_summary": entry.get("whois_summary", "—"),
            }
        if "dig_summary" in entry:
            dig_cache[(ip, True)] = (
                entry["dig_summary"],
                entry.get("dig_resolved") or dict(_empty_resolved),
                [],
            )
        if "prefix" in entry:
            bgp_cache[ip] = {
                "asn": entry.get("asn", "—"),
                "upstream_asn": entry.get("upstream_asn"),
                "prefix": entry.get("prefix"),
                "source": "routeviews_bgp",
            }

    # Pre-populate hostname dig results from __hostnames__ sub-dict
    for hostname, entry in (disk_cache.get("__hostnames__") or {}).items():
        if _ip_cache_fresh(entry) and "dig_summary" in entry:
            dig_cache[(hostname, False)] = (
                entry["dig_summary"],
                entry.get("dig_resolved") or dict(_empty_resolved),
                [],
            )

    def reverse_dns(ip: str) -> tuple[str, str | None]:
        if ip in rdns_cache:
            return rdns_cache[ip], None
        try:
            ptr = socket.gethostbyaddr(ip)[0].strip(".").lower()
            rdns_cache[ip] = ptr
        except Exception:
            rdns_cache[ip] = "—"
        disk_cache.setdefault(ip, {})["rdns"] = rdns_cache[ip]
        if rdns_cache[ip] == "—":
            return "—", "reverse_dns_failed"
        return rdns_cache[ip], None

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
        disk_cache.setdefault(ip, {}).update(
            {"asn": parsed["asn"], "owner": parsed["owner"],
             "whois_summary": parsed["whois_summary"]}
        )
        return parsed, None

    def bgp_for_ip(ip: str) -> dict[str, Any]:
        """Return BGP routing data from local DB (cached). Sets upstream_asn + prefix."""
        if ip in bgp_cache:
            return bgp_cache[ip]
        result = _bgp_module.lookup_ip(ip)
        bgp_cache[ip] = result
        if result.get("prefix"):
            disk_cache.setdefault(ip, {}).update({
                "upstream_asn": result.get("upstream_asn"),
                "prefix": result.get("prefix"),
            })
        if result.get("asn"):
            disk_cache.setdefault(ip, {}).setdefault("asn_bgp", result["asn"])
        return result

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
            dig_summary_str, dig_resolved, dig_errs_live = _dig_summary_for_host(ip, is_ip=True)
            dig_cache[dig_key] = (dig_summary_str, dig_resolved, dig_errs_live)
            disk_cache.setdefault(ip, {}).update(
                {"dig_summary": dig_summary_str, "dig_resolved": dig_resolved}
            )
        dig_summary, _resolved, dig_errs = dig_cache[dig_key]
        row["dig_summary"] = dig_summary or "—"
        row_errors.extend(dig_errs)

        whois, werr = whois_for_ip(ip)
        row["asn"] = whois["asn"]
        row["owner"] = whois["owner"]
        row["whois_summary"] = whois["whois_summary"]
        if werr:
            row_errors.append(werr)

        # BGP lookup: fill ASN when whois failed + always provide prefix + upstream
        bgp = bgp_for_ip(ip)
        if row["asn"] == "—" and bgp.get("asn"):
            row["asn"] = bgp["asn"]
            whois_cache.setdefault(ip, {})["asn"] = bgp["asn"]
            disk_cache.setdefault(ip, {})["asn"] = bgp["asn"]
        row["upstream_asn"] = bgp.get("upstream_asn") or disk_cache.get(ip, {}).get("upstream_asn")
        row["prefix"] = bgp.get("prefix") or disk_cache.get(ip, {}).get("prefix")

        row["lookup_errors"] = row_errors

    # Team Cymru fallback for IPs still missing ASN after whois + BGP lookup
    ips_need_asn = [
        str(row.get("ip") or "")
        for row in rows
        if str(row.get("ip") or "") and row.get("asn") == "—"
    ]
    if ips_need_asn:
        cymru = _cymru_asn_bulk(ips_need_asn)
        for row in rows:
            ip = str(row.get("ip") or "")
            if ip in cymru:
                row["asn"] = cymru[ip]
                if ip in whois_cache:
                    whois_cache[ip]["asn"] = cymru[ip]
                disk_cache.setdefault(ip, {})["asn"] = cymru[ip]

    for host in sorted(host_sources.keys()):
        srcs = sorted(host_sources[host])
        dig_key = (host, False)
        if dig_key not in dig_cache:
            dig_summary_str, dig_resolved, dig_errs_live = _dig_summary_for_host(host, is_ip=False)
            dig_cache[dig_key] = (dig_summary_str, dig_resolved, dig_errs_live)
            hostname_store = disk_cache.setdefault("__hostnames__", {})
            hostname_store[host] = {
                "dig_summary": dig_summary_str,
                "dig_resolved": dig_resolved,
                "cached_at": now_ts,
            }
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

    # Stamp cached_at for any IP entry updated in this call, then persist
    for ip, entry in disk_cache.items():
        if ip.startswith("__") or not isinstance(entry, dict):
            continue
        has_data = "rdns" in entry or "asn" in entry or "dig_summary" in entry
        if "cached_at" not in entry and has_data:
            entry["cached_at"] = now_ts
    _save_ip_intel_cache()

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


def _fmt_bytes(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.1f} KB"
    return f"{n} B"


# rDNS suffix → canonical company (checked first — most reliable for major CDNs)
_RDNS_COMPANY: list[tuple[str, str]] = [
    (".1e100.net", "Google"),
    (".google.com", "Google"),
    (".googleusercontent.com", "Google"),
    (".googlevideo.com", "Google"),
    (".googleapis.com", "Google"),
    (".gvt1.com", "Google"),
    (".gvt2.com", "Google"),
    (".cloudflare.com", "Cloudflare"),
    (".cloudflare-dns.com", "Cloudflare"),
    (".amazonaws.com", "Amazon"),
    (".awsdns", "Amazon"),
    (".aws.com", "Amazon"),
    (".apple.com", "Apple"),
    (".icloud.com", "Apple"),
    (".mzstatic.com", "Apple"),
    (".akamai.net", "Akamai"),
    (".akamaiedge.net", "Akamai"),
    (".akamaitechnologies.com", "Akamai"),
    (".fastly.net", "Fastly"),
    (".fastly.com", "Fastly"),
    (".facebook.com", "Meta"),
    (".fbcdn.net", "Meta"),
    (".instagram.com", "Meta"),
    (".github.com", "GitHub"),
    (".github.io", "GitHub"),
    (".githubusercontent.com", "GitHub"),
    (".dropbox.com", "Dropbox"),
    (".dropboxusercontent.com", "Dropbox"),
    (".microsoft.com", "Microsoft"),
    (".azure.com", "Microsoft"),
    (".windows.net", "Microsoft"),
    (".office.com", "Microsoft"),
    (".level3.net", "Lumen Technologies"),
    (".lumen.com", "Lumen Technologies"),
]

# WHOIS org-handle prefix → canonical company (checked when rDNS gives no match)
_OWNER_PREFIX_COMPANY: list[tuple[str, str]] = [
    ("CLOUDFLARENET", "Cloudflare"),
    ("CLOUDFLARE", "Cloudflare"),
    ("GOOGLE", "Google"),
    ("GOOGL", "Google"),
    ("GOGL", "Google"),
    ("AMAZON", "Amazon"),
    ("AMAZO", "Amazon"),
    ("APPLE-WWINET", "Apple"),
    ("APPLE", "Apple"),
    ("AKAMAI", "Akamai"),
    ("FASTLY", "Fastly"),
    ("FACEBOOK", "Meta"),
    ("FB-", "Meta"),
    ("INSTAGRAM", "Meta"),
    ("GITHU", "GitHub"),
    ("LVLT", "Lumen Technologies"),
    ("LEVEL3", "Lumen Technologies"),
    ("DROPB", "Dropbox"),
    ("MSFT", "Microsoft"),
    ("MICROSOFT", "Microsoft"),
    ("AZURE", "Microsoft"),
    ("AT-88", "AT&T"),
    ("ATTNI", "AT&T"),
    ("PACKETHUB", "Packethub"),
    ("CDNEXT", "Datacamp / CDNext"),
]


def _heuristic_canonical(owner: str, rdns: str) -> str | None:
    """Return canonical company name from rDNS suffix or owner handle prefix."""
    rdns_lower = (rdns or "").lower().strip(".")
    for suffix, name in _RDNS_COMPANY:
        if rdns_lower.endswith(suffix.lstrip(".")):
            return name
    owner_upper = (owner or "").upper().strip()
    for prefix, name in _OWNER_PREFIX_COMPANY:
        if owner_upper.startswith(prefix.upper()):
            return name
    return None


def _normalize_org_names_llm(
    entries: list[dict[str, str]],
) -> dict[str, str]:
    """Use Claude Opus to canonicalize remaining unknown org names.

    entries: list of {owner, rdns} dicts that heuristic couldn't resolve.
    Returns {owner: canonical_name} mapping; empty dict on any error.
    Requires ANTHROPIC_API_KEY in the environment.
    """
    unique_owners = sorted({e["owner"] for e in entries if e["owner"] not in ("—", "")})
    if len(unique_owners) <= 1:
        return {}
    try:
        import anthropic  # optional dep; fail-soft if absent

        client = anthropic.Anthropic()
        names_list = "\n".join(f"- {n}" for n in unique_owners)
        msg = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Map these raw WHOIS/BGP org registration handles to canonical parent "
                        "company names for a network security report. "
                        "Group handle variants and subsidiaries under one name. "
                        "Return ONLY a JSON object {raw: canonical}. "
                        "No markdown, no explanation.\n\n"
                        f"Handles:\n{names_list}"
                    ),
                }
            ],
        )
        text = msg.content[0].text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(
                line for line in lines if not line.startswith("```")
            ).strip()
        result = json.loads(text)
        if isinstance(result, dict):
            return {str(k): str(v) for k, v in result.items()}
        return {}
    except Exception:
        return {}


def build_capture_workspace_rollup(
    rows: list[tuple[str, Path, dict[str, Any]]],
    pcap_intel_per_run: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Aggregate PCAP peer IPs across all runs into company→ASN→IP clusters.

    Uses whois-enriched rows from pcap_host_intelligence (pre-computed when
    pcap_intel_per_run is provided, otherwise computed fresh per run).
    Raw WHOIS org names are normalized to canonical company names via Claude Opus
    before grouping, so GOOGL-2/GOGL/GOOGLE all cluster under Google.
    """
    ip_index: dict[str, dict[str, Any]] = {}
    all_snis: set[str] = set()
    all_dns_hosts: set[str] = set()
    run_count_with_pcap = 0

    for run_id, _path, data in rows:
        pcap = data.get("pcap_derived")
        if not isinstance(pcap, dict) or not pcap:
            continue
        run_count_with_pcap += 1

        # SNIs and DNS hosts come from raw pcap_derived fields
        for sni in pcap.get("tls_clienthello_snis_unique") or []:
            if isinstance(sni, str) and sni.strip():
                all_snis.add(sni.strip().lower())
        for host in pcap.get("dns_hostnames_unique") or []:
            if isinstance(host, str) and host.strip():
                all_dns_hosts.add(host.strip().lower())

        # Get whois-enriched intel (pre-computed or fresh)
        if pcap_intel_per_run is not None and run_id in pcap_intel_per_run:
            intel = pcap_intel_per_run[run_id]
        else:
            intel = pcap_host_intelligence(data)

        for row in intel.get("rows") or []:
            if not isinstance(row, dict):
                continue
            ip = str(row.get("host") or row.get("ip") or "")
            if not ip or not _is_public_ip(ip):
                continue

            b = int(row.get("bytes_observed") or 0)
            f = int(row.get("flow_count") or 0)
            asn = str(row.get("asn") or "—")
            owner = str(row.get("owner") or "—")
            rdns = str(row.get("reverse_dns") or "—")
            src = str(row.get("source") or "pcap_peer_ip")
            whois_summary = str(row.get("whois_summary") or "—")
            upstream_asn = row.get("upstream_asn") or None
            prefix = row.get("prefix") or None

            if ip not in ip_index:
                ip_index[ip] = {
                    "ip": ip,
                    "bytes": b,
                    "flows": f,
                    "sources": src,
                    "reverse_dns": rdns,
                    "asn": asn,
                    "owner": owner,
                    "whois_summary": whois_summary,
                    "upstream_asn": upstream_asn,
                    "prefix": prefix,
                    "run_ids": [run_id],
                }
            else:
                entry = ip_index[ip]
                entry["bytes"] += b
                entry["flows"] += f
                if run_id not in entry["run_ids"]:
                    entry["run_ids"].append(run_id)
                # Promote attribution if this run has it and entry doesn't
                if entry["asn"] == "—" and asn != "—":
                    entry["asn"] = asn
                    entry["owner"] = owner
                    entry["whois_summary"] = whois_summary
                if entry["reverse_dns"] == "—" and rdns != "—":
                    entry["reverse_dns"] = rdns
                if not entry.get("upstream_asn") and upstream_asn:
                    entry["upstream_asn"] = upstream_asn
                if not entry.get("prefix") and prefix:
                    entry["prefix"] = prefix

    if not ip_index:
        return {
            "has_data": False,
            "companies": [],
            "kpis": {
                "company_count": 0,
                "raw_org_count": 0,
                "asn_count": 0,
                "ip_count": 0,
                "sni_count": len(all_snis),
                "dns_host_count": len(all_dns_hosts),
                "run_count_with_pcap": run_count_with_pcap,
            },
            "all_snis": sorted(all_snis)[:200],
            "all_dns_hosts": sorted(all_dns_hosts)[:200],
        }

    # Resolve upstream ASN numbers → org names (cached in ip_intel.json under __upstream_asns__)
    _dc = _load_ip_intel_cache()
    upstream_asn_cache: dict[str, str] = dict(_dc.get("__upstream_asns__") or {})
    unknown_upstream = [
        ua for ua in {e.get("upstream_asn") for e in ip_index.values() if e.get("upstream_asn")}
        if ua not in upstream_asn_cache
    ]
    if unknown_upstream:
        fetched = _cymru_asn_names_bulk(unknown_upstream)
        upstream_asn_cache.update(fetched)
        _dc["__upstream_asns__"] = upstream_asn_cache
        _save_ip_intel_cache()
    for entry in ip_index.values():
        ua = entry.get("upstream_asn")
        entry["upstream_org"] = upstream_asn_cache.get(ua, ua) if ua else None

    # Count unique raw WHOIS handles before any normalization
    raw_org_count = len({e["owner"] for e in ip_index.values() if e["owner"] not in ("—", "")})

    # Step 1: heuristic normalization (rDNS suffix + owner prefix lookup)
    heuristic_map: dict[str, str] = {}
    for entry in ip_index.values():
        raw = entry["owner"]
        if raw in ("—", ""):
            continue
        if raw not in heuristic_map:
            result = _heuristic_canonical(raw, entry["reverse_dns"])
            heuristic_map[raw] = result if result else raw

    # Step 2: LLM normalization for names the heuristic couldn't resolve
    unresolved = [
        {"owner": raw, "rdns": ""}
        for raw, canonical in heuristic_map.items()
        if canonical == raw  # heuristic didn't change it
    ]
    llm_map = _normalize_org_names_llm(unresolved)

    def _canonical(raw: str) -> str:
        if raw in ("—", ""):
            return "Unknown / no whois"
        # LLM takes priority over heuristic for names it resolved
        if raw in llm_map:
            return llm_map[raw]
        return heuristic_map.get(raw, raw)

    # Group: canonical_owner → asn → [ip entries]
    owner_asn: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for entry in ip_index.values():
        owner = _canonical(entry["owner"])
        asn = entry["asn"] if entry["asn"] != "—" else "—"
        owner_asn.setdefault(owner, {}).setdefault(asn, []).append(entry)

    companies: list[dict[str, Any]] = []
    for owner, asn_map in owner_asn.items():
        asns: list[dict[str, Any]] = []
        owner_bytes = 0
        owner_ips = 0
        for asn, ip_entries in sorted(asn_map.items()):
            sorted_ips = sorted(ip_entries, key=lambda r: (-r["bytes"], r["ip"]))
            asns.append({"asn": asn, "ips": sorted_ips})
            owner_bytes += sum(r["bytes"] for r in ip_entries)
            owner_ips += len(ip_entries)
        # Sort ASNs: known first, then alphabetically
        asns.sort(key=lambda a: (a["asn"] == "—", a["asn"]))
        companies.append(
            {
                "name": owner,
                "asns": asns,
                "ip_count": owner_ips,
                "bytes_total": owner_bytes,
                "bytes_display": _fmt_bytes(owner_bytes) if owner_bytes else "",
            }
        )

    companies.sort(key=lambda c: (-c["bytes_total"], c["name"].lower()))

    # Cap total IP rows across all companies
    _MAX_IPS = 200
    total = 0
    for co in companies:
        for asn_grp in co["asns"]:
            remaining = _MAX_IPS - total
            if remaining <= 0:
                asn_grp["ips"] = []
            elif len(asn_grp["ips"]) > remaining:
                asn_grp["ips"] = asn_grp["ips"][:remaining]
            total += len(asn_grp["ips"])

    unique_asns: set[str] = set()
    for co in companies:
        for a in co["asns"]:
            if a["asn"] != "—":
                unique_asns.add(a["asn"])

    return {
        "has_data": True,
        "companies": companies,
        "kpis": {
            "company_count": len(companies),
            "raw_org_count": raw_org_count,
            "asn_count": len(unique_asns),
            "ip_count": len(ip_index),
            "sni_count": len(all_snis),
            "dns_host_count": len(all_dns_hosts),
            "run_count_with_pcap": run_count_with_pcap,
        },
        "all_snis": sorted(all_snis)[:200],
        "all_dns_hosts": sorted(all_dns_hosts)[:200],
    }
