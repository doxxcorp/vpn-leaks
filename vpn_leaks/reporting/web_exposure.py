"""Rollup helpers for website-exposure methodology outputs (HAR + provider DNS + surface matrix)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


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
    return {"methodology": meth, "pcap": cap}


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
