"""Tests for yourinfo.ai benchmark probe."""

from __future__ import annotations

from pathlib import Path

from vpn_leaks.checks.yourinfo_probe import run_yourinfo_probe


def test_skip_returns_none_no_dir(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    raw.mkdir()
    svc: list[str] = []
    assert run_yourinfo_probe(raw_dir=raw, services_contacted=svc, skip=True) is None
    assert not (raw / "yourinfo_probe").is_dir()


def test_skip_does_not_touch_services(tmp_path: Path) -> None:
    raw = tmp_path / "r"
    raw.mkdir()
    svc: list[str] = []
    run_yourinfo_probe(raw_dir=raw, services_contacted=svc, skip=True)
    assert "yourinfo" not in "".join(svc).lower()
