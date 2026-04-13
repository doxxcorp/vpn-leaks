"""Poll exit IP across disconnect/reconnect (SPEC §13.3) — skipped for manual_gui."""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vpn_leaks.auto_connection import quick_exit_ip


def run_transition_tests(
    *,
    leak_cfg: dict[str, Any],
    raw_dir: Path,
    connection_mode: str,
    adapter: Any,
    loc: dict[str, Any],
    stabilize: float,
    log: Callable[[str], None],
) -> dict[str, Any] | None:
    if connection_mode == "manual_gui":
        out = {
            "status": "skipped",
            "reason": "manual_gui adapter — use scripted mode for automated transitions",
        }
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / "transitions.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        return out

    samples: list[dict[str, Any]] = []

    def snap(phase: str) -> None:
        v4, _svc = quick_exit_ip(leak_cfg)
        samples.append(
            {
                "phase": phase,
                "timestamp_utc": datetime.now(UTC).isoformat(),
                "exit_ip_v4": v4,
            },
        )

    try:
        snap("connected_before_disconnect")
        log("transition_tests: disconnect")
        adapter.disconnect()
        time.sleep(1.0)
        for i in range(5):
            snap(f"after_disconnect_poll_{i}")
            time.sleep(0.4)
        log("transition_tests: reconnect")
        adapter.connect(loc)
        time.sleep(max(1.0, stabilize))
        for i in range(5):
            snap(f"after_reconnect_poll_{i}")
            time.sleep(0.4)
    except Exception as e:
        samples.append({"phase": "error", "error": str(e)[:500]})

    result = {
        "status": "ok",
        "samples": samples,
    }
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "transitions.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
