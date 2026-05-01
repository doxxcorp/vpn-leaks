"""Locate tcpdump and build argument lists."""

from __future__ import annotations

import shutil
from pathlib import Path


def tcpdump_executable() -> str:
    env = shutil.which("tcpdump")
    if env:
        return env
    for cand in ("/usr/sbin/tcpdump", "/sbin/tcpdump", "/usr/bin/tcpdump"):
        if Path(cand).is_file():
            return cand
    return "tcpdump"


def tcpdump_listen_cmd(
    interface: str,
    pcap_path: Path,
    *,
    bpf: str | None = None,
) -> list[str]:
    """Command to capture all link-layer traffic to pcap_path (-U packet-buffered)."""
    cmd: list[str] = [
        tcpdump_executable(),
        "-i",
        interface,
        "-w",
        str(pcap_path),
        "-U",
        "-n",
    ]
    if bpf:
        cmd.append(bpf)
    return cmd
