"""Pre-VPN (or current) network snapshot for comparison (SPEC §13.1)."""

from __future__ import annotations

import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vpn_leaks.auto_connection import quick_exit_ip


def _dns_snippet() -> str | None:
    if platform.system() != "Darwin":
        return None
    try:
        proc = subprocess.run(
            ["scutil", "--dns"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode == 0 and proc.stdout:
            return proc.stdout[:12000]
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return None


def capture_baseline(leak_cfg: dict[str, Any]) -> dict[str, Any]:
    """Snapshot public IP and optional resolver info using the current network path."""
    v4, services = quick_exit_ip(leak_cfg)
    return {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "exit_ip_v4": v4,
        "preflight_services": services,
        "dns_scutil_snippet": _dns_snippet(),
        "metadata": {
            "note": (
                "For a true pre-VPN baseline, disconnect the VPN before the run starts "
                "so this snapshot reflects your real ISP path."
            ),
        },
    }


def write_baseline_json(path: Path, leak_cfg: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = capture_baseline(leak_cfg)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data
