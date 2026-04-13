"""Derive structured findings from normalized run data."""

from __future__ import annotations

import uuid

from vpn_leaks.models import EvidenceRef, Finding, NormalizedRun


def _fid(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def build_findings(run: NormalizedRun) -> list[Finding]:
    out: list[Finding] = []

    if run.dns_leak_flag is True:
        out.append(
            Finding(
                id=_fid("finding-dns"),
                category="dns",
                title="DNS leak heuristic triggered",
                description=(
                    "The harness flagged a possible DNS leak. "
                    "Review dns_servers_observed and raw dnsleak HTML."
                ),
                severity="CRITICAL",
                confidence="MEDIUM",
                kind="observed",
                evidence_refs=[
                    EvidenceRef(normalized_pointer="dns_leak_flag"),
                    EvidenceRef(normalized_pointer="dns_servers_observed"),
                ],
                affected_data_types=["dns_queries"],
                recipients=["dns_resolver_operators", "vpn_provider"],
                test_conditions="connected_state",
                reproducibility_notes=run.dns_leak_notes,
            ),
        )

    if run.webrtc_leak_flag is True:
        out.append(
            Finding(
                id=_fid("finding-webrtc"),
                category="real_ip_leak",
                title="WebRTC leak heuristic triggered",
                description=(
                    "ICE candidates suggest exposure inconsistent with expected tunnel identity."
                ),
                severity="HIGH",
                confidence="MEDIUM",
                kind="observed",
                evidence_refs=[
                    EvidenceRef(normalized_pointer="webrtc_leak_flag"),
                    EvidenceRef(normalized_pointer="webrtc_candidates"),
                ],
                affected_data_types=["public_ip", "local_ip"],
                recipients=["stun_peers", "webrtc_peers"],
                test_conditions="connected_state",
                reproducibility_notes=run.webrtc_notes,
            ),
        )

    if run.ipv6_leak_flag is True:
        out.append(
            Finding(
                id=_fid("finding-ipv6"),
                category="real_ip_leak",
                title="IPv6 leak heuristic triggered",
                description="IPv6 path may bypass or expose non-tunnel identity.",
                severity="HIGH",
                confidence="MEDIUM",
                kind="observed",
                evidence_refs=[
                    EvidenceRef(normalized_pointer="ipv6_leak_flag"),
                    EvidenceRef(normalized_pointer="ipv6_status"),
                ],
                affected_data_types=["ipv6_address"],
                recipients=["upstream_networks"],
                test_conditions="connected_state",
                reproducibility_notes=run.ipv6_notes,
            ),
        )

    # Inferred third-party exposure from YourInfo / competitor (non-fatal)
    if run.yourinfo_snapshot and isinstance(run.yourinfo_snapshot, dict):
        out.append(
            Finding(
                id=_fid("finding-yourinfo"),
                category="third_party_web",
                title="Third-party benchmark page loaded (yourinfo.ai)",
                description=(
                    "HAR and page excerpt captured for competitive benchmark; "
                    "third parties may observe exit IP and browser metadata."
                ),
                severity="LOW",
                confidence="HIGH",
                kind="inferred",
                evidence_refs=[EvidenceRef(normalized_pointer="yourinfo_snapshot")],
                affected_data_types=["public_ip", "user_agent", "browser_fingerprint"],
                recipients=["yourinfo.ai", "asset_hosts"],
                test_conditions="connected_state_benchmark",
            ),
        )

    if not out:
        out.append(
            Finding(
                id=_fid("finding-clean"),
                category="summary",
                title="No leak flags raised by core heuristics",
                description=(
                    "DNS/WebRTC/IPv6 leak flags were not set. "
                    "This does not prove absence of all leaks."
                ),
                severity="INFO",
                confidence="MEDIUM",
                kind="observed",
                evidence_refs=[
                    EvidenceRef(
                        normalized_pointer="dns_leak_flag",
                        note="false or null",
                    ),
                ],
                affected_data_types=[],
                recipients=[],
                test_conditions="connected_state",
                reproducibility_notes="Heuristic limits apply; see methodology.",
            ),
        )

    return out
