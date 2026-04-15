"""Map question bank entries to coverage rows given a NormalizedRun."""

from __future__ import annotations

import json
from typing import Any

from vpn_leaks.config_loader import repo_root
from vpn_leaks.framework.load import QuestionDef
from vpn_leaks.models import CompetitorSurfaceSnapshot, EvidenceRef, NormalizedRun, QuestionCoverageRecord


def _ev(field: str, note: str | None = None) -> EvidenceRef:
    return EvidenceRef(normalized_pointer=field, note=note)


def _row(
    q: QuestionDef,
    *,
    status: str,
    summary: str,
    refs: list[EvidenceRef] | None = None,
    notes: str | None = None,
) -> QuestionCoverageRecord:
    return QuestionCoverageRecord(
        question_id=q.id,
        question_text=q.text,
        category=q.category,
        testability=q.testability,
        answer_status=status,
        answer_summary=summary,
        evidence_refs=refs or [],
        notes=notes,
    )


def _not_dynamic(q: QuestionDef, reason: str) -> QuestionCoverageRecord:
    return _row(
        q,
        status="not_testable_dynamically",
        summary=reason,
        notes=q.testability,
    )


def _has_web_or_portal_probes(cs: CompetitorSurfaceSnapshot | None) -> bool:
    if not cs:
        return False
    return bool(cs.web_probes or cs.portal_probes)


def _has_browserleaks_data(run: NormalizedRun) -> bool:
    bl = run.browserleaks_snapshot
    if not isinstance(bl, dict) or not bl:
        return False
    pages = bl.get("pages")
    if isinstance(pages, list) and len(pages) > 0:
        return True
    return bool(bl)


def _read_exit_dns_payload(run: NormalizedRun) -> dict[str, Any] | None:
    art = run.artifacts
    if not art or not art.exit_dns_json:
        return None
    path = repo_root() / art.exit_dns_json
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    return raw if isinstance(raw, dict) else None


