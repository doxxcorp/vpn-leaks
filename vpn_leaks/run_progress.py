"""Terminal progress for `vpn-leaks run` (tqdm bar + phase hints)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from tqdm import tqdm

_LABEL_MAX = 40

# tqdm default-style bar: desc + pct in l_bar, n/total + ETA + rate + optional location postfix.
_BAR_FORMAT = "{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"


def _truncate_label(label: str, max_len: int = _LABEL_MAX) -> str:
    s = label.strip()
    if len(s) <= max_len:
        return s
    if max_len <= 1:
        return "…"
    return s[: max_len - 1] + "…"


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
        self._loc_prefix = ""
        if self._use_bar:
            self._pbar = tqdm(
                total=total,
                file=self._file,
                mininterval=0.4,
                dynamic_ncols=True,
                unit="step",
                bar_format=_BAR_FORMAT,
            )

    def set_location(self, index: int, total: int, label: str) -> None:
        """Annotate phases with which location is running (1-based index); does not advance the bar."""
        short = _truncate_label(label)
        self._loc_prefix = f"loc={index}/{total} ({short}) "
        if self._pbar is not None:
            self._pbar.set_postfix_str(f"{index}/{total} {short}", refresh=False)

    def clear_location(self) -> None:
        """Clear location postfix (e.g. before PCAP finalize or run summary steps)."""
        self._loc_prefix = ""
        if self._pbar is not None:
            self._pbar.set_postfix_str("", refresh=False)

    def step(self, description: str) -> None:
        self._done += 1
        if self._pbar is not None:
            self._pbar.set_description(description, refresh=False)
            self._pbar.update(1)
        else:
            body = f"{self._loc_prefix}{description}" if self._loc_prefix else description
            print(f"[{self._done}/{self._total}] {body}", file=self._file, flush=True)

    def close(self) -> None:
        if self._pbar is not None:
            self._pbar.close()
            self._pbar = None
