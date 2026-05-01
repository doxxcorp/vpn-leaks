"""Tests for detailed VPN report context."""

from __future__ import annotations

from vpn_leaks.config_loader import repo_root
from vpn_leaks.reporting.generate_reports import (
    build_detailed_runs,
    generate_provider_report,
)


def test_build_detailed_runs_minimal() -> None:
    p = repo_root() / "runs/x/locations/loc/normalized.json"
    data = {
        "vpn_provider": "p",
        "vpn_location_id": "loc",
        "vpn_location_label": "L",
        "schema_version": "1.2",
        "exit_ip_v4": "1.2.3.4",
        "exit_ip_sources": [],
        "dns_servers_observed": [],
        "webrtc_candidates": [],
        "attribution": {},
        "policies": [],
        "services_contacted": [],
        "artifacts": {},
        "extra": {},
    }
    rows = [("run-x", p, data)]
    dr = build_detailed_runs(rows)
    assert len(dr) == 1
    assert dr[0]["run_id"] == "run-x"
    assert dr[0]["location_id"] == "loc"
    assert "```json" in dr[0]["exit_ip_sources_block"]
    assert dr[0]["yourinfo_snapshot_block"] is None
    assert dr[0]["competitor_surface_kind"] == "absent"
    assert dr[0]["competitor_surface_block"] is None
    assert dr[0]["has_framework"] is False
    assert dr[0]["framework_block"] is None
    assert isinstance(dr[0]["truncation_notes"], list)
    assert dr[0]["has_truncated_blocks"] is False


def test_generate_provider_report_progress_callback(
    monkeypatch,
    tmp_path,
) -> None:
    monkeypatch.setattr("vpn_leaks.config_loader.repo_root", lambda: tmp_path)
    monkeypatch.setattr("vpn_leaks.reporting.generate_reports.repo_root", lambda: tmp_path)

    calls: list[str] = []
    out = generate_provider_report(64512, progress_step=calls.append)
    assert out.is_file()
    assert calls == [
        "Provider report: collect evidence",
        "Provider report: render markdown",
        "Provider report: write markdown",
    ]
