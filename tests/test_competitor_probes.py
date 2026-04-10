"""Tests for competitor-surface probes."""

from __future__ import annotations

from pathlib import Path

from vpn_leaks.checks.competitor_probes import run_competitor_probes


def test_no_config_returns_none(tmp_path: Path) -> None:
    assert (
        run_competitor_probes(
            {},
            raw_base=tmp_path,
            exit_ip_v4="1.1.1.1",
            services_contacted=[],
        )
        is None
    )


def test_empty_probe_section_returns_none(tmp_path: Path) -> None:
    assert (
        run_competitor_probes(
            {"competitor_probe": {}},
            raw_base=tmp_path,
            exit_ip_v4="1.1.1.1",
            services_contacted=[],
        )
        is None
    )


def test_transit_only_runs_with_exit_ip(tmp_path: Path) -> None:
    snap = run_competitor_probes(
        {"competitor_probe": {"provider_domains": []}},
        raw_base=tmp_path,
        exit_ip_v4="8.8.8.8",
        services_contacted=[],
        skip_dns=True,
        skip_web=True,
        skip_portal=True,
        skip_stray_json=True,
    )
    assert snap is not None
    assert "target" in snap.transit
