from __future__ import annotations

from pathlib import Path

from vpn_leaks.config_loader import repo_root


def capture_state_dir() -> Path:
    d = repo_root() / ".vpn-leaks" / "capture"
    d.mkdir(parents=True, exist_ok=True)
    return d


def active_descriptor_path() -> Path:
    return capture_state_dir() / "active.json"
