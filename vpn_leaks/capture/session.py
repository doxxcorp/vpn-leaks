"""Persistent tcpdump capture session (descriptor on disk)."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path

from vpn_leaks.capture.paths import active_descriptor_path, capture_state_dir
from vpn_leaks.capture.tcpdump_proc import tcpdump_listen_cmd


@dataclass(frozen=True)
class CaptureSessionDescriptor:
    session_id: str
    pid: int
    pcap_path: str
    interface: str
    started_at_utc: str
    bpf: str | None = None

    def to_json(self) -> dict:
        d = asdict(self)
        return d

    @staticmethod
    def from_json(row: dict) -> CaptureSessionDescriptor:
        return CaptureSessionDescriptor(
            session_id=str(row["session_id"]),
            pid=int(row["pid"]),
            pcap_path=str(row["pcap_path"]),
            interface=str(row["interface"]),
            started_at_utc=str(row["started_at_utc"]),
            bpf=row.get("bpf"),
        )


def load_active() -> CaptureSessionDescriptor | None:
    path = active_descriptor_path()
    if not path.is_file():
        return None
    try:
        row = json.loads(path.read_text(encoding="utf-8"))
        return CaptureSessionDescriptor.from_json(row)
    except (OSError, ValueError, KeyError, TypeError):
        return None


def _descriptor_path_for_quarantine(desc: CaptureSessionDescriptor) -> Path:
    return capture_state_dir() / f"aborted-{desc.session_id}.json"


def start(
    *, interface: str, bpf: str | None = None
) -> tuple[CaptureSessionDescriptor | None, str | None]:
    if load_active() is not None:
        return (
            None,
            "A capture session is already active (`vpn-leaks capture status`). "
            "Abort it first.",
        )

    sid = uuid.uuid4().hex[:12]
    capture_state_dir().mkdir(parents=True, exist_ok=True)
    pcap_path = capture_state_dir() / f"session_{sid}.pcap"
    cmd = tcpdump_listen_cmd(interface, pcap_path, bpf=bpf)
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
    except OSError as e:
        return None, f"failed to start tcpdump: {e}"

    time.sleep(0.15)
    if proc.poll() is not None:
        err = ""
        if proc.stderr:
            try:
                err = proc.stderr.read().decode("utf-8", errors="replace")[:800]
            except Exception:
                err = ""
        return None, f"tcpdump exited immediately (need sudo on many systems). {err}".strip()

    from datetime import UTC, datetime

    desc = CaptureSessionDescriptor(
        session_id=sid,
        pid=int(proc.pid),
        pcap_path=str(pcap_path.resolve()),
        interface=interface,
        started_at_utc=datetime.now(UTC).isoformat(),
        bpf=bpf,
    )
    active_descriptor_path().write_text(
        json.dumps(desc.to_json(), indent=2),
        encoding="utf-8",
    )
    return desc, None


def status() -> tuple[CaptureSessionDescriptor | None, dict[str, object]]:
    desc = load_active()
    if desc is None:
        return None, {"message": "no active capture session"}
    alive = _pid_alive(desc.pid)
    p = Path(desc.pcap_path)
    size_b = p.stat().st_size if p.is_file() else 0
    return desc, {"alive": alive, "pcap_bytes": size_b}


def abort(*, discard_pcap: bool = True) -> tuple[bool, str]:
    desc = load_active()
    if desc is None:
        return False, "no active capture session"
    _stop_pid(desc.pid)
    path = Path(desc.pcap_path)
    msg = "aborted session descriptor"
    try:
        active_descriptor_path().unlink(missing_ok=True)
    except OSError as e:
        return False, str(e)
    if discard_pcap:
        try:
            path.unlink(missing_ok=True)
            msg += "; discarded pcap"
        except OSError:
            msg += "; partial pcap left on disk"
    else:
        msg += f"; pcap retained at {path}"
    _descriptor_path_for_quarantine(desc).write_text(
        json.dumps(desc.to_json(), indent=2),
        encoding="utf-8",
    )
    return True, msg


def finalize_stop() -> tuple[CaptureSessionDescriptor | None, str | None]:
    """Stop tcpdump but keep pcap on disk; remove active.json. Caller moves the file."""
    desc = load_active()
    if desc is None:
        return None, "no_active_capture_session"
    _stop_pid(desc.pid)
    try:
        active_descriptor_path().unlink(missing_ok=True)
    except OSError:
        pass
    return desc, None


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _stop_pid(pid: int) -> None:
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(30):
            time.sleep(0.1)
            try:
                os.kill(pid, 0)
            except OSError:
                return
        os.kill(pid, signal.SIGKILL)
    except OSError:
        pass
