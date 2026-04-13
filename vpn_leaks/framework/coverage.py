"""Map question bank entries to coverage rows given a NormalizedRun."""

from __future__ import annotations

from vpn_leaks.framework.load import QuestionDef
from vpn_leaks.models import EvidenceRef, NormalizedRun, QuestionCoverageRecord


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


def _coverage_for_question(q: QuestionDef, run: NormalizedRun) -> QuestionCoverageRecord:
    # Identity
    if q.id == "IDENTITY-001":
        has_fp = bool(run.fingerprint_snapshot)
        yi = run.yourinfo_snapshot or {}
        has_yi = bool(isinstance(yi, dict) and yi)
        return _row(
            q,
            status="partially_answered",
            summary="Browser/session signals captured via fingerprint and optional YourInfo probe.",
            refs=[_ev("fingerprint_snapshot"), _ev("yourinfo_snapshot")],
            notes=(
                None
                if (has_fp or has_yi)
                else "Limited identifiers without fingerprint/YourInfo data."
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
        return _row(
            q,
            status="partially_answered",
            summary="Fingerprint snapshot available for re-identification risk assessment.",
            refs=[_ev("fingerprint_snapshot")],
        )

    # Signup
    if q.id in ("SIGNUP-001", "SIGNUP-004", "SIGNUP-010"):
        cs = run.competitor_surface
        has_web = bool(cs and cs.web_probes)
        if not has_web:
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
        if run.competitor_surface and run.competitor_surface.web_probes:
            return _row(
                q,
                status="partially_answered",
                summary="Response headers / CDN signatures captured in web probes.",
                refs=[_ev("competitor_surface.web_probes")],
            )
        return _row(q, status="unanswered", summary="", notes="No web probes in run.")
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
        if len(run.exit_ip_sources or []) > 1:
            return _row(
                q,
                status="partially_answered",
                summary="Multiple IP echo endpoints; compare exit_ip_sources for disagreement.",
                refs=[_ev("exit_ip_sources")],
            )
        return _row(
            q,
            status="partially_answered",
            summary="Single endpoint or no disagreement data.",
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
        if run.competitor_surface and run.competitor_surface.web_probes:
            return _row(
                q,
                status="partially_answered",
                summary="CDN/WAF hints from web headers.",
                refs=[_ev("competitor_surface.web_probes")],
            )
        return _row(q, status="unanswered", summary="", notes="No web probes.")

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
        return _row(
            q,
            status="partially_answered",
            summary="rDNS not always in merge; see raw attribution JSON if present.",
            refs=[_ev("attribution")],
        )
    if q.id == "EXIT-005":
        geo = (run.extra or {}).get("exit_geo") if isinstance(run.extra, dict) else None
        if geo:
            return _row(
                q,
                status="partially_answered",
                summary="Compare extra.exit_geo to advertised location label.",
                refs=[_ev("extra.exit_geo")],
            )
        return _row(
            q,
            status="partially_answered",
            summary="Use auto-location or manual label vs attribution country.",
            refs=[_ev("vpn_location_label"), _ev("attribution")],
        )

    # Third-party web
    if q.id in ("THIRDWEB-001", "THIRDWEB-003", "THIRDWEB-012"):
        if run.competitor_surface and (
            run.competitor_surface.web_probes or run.competitor_surface.errors
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
