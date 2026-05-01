"""Capture session lifecycle (tcpdump mocked; no sudo)."""

from __future__ import annotations

import io
import json

import pytest

from vpn_leaks.capture.session import (
    CaptureSessionDescriptor,
    abort,
    finalize_stop,
    load_active,
    start,
)


class _DummyProc:
    pid = 9001
    stderr = None

    def poll(self):  # noqa: ANN201
        return None


class _EarlyExitProc:
    """tcpdump failed immediately (e.g. macOS BPF permission)."""

    pid = 9002

    def __init__(self, stderr_bytes: bytes) -> None:
        self.stderr = io.BytesIO(stderr_bytes)

    def poll(self):  # noqa: ANN201
        return 1


@pytest.fixture()
def isolate_capture_state(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:  # noqa: ANN001
    monkeypatch.setattr("vpn_leaks.capture.paths.repo_root", lambda: tmp_path)
    monkeypatch.setattr("vpn_leaks.capture.session.time.sleep", lambda _s: None)


def test_capture_start_early_exit_adds_macos_privilege_hint(
    isolate_capture_state,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,  # noqa: ARG001
) -> None:
    stderr_txt = (
        "tcpdump: en0: You don't have permission to capture on that device\n"
        "((cannot open BPF device) /dev/bpf0: Permission denied)\n"
    )
    monkeypatch.setattr(
        "vpn_leaks.capture.session.subprocess.Popen",
        lambda *_a, **_k: _EarlyExitProc(stderr_txt.encode()),
    )
    desc, err = start(interface="en0")
    assert desc is None and err is not None
    assert "need sudo on many systems" in err
    assert "BPF" in err or "/dev/bpf" in err
    assert "sudo vpn-leaks capture start" in err
    assert "sudo vpn-leaks run --provider <slug>" in err
    assert "competitive-capture-playbook.md" in err


def test_capture_start_status_abort_mocked(
    isolate_capture_state,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,  # noqa: ARG001
) -> None:
    monkeypatch.setattr(
        "vpn_leaks.capture.session.subprocess.Popen",
        lambda *_a, **_k: _DummyProc(),
    )
    desc, err = start(interface="lo0")
    assert err is None and desc is not None
    assert desc.pid == _DummyProc.pid
    loaded = load_active()
    assert loaded is not None and loaded.session_id == desc.session_id
    ok, msg = abort(discard_pcap=True)
    assert ok and "descriptor" in msg.lower()
    assert load_active() is None


def test_finalize_stop_keeps_pcap(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr("vpn_leaks.capture.paths.repo_root", lambda: tmp_path)
    cap_dir = tmp_path / ".vpn-leaks" / "capture"
    cap_dir.mkdir(parents=True)
    fake_pcap = cap_dir / "session_x.pcap"
    fake_pcap.write_bytes(b"\x01\x02")
    desc = CaptureSessionDescriptor(
        session_id="sess123456",
        pid=9002,
        pcap_path=str(fake_pcap),
        interface="lo0",
        started_at_utc="2026-05-01T00:00:00+00:00",
    )
    active = cap_dir / "active.json"
    active.write_text(json.dumps(desc.to_json()), encoding="utf-8")

    monkeypatch.setattr(
        "vpn_leaks.capture.session._stop_pid",
        lambda _pid: None,
    )
    monkeypatch.setattr("vpn_leaks.capture.session.time.sleep", lambda _s: None)
    monkeypatch.setattr("vpn_leaks.capture.session.os.kill", lambda *_a, **_k: None)

    stopped, ferr = finalize_stop()
    assert ferr is None and stopped is not None
    assert active.is_file() is False  # cleared
    assert fake_pcap.is_file()  # pcap retained for bundle move


def test_finalize_merge_invoked_with_mock_descriptor(
    tmp_path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from vpn_leaks.capture.finalize_bundle import finalize_capture_and_merge
    from vpn_leaks.models import NormalizedRun

    rr = tmp_path / "runs" / "r1"
    loc = rr / "locations" / "loc-z"
    loc.mkdir(parents=True)
    norm = loc / "normalized.json"
    n = NormalizedRun(
        run_id="r1",
        vpn_provider="unit",
        vpn_location_id="loc-z",
        vpn_location_label="z",
        connection_mode="manual_gui",
    )
    norm.write_text(n.model_dump_json(indent=2), encoding="utf-8")

    monkeypatch.setattr(
        "vpn_leaks.capture.finalize_bundle.summarize_pcap_file",
        lambda *_a, **_k: {"schema_version": "1.0", "flows_unique_estimate": 0},
    )

    cap_dir = tmp_path / ".vpn-leaks" / "capture"
    cap_dir.mkdir(parents=True)
    pcap_file = cap_dir / "sess.pcap"
    pcap_file.write_bytes(b"pcap_placeholder")

    desc = CaptureSessionDescriptor(
        session_id="sess000",
        pid=9100,
        pcap_path=str(pcap_file),
        interface="en0",
        started_at_utc="2026-05-01T00:01:00+00:00",
    )

    monkeypatch.setattr(
        "vpn_leaks.capture.finalize_bundle.finalize_stop",
        lambda: (desc, None),
    )
    monkeypatch.setattr(
        "vpn_leaks.capture.finalize_bundle.repo_root",
        lambda: tmp_path,
    )

    logs: list[str] = []

    finalize_capture_and_merge(
        run_root=rr,
        fresh_norm_paths=[norm],
        log=logs.append,
    )

    cap_out = rr / "raw" / "loc-z" / "capture"
    assert (cap_out / "session.pcap").is_file()
    updated = json.loads(norm.read_text(encoding="utf-8"))
    assert updated.get("pcap_derived") is not None
    assert isinstance(updated["pcap_derived"], dict)
    assert updated.get("artifacts", {}).get("capture_dir")
