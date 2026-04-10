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


class CompetitorSurfaceSnapshot(BaseModel):
    """Summarized competitor-facing signals; detail under raw/.../competitor_probe/."""

    provider_dns: dict[str, Any] = Field(default_factory=dict)
    web_probes: list[dict[str, Any]] = Field(default_factory=list)
    portal_probes: list[dict[str, Any]] = Field(default_factory=list)
    transit: dict[str, Any] = Field(default_factory=dict)
    stray_json: list[dict[str, Any]] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class NormalizedRun(BaseModel):
    """One location run — minimum fields per project spec."""

    schema_version: str = "1.2"
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
    extra: dict[str, Any] = Field(default_factory=dict)