def _collect_ptr_names(payload: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for key in ("ptr_v4", "ptr_v6"):
        block = payload.get(key)
        if not isinstance(block, dict):
            continue
        ptrs = block.get("ptr")
        if isinstance(ptrs, list):
            out.extend(str(p) for p in ptrs if p)
    return sorted(set(out))


def _exit_geo_vs_label_summary(run: NormalizedRun) -> str:
    extra = run.extra if isinstance(run.extra, dict) else {}
    geo = extra.get("exit_geo")
    if not isinstance(geo, dict):
        return "Use auto-location or manual label vs attribution country."
    label = (run.vpn_location_label or "").strip()
    glabel = str(geo.get("location_label") or "").strip()
    gid = str(geo.get("location_id") or "").strip()
    loc_id = (run.vpn_location_id or "").strip()
    if glabel and label and glabel.lower() == label.lower():
        return (
            f"Consistent: exit_geo.location_label matches vpn_location_label ({label!r})."
        )
    if gid and loc_id and gid == loc_id:
        return f"Consistent: exit_geo.location_id matches vpn_location_id ({loc_id!r})."
    city = str(geo.get("city") or "").strip()
    region = str(geo.get("region") or "").strip()
    cc = str(geo.get("country_code") or "").strip()
    if city and label and city.lower() in label.lower():
        if not region or region.lower() in label.lower():
            return (
                f"Likely consistent: exit_geo city/region ({city}, {region}, {cc}) "
                f"appear in vpn_location_label ({label!r})."
            )
    if glabel or city:
        return (
            f"Inconclusive or mismatch: exit_geo suggests {glabel or city or 'n/a'}; "
            f"vpn_location_label={label!r}."
        )
    return "Compare extra.exit_geo fields to vpn_location_label."


def _ip014_summary(run: NormalizedRun) -> tuple[str, str]:
    """Return (status, summary) for IP-014."""
    sources = list(run.exit_ip_sources or [])
    v4s = [s.ipv4.strip() for s in sources if s.ipv4 and str(s.ipv4).strip()]
    uniq = sorted(set(v4s))
    if len(uniq) > 1:
        return (
            "partially_answered",
            f"Disagreement: distinct IPv4 values across echo endpoints: {', '.join(uniq)}.",
        )
    if len(sources) <= 1:
        return (
            "partially_answered",
            "Single echo endpoint or no multi-source data.",
        )
    ip = uniq[0] if uniq else "n/a"
    return (
        "partially_answered",
        f"All {len(sources)} echo endpoints agree on IPv4 {ip}.",
    )


def _coverage_for_question(q: QuestionDef, run: NormalizedRun) -> QuestionCoverageRecord:
    # Identity
    if q.id == "IDENTITY-001":
        has_fp = bool(run.fingerprint_snapshot)
        yi = run.yourinfo_snapshot or {}
        has_yi = bool(isinstance(yi, dict) and yi)
        has_bl = _has_browserleaks_data(run)
        return _row(
            q,
            status="partially_answered",
            summary="Browser/session signals captured via fingerprint and optional YourInfo probe.",
            refs=[
                _ev("fingerprint_snapshot"),
                _ev("yourinfo_snapshot"),
                _ev("browserleaks_snapshot"),
            ],
            notes=(
                None
                if (has_fp or has_yi or has_bl)
                else "Limited identifiers without fingerprint/YourInfo/BrowserLeaks data."
            ),
        )
    if q.id == "IDENTITY-006":
        return _row(
            q,
            status="partially_answered",
            summary=(
                "Services contacted list enumerates URLs used during harness "
                "(may include auth-adjacent endpoints)."
            ),
            refs=[_ev("services_contacted")],
        )
    if q.id == "IDENTITY-009":
        has_fp = bool(run.fingerprint_snapshot)
        has_bl = _has_browserleaks_data(run)
        if has_fp and has_bl:
            summ = (
                "Fingerprint and BrowserLeaks captures present for re-identification risk assessment."
            )
        elif has_fp:
            summ = "Fingerprint snapshot available for re-identification risk assessment."
        elif has_bl:
            summ = "BrowserLeaks probe data available for re-identification risk assessment."
        else:
            summ = "No fingerprint or BrowserLeaks snapshot; re-ID risk unassessed."
        return _row(
            q,
            status="partially_answered",
            summary=summ,
            refs=[_ev("fingerprint_snapshot"), _ev("browserleaks_snapshot")],
        )

    # Signup
    if q.id in ("SIGNUP-001", "SIGNUP-004", "SIGNUP-010"):
        cs = run.competitor_surface
        has_surface = _has_web_or_portal_probes(cs)
        if not has_surface:
            return _row(
                q,
                status="partially_answered",
                summary=(
                    "No competitor web HAR in this run; "
                    "configure competitor_probe and surface_urls."
                ),
                notes="",
            )
        return _row(
            q,
            status="partially_answered",
            summary=(
                "Third-party/CDN signals may appear in competitor web probes and HAR artifacts."
            ),
            refs=[_ev("competitor_surface")],
        )

    # Web / portal
    if q.id == "WEB-001":
        if run.competitor_surface and run.competitor_surface.provider_dns:
            return _row(
                q,
                status="partially_answered",
                summary="Apex DNS/NS data recorded for configured provider domains.",
                refs=[_ev("competitor_surface.provider_dns")],
            )
        return _row(
            q,
            status="unanswered",
            summary="",
            notes="Configure competitor_probe.provider_domains.",
        )
    if q.id == "WEB-004":
        cs = run.competitor_surface
        if cs and cs.web_probes:
            return _row(
                q,
                status="partially_answered",
                summary="Response headers / CDN signatures captured in web probes.",
                refs=[_ev("competitor_surface.web_probes")],
            )
        if cs and cs.portal_probes:
            return _row(
                q,
                status="partially_answered",
                summary="Response headers / CDN signatures captured in portal HTTPS probes.",
                refs=[_ev("competitor_surface.portal_probes")],
            )
        return _row(
            q,
            status="unanswered",
            summary="",
            notes="No web or portal probes in run.",
        )
    if q.id == "WEB-008":
        return _row(
            q,
            status="partially_answered",
            summary="Review web probe headers, redirects, and HAR for origin leaks.",
            refs=[_ev("competitor_surface")],
        )

    # DNS
    if q.id == "DNS-001":
        if run.dns_servers_observed:
            return _row(
                q,
                status="answered",
                summary="Resolver tiers observed (local + external).",
                refs=[_ev("dns_servers_observed")],
            )
        return _row(q, status="unanswered", summary="", notes="No DNS observations.")
    if q.id in ("DNS-002", "DNS-003", "DNS-011"):
        if run.dns_servers_observed:
            return _row(
                q,
                status="partially_answered",
                summary=f"Leak flag={run.dns_leak_flag}; see notes.",
                refs=[_ev("dns_servers_observed"), _ev("dns_leak_notes")],
                notes=run.dns_leak_notes,
            )
        return _row(q, status="unanswered", summary="", notes="No DNS observations.")
    if q.id == "DNS-004":
        extra = run.extra or {}
        trans = extra.get("transition_tests") or extra.get("transitions")
        if trans:
            return _row(
                q,
                status="partially_answered",
                summary="Transition samples captured.",
                refs=[_ev("extra.transition_tests")],
            )
        return _row(
            q,
            status="partially_answered",
            summary=(
                "Connect/disconnect DNS not sampled; use --transition-tests when supported."
            ),
        )
    if q.id == "DNS-009":
        return _row(
            q,
            status="partially_answered",
            summary="DoH/DoT not isolated from resolver snapshot; inspect raw captures.",
            refs=[_ev("dns_servers_observed")],
        )

    # IP
    if q.id == "IP-001":
        if run.exit_ip_v4:
            leak = run.dns_leak_flag or run.webrtc_leak_flag or run.ipv6_leak_flag
            st = "answered" if not leak else "partially_answered"
            return _row(
                q,
                status=st,
                summary=(
                    f"Exit IPv4 {run.exit_ip_v4}; leak flags dns={run.dns_leak_flag} "
                    f"webrtc={run.webrtc_leak_flag} ipv6={run.ipv6_leak_flag}."
                ),
                refs=[_ev("exit_ip_v4"), _ev("exit_ip_sources")],
            )
        return _row(q, status="unanswered", summary="", notes="No exit IPv4.")
    if q.id == "IP-002":
        if run.exit_ip_v6:
            return _row(
                q,
                status="answered",
                summary=f"Exit IPv6 observed: {run.exit_ip_v6}",
                refs=[_ev("exit_ip_v6")],
            )
        return _row(
            q,
            status="partially_answered",
            summary="No IPv6 exit or IPv6 not returned by endpoints.",
            refs=[_ev("exit_ip_sources")],
        )
    if q.id == "IP-006":
        if run.webrtc_candidates:
            return _row(
                q,
                status="answered",
                summary=f"WebRTC candidates captured; leak flag={run.webrtc_leak_flag}.",
                refs=[_ev("webrtc_candidates"), _ev("webrtc_leak_flag")],
                notes=run.webrtc_notes,
            )
        return _row(q, status="unanswered", summary="", notes="No WebRTC candidates.")
    if q.id == "IP-007":
        return _row(
            q,
            status="partially_answered",
            summary="Inspect host candidates vs LAN; see webrtc_notes.",
            refs=[_ev("webrtc_candidates")],
            notes=run.webrtc_notes,
        )
    if q.id == "IP-014":
        st, summ = _ip014_summary(run)
        return _row(
            q,
            status=st,
            summary=summ,
            refs=[_ev("exit_ip_sources")],
        )

    # Control plane
    if q.id == "CTRL-002":
        if run.services_contacted:
            return _row(
                q,
                status="partially_answered",
                summary="Post-harness service list captured.",
                refs=[_ev("services_contacted")],
            )
        return _row(q, status="unanswered", summary="", notes="No services list.")
    if q.id == "CTRL-003":
        return _not_dynamic(
            q,
            "Auth/control-plane inventory requires internal docs or app instrumentation.",
        )
    if q.id == "CTRL-004":
        return _row(
            q,
            status="partially_answered",
            summary="Infer from services_contacted and classified endpoints.",
            refs=[_ev("services_contacted")],
        )
    if q.id == "CTRL-009":
        cs = run.competitor_surface
        if cs and cs.web_probes:
            return _row(
                q,
                status="partially_answered",
                summary="CDN/WAF hints from web headers.",
                refs=[_ev("competitor_surface.web_probes")],
            )
        if cs and cs.portal_probes:
            return _row(
                q,
                status="partially_answered",
                summary="CDN/WAF hints from portal HTTPS probes.",
                refs=[_ev("competitor_surface.portal_probes")],
            )
        return _row(q, status="unanswered", summary="", notes="No web or portal probes.")

    # Exit
    if q.id == "EXIT-001":
        if run.exit_ip_v4:
            return _row(
                q,
                status="answered",
                summary=f"Exit IPv4 {run.exit_ip_v4} for location {run.vpn_location_id}.",
                refs=[_ev("exit_ip_v4")],
            )
        return _row(q, status="unanswered", summary="", notes="")
    if q.id in ("EXIT-002", "EXIT-003"):
        if run.attribution and run.attribution.asn:
            return _row(
                q,
                status="answered",
                summary=f"ASN {run.attribution.asn} — {run.attribution.holder or 'unknown holder'}",
                refs=[_ev("attribution")],
            )
        return _row(
            q,
            status="partially_answered",
            summary="Attribution incomplete.",
            refs=[_ev("attribution")],
        )
    if q.id == "EXIT-004":
        payload = _read_exit_dns_payload(run)
        refs: list[EvidenceRef] = [_ev("artifacts.exit_dns_json")]
        if payload is None:
            return _row(
                q,
                status="partially_answered",
                summary="No exit_dns.json path or file not readable; PTR unknown.",
                refs=[_ev("attribution")],
            )
        ptrs = _collect_ptr_names(payload)
        if ptrs:
            return _row(
                q,
                status="answered",
                summary=f"PTR for exit: {', '.join(ptrs)}",
                refs=refs,
            )
        err_bits: list[str] = []
        for key in ("ptr_v4", "ptr_v6"):
            block = payload.get(key)
            if isinstance(block, dict) and block.get("error"):
                err_bits.append(f"{key}: {block.get('error')}")
        if err_bits:
            return _row(
                q,
                status="partially_answered",
                summary="PTR lookup errors: " + "; ".join(err_bits),
                refs=refs,
            )
        return _row(
            q,
            status="partially_answered",
            summary="PTR lookup completed; no reverse DNS records returned for exit IP(s).",
            refs=refs,
        )
    if q.id == "EXIT-005":
        geo = (run.extra or {}).get("exit_geo") if isinstance(run.extra, dict) else None
        summ = _exit_geo_vs_label_summary(run)
        if geo:
            return _row(
                q,
                status="partially_answered",
                summary=summ,
                refs=[_ev("extra.exit_geo"), _ev("vpn_location_label")],
            )
        return _row(
            q,
            status="partially_answered",
            summary=summ,
            refs=[_ev("vpn_location_label"), _ev("attribution")],
        )

    # Third-party web
    if q.id in ("THIRDWEB-001", "THIRDWEB-003", "THIRDWEB-012"):
        if run.competitor_surface and (
            run.competitor_surface.web_probes
            or run.competitor_surface.portal_probes
            or run.competitor_surface.errors
        ):
            return _row(
                q,
                status="partially_answered",
                summary="See web HAR + competitor_surface for external scripts/analytics.",
                refs=[_ev("competitor_surface")],
            )
        return _row(
            q,
            status="unanswered",
            summary="",
            notes="Enable competitor_probe or surface_urls.",
        )

    # Fingerprint
    if q.id == "FP-001":
        if run.fingerprint_snapshot:
            return _row(
                q,
                status="partially_answered",
                summary="Fingerprint snapshot present.",
                refs=[_ev("fingerprint_snapshot")],
            )
        if _has_browserleaks_data(run):
            return _row(
                q,
                status="partially_answered",
                summary="BrowserLeaks probe pages captured (canvas/WebGL/tls signals in raw excerpts).",
                refs=[_ev("browserleaks_snapshot")],
            )
        return _row(q, status="unanswered", summary="", notes="No fingerprint data.")
    if q.id == "FP-011":
        return _row(
            q,
            status="answered",
            summary="WebRTC exercised by harness on leak-test pages.",
            refs=[_ev("webrtc_candidates")],
        )

    # Telemetry
    if q.id in ("TELEM-001", "TELEM-004"):
        return _not_dynamic(
            q,
            (
                "App telemetry requires traffic capture or binary analysis; "
                "not proven by this harness alone."
            ),
        )

    # OS
    if q.id == "OS-001":
        return _row(
            q,
            status="partially_answered",
            summary=(
                f"OS snapshot: {run.runner_env.os or 'unknown'}; "
                "no process-level tunnel bypass test in this run."
            ),
            refs=[_ev("runner_env")],
        )

    # Failure
    if q.id in ("FAIL-001", "FAIL-003"):
        extra = run.extra or {}
        trans = extra.get("transition_tests")
        if trans:
            return _row(
                q,
                status="partially_answered",
                summary="Transition samples captured.",
                refs=[_ev("extra.transition_tests")],
            )
        return _row(
            q,
            status="partially_answered",
            summary="Not sampled; optional --transition-tests or manual observation.",
        )
    if q.id == "FAIL-004":
        return _not_dynamic(
            q,
            "Crash/kill leak tests not run in this harness by default.",
        )

    # Logging
    if q.id == "LOG-001":
        return _row(
            q,
            status="partially_answered",
            summary="Infer logging surface from observable endpoints and services_contacted.",
            refs=[_ev("services_contacted")],
        )
    if q.id == "LOG-005":
        if run.policies:
            return _row(
                q,
                status="partially_answered",
                summary="Policy text captured; compare claims to observed traffic manually.",
                refs=[_ev("policies")],
            )
        return _row(
            q,
            status="unanswered",
            summary="",
            notes="No policy fetch or failed fetch.",
        )

    return _row(
        q,
        status="unanswered",
        summary="",
        notes="No handler for this question id.",
    )


def build_question_coverage(
    run: NormalizedRun,
    questions: list[QuestionDef],
) -> list[QuestionCoverageRecord]:
    return [_coverage_for_question(q, run) for q in questions]
