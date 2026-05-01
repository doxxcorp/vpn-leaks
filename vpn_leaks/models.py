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
    asn_prefixes_json: str | None = Field(
        default=None,
        description="RIPEstat announced prefixes for exit ASN (raw/<loc>/asn_prefixes.json)",
    )
    exit_dns_json: str | None = Field(
        default=None,
        description="PTR lookups for exit IPs (raw/<loc>/exit_dns.json)",
    )
    policy_dir: str | None = None
    competitor_probe_dir: str | None = Field(
        default=None,
        description="Raw JSON/HAR from competitor-surface probes (DNS, web, portal, transit)",
    )
    browserleaks_probe_dir: str | None = Field(
        default=None,
        description="BrowserLeaks Playwright captures (raw/<loc>/browserleaks_probe/)",
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
    website_exposure_dir: str | None = Field(
        default=None,
        description="Automated methodology JSON under raw/<loc>/website_exposure/",
    )
    capture_dir: str | None = Field(
        default=None,
        description="Final PCAP bundle under raw/<loc>/capture/ when attach-capture finalized",
    )


class CompetitorSurfaceSnapshot(BaseModel):
    """Summarized competitor-facing signals; detail under raw/.../competitor_probe/."""

    provider_dns: dict[str, Any] = Field(default_factory=dict)
    web_probes: list[dict[str, Any]] = Field(default_factory=list)
    har_summary: dict[str, Any] = Field(
        default_factory=dict,
        description="Aggregated HAR hosts + tracker/CDN hints; see har_summary.json",
    )
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


class WebsiteExposureMethodology(BaseModel):
    """Automated desk methodology (Phases 1–9). Tier = desk automation, not client DNS-leak (O)."""

    methodology_schema_version: str = "1.0"
    evidence_tier_note: str = Field(
        default=(
            "Desk automation of website-exposure methodology (Phases 1–9). "
            "Do not conflate with client resolver / DNS-leak observations (O); see "
            "docs/research-questions-and-evidence.md."
        ),
    )
    phases: dict[str, Any] = Field(
        default_factory=dict,
        description="Compact summaries per methodology phase.",
    )
    hosts_inventory: dict[str, Any] = Field(default_factory=dict)
    resolver_results: dict[str, Any] = Field(default_factory=dict)
    classifications: dict[str, Any] = Field(default_factory=dict)
    phase8_dns_infra: dict[str, Any] = Field(default_factory=dict)
    phase9_third_party_inventory: list[dict[str, Any]] = Field(default_factory=list)
    raw_relpaths: dict[str, str] = Field(
        default_factory=dict,
        description="Paths relative to repo root for methodology JSON artifacts.",
    )
    limits: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class CaptureSessionFinalize(BaseModel):
    """Recorded when a tcpdump attach-capture session is finalized."""

    session_id: str | None = None
    finalized_at_utc: str | None = None
    source_pcap_cache_path: str | None = Field(
        default=None,
        description="Original cache path prior to moving into runs/ (audit).",
    )
    finalize_errors: list[str] = Field(default_factory=list)


class NormalizedRun(BaseModel):
    """One location run — minimum fields per project spec."""

    schema_version: str = "1.5"
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
    browserleaks_snapshot: dict[str, Any] | None = Field(
        default=None,
        description="Pinned browserleaks.com pages (HAR + per-page excerpts)",
    )
    framework: FrameworkResult | None = Field(
        default=None,
        description="Findings, coverage, risk scores (SPEC framework)",
    )
    website_exposure_methodology: WebsiteExposureMethodology | None = Field(
        default=None,
        description="Automated website exposure methodology (Phases 1–9).",
    )
    pcap_derived: dict[str, Any] | None = Field(
        default=None,
        description="Summarized PCAP (pcap_summary.json payload); metadata-only, no Wireshark.",
    )
    capture_finalize: CaptureSessionFinalize | None = Field(
        default=None,
        description="Attach-capture session finalization audit row.",
    )
    extra: dict[str, Any] = Field(default_factory=dict)
