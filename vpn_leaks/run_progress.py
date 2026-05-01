"""Terminal progress for `vpn-leaks run` (tqdm bar + phase hints)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from tqdm import tqdm


def transition_runs(args: argparse.Namespace, skip_vpn: bool, mode: str) -> bool:
    return bool(
        args.transition_tests and (not skip_vpn or mode == "manual_gui"),
    )


def steps_for_full_run(args: argparse.Namespace, skip_vpn: bool, mode: str) -> int:
    """Major phases per location for a full run (must match `cmd_run` step() calls)."""
    # connect+stabilize, ip, dns, ipv6, webrtc, fp, attribution, policies,
    # yourinfo, browserleaks, competitor, surface, methodology, disconnect, write
    n = 15
    if transition_runs(args, skip_vpn, mode):
        n += 1
    return n


def compute_run_total(
    *,
    locations: list[dict[str, Any]],
    run_root: Path,
    force: bool,
    args: argparse.Namespace,
    skip_vpn: bool,
    mode: str,
) -> int:
    """Total progress ticks: per-location (skip or full) + one for run summary."""
    full = steps_for_full_run(args, skip_vpn, mode)
    total = 0
    attach_extra = (
        1 if (getattr(args, "attach_capture", False) or getattr(args, "with_pcap", False)) else 0
    )
    for loc in locations:
        loc_id = str(loc.get("id") or "default")
        norm_path = run_root / "locations" / loc_id / "normalized.json"
        if norm_path.is_file() and not force:
            total += 1
        else:
            total += full
    return total + attach_extra + 1


class RunProgress:
    """Progress bar when stderr is a TTY; otherwise one line per phase."""

    def __init__(self, total: int, *, no_progress: bool) -> None:
        self._total = total
        self._done = 0
        self._file = sys.stderr
        self._use_bar = bool(self._file.isatty() and not no_progress)
        self._pbar: tqdm | None = None
        if self._use_bar:
            self._pbar = tqdm(
                total=total,
                file=self._file,
                mininterval=0.4,
                dynamic_ncols=True,
                unit="step",
            )

    def step(self, description: str) -> None:
        self._done += 1
        if self._pbar is not None:
            self._pbar.set_description(description, refresh=False)
            self._pbar.update(1)
        else:
            print(f"[{self._done}/{self._total}] {description}", file=self._file, flush=True)

    def close(self) -> None:
        if self._pbar is not None:
            self._pbar.close()
            self._pbar = None
