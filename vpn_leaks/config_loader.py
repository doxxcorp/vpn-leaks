"""Load YAML configs from repo configs/ directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at {path}")
    return data


def load_vpn_config(slug: str) -> dict[str, Any]:
    path = repo_root() / "configs" / "vpns" / f"{slug}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"Missing VPN config: {path}")
    return load_yaml(path)


def load_leak_tests_config() -> dict[str, Any]:
    path = repo_root() / "configs" / "tools" / "leak-tests.yaml"
    return load_yaml(path) if path.is_file() else {}


def load_attribution_config() -> dict[str, Any]:
    path = repo_root() / "configs" / "tools" / "attribution.yaml"
    return load_yaml(path) if path.is_file() else {}
