"""Tests for `vpn_leaks.run_progress` step totals (must stay in sync with `cmd_run`)."""

from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from vpn_leaks.run_progress import (
    RunProgress,
    compute_run_total,
    steps_for_full_run,
    transition_runs,
)


def _ns(**kwargs: object) -> argparse.Namespace:
    base = {
        "transition_tests": False,
        "attach_capture": False,
        "with_pcap": False,
    }
    base.update(kwargs)
    return argparse.Namespace(**base)


def test_transition_runs_manual_gui_with_skip_vpn() -> None:
    args = _ns(transition_tests=True)
    assert transition_runs(args, skip_vpn=True, mode="manual_gui") is True


def test_transition_skipped_when_skip_vpn_and_not_manual_gui() -> None:
    args = _ns(transition_tests=True)
    assert transition_runs(args, skip_vpn=True, mode="openvpn") is False


def test_steps_for_full_run_without_transition() -> None:
    args = _ns(transition_tests=False)
    assert steps_for_full_run(args, skip_vpn=False, mode="openvpn") == 15


def test_steps_for_full_run_with_transition() -> None:
    args = _ns(transition_tests=True)
    assert steps_for_full_run(args, skip_vpn=False, mode="openvpn") == 16


def test_steps_for_full_run_transition_stub_manual_gui() -> None:
    args = _ns(transition_tests=True)
    assert steps_for_full_run(args, skip_vpn=True, mode="manual_gui") == 16


def test_compute_run_total_one_location_full(tmp_path: Path) -> None:
    args = _ns(transition_tests=False)
    run_root = tmp_path / "run"
    # No normalized.json -> full pipeline + summary
    assert (
        compute_run_total(
            locations=[{"id": "loc1"}],
            run_root=run_root,
            force=False,
            args=args,
            skip_vpn=True,
            mode="manual_gui",
        )
        == 16
    )


def test_compute_run_total_skip_cached_location(tmp_path: Path) -> None:
    args = _ns(transition_tests=False)
    run_root = tmp_path / "run"
    norm = run_root / "locations" / "loc1" / "normalized.json"
    norm.parent.mkdir(parents=True)
    norm.write_text("{}", encoding="utf-8")
    assert (
        compute_run_total(
            locations=[{"id": "loc1"}],
            run_root=run_root,
            force=False,
            args=args,
            skip_vpn=True,
            mode="manual_gui",
        )
        == 2
    )


def test_compute_run_total_force_reruns_full(tmp_path: Path) -> None:
    args = _ns(transition_tests=False)
    run_root = tmp_path / "run"
    norm = run_root / "locations" / "loc1" / "normalized.json"
    norm.parent.mkdir(parents=True)
    norm.write_text("{}", encoding="utf-8")
    assert (
        compute_run_total(
            locations=[{"id": "loc1"}],
            run_root=run_root,
            force=True,
            args=args,
            skip_vpn=True,
            mode="manual_gui",
        )
        == 16
    )


def test_compute_run_total_attach_adds_finalize_tick(tmp_path: Path) -> None:
    args = _ns(transition_tests=False, attach_capture=True)
    run_root = tmp_path / "run"
    assert (
        compute_run_total(
            locations=[{"id": "loc1"}],
            run_root=run_root,
            force=False,
            args=args,
            skip_vpn=True,
            mode="manual_gui",
        )
        == 17
    )


def test_compute_run_total_with_pcap_adds_finalize_tick(tmp_path: Path) -> None:
    args = _ns(transition_tests=False, attach_capture=False, with_pcap=True)
    run_root = tmp_path / "run"
    assert (
        compute_run_total(
            locations=[{"id": "loc1"}],
            run_root=run_root,
            force=False,
            args=args,
            skip_vpn=True,
            mode="manual_gui",
        )
        == 17
    )


def test_run_progress_no_bar_prints_lines(capsys: pytest.CaptureFixture[str]) -> None:
    rp = RunProgress(3, no_progress=True)
    try:
        rp.step("a")
        rp.step("b")
    finally:
        rp.close()
    err = capsys.readouterr().err
    assert "[1/3] a" in err
    assert "[2/3] b" in err


def test_run_progress_location_prefix_then_clear(capsys: pytest.CaptureFixture[str]) -> None:
    rp = RunProgress(4, no_progress=True)
    try:
        rp.set_location(1, 3, "us-east")
        rp.step("VPN connect + stabilize")
        rp.step("Exit IP check")
        rp.clear_location()
        rp.step("Writing run summary")
    finally:
        rp.close()
    err = capsys.readouterr().err
    assert "[1/4] loc=1/3 (us-east) VPN connect + stabilize" in err
    assert "[2/4] loc=1/3 (us-east) Exit IP check" in err
    assert "[3/4] Writing run summary" in err


def test_run_progress_truncates_long_location_label(capsys: pytest.CaptureFixture[str]) -> None:
    long_label = "a" * 50
    rp = RunProgress(1, no_progress=True)
    try:
        rp.set_location(2, 4, long_label)
        rp.step("x")
    finally:
        rp.close()
    err = capsys.readouterr().err
    assert "loc=2/4" in err
    assert "(" in err and "…)" in err
    assert "[1/1] loc=2/4 (" in err


def test_run_progress_close_idempotent() -> None:
    rp = RunProgress(1, no_progress=True)
    rp.close()
    rp.close()
