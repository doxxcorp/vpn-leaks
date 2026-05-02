"""Structured context for visual-first VPN HTML reports."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from vpn_leaks.reporting.benchmark_location import format_benchmark_location_display
from vpn_leaks.reporting.web_exposure import (
    build_capture_workspace_rollup,
    collect_surface_probe_urls,
    merge_har_signals,
    rollup_web_exposure,
)

# Slugs with a vendored icon under style/icons/<slug>.svg (see configs/framework/questions.yaml).
_SPEC_CATEGORY_ICON_SLUGS: frozenset[str] = frozenset(
    {
        "identity_correlation",
        "signup_payment",
        "website_portal",
        "dns",
        "real_ip_leak",
        "control_plane",
        "exit_infrastructure",
        "third_party_web",
        "browser_tracking",
        "telemetry_app",
        "os_specific",
        "failure_state",
        "logging_retention",
    },
)


def _category_icon_href(category: str) -> str:
    slug = str(category or "unknown").strip()
    if slug not in _SPEC_CATEGORY_ICON_SLUGS:
        slug = "default"
    return f"../style/icons/{slug}.svg"


def _spec_list_preview(row: dict[str, Any]) -> str:
    """One line for collapsed SPEC row: answers and/or actionable next steps."""
    status = str(row.get("answer_status") or "")
    summ = str(row.get("answer_summary") or "").strip()
    ns = str(row.get("next_steps") or "").strip()
    if status == "answered":
        return summ if summ else "—"
    if status == "unanswered":
        return ns if ns else "—"
    if status == "partially_answered":
        if summ and ns and ns != "—":
            if ns in summ:
                return summ
            return f"{summ} · {ns}"
        return summ or ns or "—"
    if status == "not_testable_dynamically":
        return ns if ns else summ or "—"
    return summ or ns or "—"


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
        full_label = str(
            data.get("vpn_location_label") or data.get("vpn_location_id") or "",
        )
        display_label = format_benchmark_location_display(data) or full_label
        cards.append(
            {
                "run_id": run_id,
                "location_id": str(data.get("vpn_location_id") or ""),
                "location_label": full_label,
                "location_label_display": display_label,
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
                    "list_preview": _spec_list_preview(r),
                },
            )
        label = (
            str(cat).replace("_", " ") if str(cat).strip() else "unknown"
        )
        out.append(
            {
                "category": cat,
                "category_label": label,
                "icon_href": _category_icon_href(cat),
                "questions": enriched,
            },
        )
    return out


def extract_third_party_signals(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Merge competitor_surface + surface_probe HAR signals across locations (best-effort)."""
    merged_har = merge_har_signals(rows)
    trackers: set[str] = set(merged_har["merged_tracker_candidates"])
    cdns: set[str] = set(merged_har["merged_cdn_candidates"])
    apex_domains: set[str] = set()
    portal_hosts: set[str] = set()
    probe_urls: list[str] = []
    surface_urls: list[str] = []

    for _rid, _p, data in rows:
        cs = data.get("competitor_surface")
        if isinstance(cs, dict):
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
        extra = data.get("extra") or {}
        if isinstance(extra, dict):
            surface_urls.extend(collect_surface_probe_urls(extra))

    seen_surf: set[str] = set()
    surface_unique: list[str] = []
    for u in surface_urls:
        if u not in seen_surf:
            seen_surf.add(u)
            surface_unique.append(u)

    has_signals = bool(
        merged_har["merged_unique_hosts"]
        or merged_har["merged_tracker_candidates"]
        or merged_har["merged_cdn_candidates"]
        or apex_domains
        or portal_hosts
        or probe_urls
        or surface_unique
    )

    return {
        "tracker_candidates": sorted(trackers)[:48],
        "cdn_candidates": sorted(cdns)[:48],
        "apex_domains": sorted(apex_domains),
        "portal_hosts": sorted(portal_hosts),
        "probe_urls_sample": probe_urls[:12],
        "surface_urls_sample": surface_unique[:12],
        "has_signals": has_signals,
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
    pcap_intel_per_run: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Dashboard props for vpn_report_document.html.j2.

    markdown_basename: e.g. NORDVPN.md (sibling link from HTML).
    pcap_intel_per_run: pre-computed pcap_host_intelligence results keyed by run_id,
        avoids re-running whois/dig lookups that already ran during Markdown generation.
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

    web_exposure = rollup_web_exposure(rows)
    capture_workspace = build_capture_workspace_rollup(rows, pcap_intel_per_run=pcap_intel_per_run)

    return {
        "markdown_basename": markdown_basename,
        "capture_workspace": capture_workspace,
        "location_cards": build_location_cards(rows),
        "spec_by_category": group_spec_by_category(merged),
        "third_party": extract_third_party_signals(rows),
        "web_exposure": web_exposure,
        "leak_flags": leak_flags_anywhere(rows),
        "top_findings": findings,
        "max_overall_severity": str(
            framework_rollup.get("max_overall_severity") or "INFO",
        ),
        "has_framework": bool(framework_rollup.get("has_framework")),
        "run_count": len(rows),
    }
