"""Stable normalized.json schema (append-only evolution)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


class RunnerEnv(BaseModel):
    os: str | None = None
    kernel: str | None = None
    python: str | None = None
    browser: str | None = None
    vpn_protocol: str | None = None
    vpn_client: str | None = None


class ExitIpSource(BaseModel):
    url: str
    ipv4: str | None = None
    ipv6: str | None = None
    raw_excerpt: str | None = None
    error: str | None = None


class DnsObservation(BaseModel):
    tier: str = Field(description="local | external")
    detail: str | None = None
    servers: list[str] = Field(default_factory=list)


class WebRtcCandidate(BaseModel):
    candidate_type: str | None = None
    protocol: str | None = None
    address: str | None = None
    port: int | None = None
    raw: str | None = None


class AttributionSource(BaseModel):
    name: str
    asn: int | None = None
    holder: str | None = None
    country: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class AttributionResult(BaseModel):
    asn: int | None = None
    holder: str | None = None
    country: str | None = None
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    confidence_notes: str | None = None
    supporting_sources: list[AttributionSource] = Field(default_factory=list)
    disclaimers: list[str] = Field(default_factory=list)


class PolicyRecord(BaseModel):
    role: str = Field(description="vpn | underlay")
    url: str | None = None
    fetched_at_utc: str | None = None
    sha256: str | None = None
    summary_bullets: list[str] = Field(default_factory=list)


class ArtifactIndex(BaseModel):
    connect_log: str | None = None
    ip_check_json: str | None = None
    dnsleak_dir: str | None = None
    webrtc_dir: str | None = None
    ipv6_dir: str | None = None
    fingerprint_dir: str | None = None
    attribution_json: str | None = None
    policy_dir: str | None = None
    competitor_probe_dir: str | None = Field(
        default=None,
        description="Raw JSON/HAR from competitor-surface probes (DNS, web, portal, transit)",
    )
    yourinfo_probe_dir: str | None = Field(
        default=None,
        description="Raw JSON/HAR from yourinfo.ai benchmark load",
    )
    baseline_json: str | None = Field(
        default=None,
        description="Pre-VPN baseline snapshot under raw/baseline.json",
    )
    surface_probe_dir: str | None = Field(
        default=None,
        description="HAR/JSON from surface URL matrix under raw/.../surface_probe/",
    )
    transitions_json: str | None = Field(
        default=None,
        description="Optional transition poll log raw/.../transitions.json",
    )


class CompetitorSurfaceSnapshot(BaseModel):
    """Summarized competitor-facing signals; detail under raw/.../competitor_probe/."""

    provider_dns: dict[str, Any] = Field(default_factory=dict)
    web_probes: list[dict[str, Any]] = Field(default_factory=list)
    portal_probes: list[dict[str, Any]] = Field(default_factory=list)
    transit: dict[str, Any] = Field(default_factory=dict)
    stray_json: list[dict[str, Any]] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class EvidenceRef(BaseModel):
    """Pointer to raw artifact and/or normalized field (SPEC §11)."""

    artifact_path: str | None = None
    normalized_pointer: str | None = None
    note: str | None = None


class Finding(BaseModel):
    """Structured assessment row (SPEC §6.4, §17)."""

    id: str
    category: str
    title: str
    description: str
    severity: str = Field(description="INFO | LOW | MEDIUM | HIGH | CRITICAL")
    confidence: str = Field(description="LOW | MEDIUM | HIGH")
    kind: str = Field(description="observed | inferred | hypothesis")
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    affected_data_types: list[str] = Field(default_factory=list)
    recipients: list[str] = Field(default_factory=list)
    test_conditions: str | None = None
    reproducibility_notes: str | None = None


class QuestionCoverageRecord(BaseModel):
    """Per-question coverage (SPEC §6.5, §19)."""

    question_id: str
    question_text: str = ""
    category: str = ""
    testability: str = ""
    answer_status: str = Field(
        description="answered | partially_answered | unanswered | not_testable_dynamically",
    )
    answer_summary: str = ""
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    notes: str | None = None


class RiskScores(BaseModel):
    """Aggregate scoring (SPEC §17)."""

    overall_severity: str = "INFO"
    leak_severity: str = "INFO"
    correlation_risk: str = "LOW"
    third_party_exposure: str = "LOW"
    notes: list[str] = Field(default_factory=list)


class ObservedEndpoint(BaseModel):
    """Classified host (SPEC §6.3, §12)."""

    host: str
    classification: str = "unknown"
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    source: str = ""
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class FrameworkResult(BaseModel):
    """Synthesized framework output embedded in normalized.json (SPEC §18.2)."""

    question_bank_version: str = ""
    test_matrix_version: str = ""
    findings: list[Finding] = Field(default_factory=list)
    question_coverage: list[QuestionCoverageRecord] = Field(default_factory=list)
    risk_scores: RiskScores = Field(default_factory=RiskScores)
    observed_endpoints: list[ObservedEndpoint] = Field(default_factory=list)


class NormalizedRun(BaseModel):
    """One location run — minimum fields per project spec."""

    schema_version: str = "1.4"
    run_id: str
    timestamp_utc: str = Field(default_factory=utc_now_iso)
    runner_env: RunnerEnv = Field(default_factory=RunnerEnv)

    vpn_provider: str
    vpn_location_id: str
    vpn_location_label: str = ""
    connection_mode: str = "unknown"

    exit_ip_v4: str | None = None
    exit_ip_v6: str | None = None
    exit_ip_sources: list[ExitIpSource] = Field(default_factory=list)

    dns_servers_observed: list[DnsObservation] = Field(default_factory=list)
    dns_leak_flag: bool | None = None
    dns_leak_notes: str | None = None

    webrtc_candidates: list[WebRtcCandidate] = Field(default_factory=list)
    webrtc_leak_flag: bool | None = None
    webrtc_notes: str | None = None

    ipv6_status: str | None = Field(
        default=None,
        description="e.g. unsupported | tunneled | blocked | leaked",
    )
    ipv6_leak_flag: bool | None = None
    ipv6_notes: str | None = None

    fingerprint_snapshot: dict[str, Any] = Field(default_factory=dict)

    attribution: AttributionResult = Field(default_factory=AttributionResult)
    policies: list[PolicyRecord] = Field(default_factory=list)
    services_contacted: list[str] = Field(
        default_factory=list,
        description="Third-party URLs/services touched during this run",
    )

    artifacts: ArtifactIndex = Field(default_factory=ArtifactIndex)
    competitor_surface: CompetitorSurfaceSnapshot | None = None
    yourinfo_snapshot: dict[str, Any] | None = Field(
        default=None,
        description="yourinfo.ai page capture (HAR + excerpt); see raw/.../yourinfo_probe/",
    )
    framework: FrameworkResult | None = Field(
        default=None,
        description="Findings, coverage, risk scores (SPEC framework)",
    )
    extra: dict[str, Any] = Field(default_factory=dict)
