"""Aggregate severity / risk from findings and flags (SPEC §17)."""

from __future__ import annotations

from vpn_leaks.models import Finding, NormalizedRun, RiskScores

_ORDER = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]


def _max_sev(a: str, b: str) -> str:
    try:
        return a if _ORDER.index(a) >= _ORDER.index(b) else b
    except ValueError:
        return b


def score_risk(run: NormalizedRun, findings: list[Finding]) -> RiskScores:
    notes: list[str] = []
    leak = "INFO"
    if run.dns_leak_flag is True:
        leak = _max_sev(leak, "CRITICAL")
        notes.append("DNS leak flag set.")
    if run.webrtc_leak_flag is True:
        leak = _max_sev(leak, "HIGH")
        notes.append("WebRTC leak flag set.")
    if run.ipv6_leak_flag is True:
        leak = _max_sev(leak, "HIGH")
        notes.append("IPv6 leak flag set.")

    for f in findings:
        if f.category in ("dns", "real_ip_leak") and f.severity != "INFO":
            leak = _max_sev(leak, f.severity)

    overall = "INFO"
    for f in findings:
        overall = _max_sev(overall, f.severity)

    third = "LOW"
    if run.competitor_surface and (
        run.competitor_surface.web_probes or run.competitor_surface.portal_probes
    ):
        third = "MEDIUM"
        notes.append("Competitor web/portal probes executed.")
    if run.yourinfo_snapshot:
        third = _max_sev(third, "LOW")

    corr = "LOW"
    if run.fingerprint_snapshot or run.yourinfo_snapshot:
        corr = "MEDIUM"
    if len(run.services_contacted) > 30:
        corr = _max_sev(corr, "MEDIUM")
        notes.append("Large services_contacted list.")

    return RiskScores(
        overall_severity=overall,
        leak_severity=leak,
        correlation_risk=corr,
        third_party_exposure=third,
        notes=notes,
    )
