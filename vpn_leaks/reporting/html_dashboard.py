"""Structured context for visual-first VPN HTML reports."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any


def _truncate(s: str, max_len: int = 140) -> str:
    t = " ".join(str(s).split())
    if len(t) <= max_len:
        return t
    return t[: max_len - 1].rstrip() + "…"


def _dns_tiers_line(dns_obs: list[dict[str, Any]] | None) -> str:
    if not dns_obs:
        return "No resolver observations"
    parts: list[str] = []
    for tier in dns_obs:
        if not isinstance(tier, dict):
            continue
        name = str(tier.get("tier") or "?")
        detail = str(tier.get("detail") or "")[:48]
        servers = tier.get("servers") or []
        if isinstance(servers, list) and servers:
            snip = ", ".join(str(x) for x in servers[:3])
            if len(servers) > 3:
                snip += f" +{len(servers) - 3}"
            parts.append(f"{name}: {snip}")
        else:
            parts.append(f"{name} ({detail})" if detail else name)
    return " · ".join(parts) if parts else "—"


def _bool_flag(v: Any) -> bool | None:
    if v is True:
        return True
    if v is False:
        return False
    return None


def build_location_cards(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> list[dict[str, Any]]:
    """One card per normalized location row."""
    cards: list[dict[str, Any]] = []
    for run_id, path, data in rows:
        att = data.get("attribution") or {}
        asn = att.get("asn")
        holder = (
            str(att.get("holder") or "").strip() or None
            if isinstance(att, dict)
            else None
        )
        dns_obs = data.get("dns_servers_observed")
        if not isinstance(dns_obs, list):
            dns_obs = []
        cards.append(
            {
                "run_id": run_id,
                "location_id": str(data.get("vpn_location_id") or ""),
                "location_label": str(
                    data.get("vpn_location_label") or data.get("vpn_location_id") or "",
                ),
                "normalized_path": str(path),
                "exit_ip_v4": data.get("exit_ip_v4"),
                "exit_ip_v6": data.get("exit_ip_v6"),
                "asn": asn if isinstance(asn, int) else None,
                "asn_holder": holder,
                "connection_mode": str(data.get("connection_mode") or "unknown"),
                "dns_leak": _bool_flag(data.get("dns_leak_flag")),
                "webrtc_leak": _bool_flag(data.get("webrtc_leak_flag")),
                "ipv6_leak": _bool_flag(data.get("ipv6_leak_flag")),
                "dns_summary": _dns_tiers_line(dns_obs),
            },
        )
    return cards


def group_spec_by_category(
    merged_coverage: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """SPEC rows grouped by category for accordion UI."""
    by_cat: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in merged_coverage:
        if not isinstance(m, dict):
            continue
        cat = str(m.get("category") or "unknown")
        by_cat[cat].append(m)

    out: list[dict[str, Any]] = []
    for cat in sorted(by_cat.keys()):
        rows = sorted(by_cat[cat], key=lambda x: str(x.get("question_id") or ""))
        enriched = []
        for r in rows:
            summ = str(r.get("answer_summary") or "").strip()
            enriched.append(
                {
                    **r,
                    "answer_summary_short": _truncate(summ, 160),
                },
            )
        out.append({"category": cat, "questions": enriched})
    return out


def extract_third_party_signals(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Merge competitor_surface signals across locations (best-effort)."""
    trackers: set[str] = set()
    apex_domains: set[str] = set()
    portal_hosts: set[str] = set()
    probe_urls: list[str] = []

    for _rid, _p, data in rows:
        cs = data.get("competitor_surface")
        if not isinstance(cs, dict):
            continue
        hs = cs.get("har_summary") or {}
        if isinstance(hs, dict):
            for t in hs.get("tracker_candidates") or []:
                if isinstance(t, str) and t.strip():
                    trackers.add(t.strip())
            merged = hs.get("merged_tracker_candidates")
            if isinstance(merged, list):
                for t in merged:
                    if isinstance(t, str) and t.strip():
                        trackers.add(t.strip())
        pd = cs.get("provider_dns") or {}
        if isinstance(pd, dict):
            doms = pd.get("domains") or {}
            if isinstance(doms, dict):
                for d in doms.keys():
                    if isinstance(d, str) and d.strip():
                        apex_domains.add(d.strip().lower())
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

    return {
        "tracker_candidates": sorted(trackers)[:48],
        "apex_domains": sorted(apex_domains),
        "portal_hosts": sorted(portal_hosts),
        "probe_urls_sample": probe_urls[:12],
        "has_signals": bool(trackers or apex_domains or portal_hosts or probe_urls),
    }


def leak_flags_anywhere(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, bool]:
    return {
        "dns": any(bool(r[2].get("dns_leak_flag")) for r in rows),
        "webrtc": any(bool(r[2].get("webrtc_leak_flag")) for r in rows),
        "ipv6": any(bool(r[2].get("ipv6_leak_flag")) for r in rows),
    }


def normalize_finding(f: dict[str, Any]) -> dict[str, Any]:
    return {
        "severity": str(f.get("severity") or ""),
        "title": str(f.get("title") or ""),
        "category": str(f.get("category") or ""),
        "kind": str(f.get("kind") or ""),
    }


def build_html_dashboard_context(
    rows: list[tuple[str, Path, dict[str, Any]]],
    framework_rollup: dict[str, Any],
    *,
    markdown_basename: str,
) -> dict[str, Any]:
    """
    Dashboard props for vpn_report_document.html.j2.

    markdown_basename: e.g. NORDVPN.md (sibling link from HTML).
    """
    merged = framework_rollup.get("merged_coverage") or []
    if not isinstance(merged, list):
        merged = []

    top_raw = framework_rollup.get("top_findings") or []
    findings: list[dict[str, Any]] = []
    if isinstance(top_raw, list):
        for f in top_raw[:12]:
            if isinstance(f, dict):
                findings.append(normalize_finding(f))

    return {
        "markdown_basename": markdown_basename,
        "location_cards": build_location_cards(rows),
        "spec_by_category": group_spec_by_category(merged),
        "third_party": extract_third_party_signals(rows),
        "leak_flags": leak_flags_anywhere(rows),
        "top_findings": findings,
        "max_overall_severity": str(
            framework_rollup.get("max_overall_severity") or "INFO",
        ),
        "has_framework": bool(framework_rollup.get("has_framework")),
        "run_count": len(rows),
    }
