"""Resolve adapter class from VPN config."""

from __future__ import annotations

from typing import Any

from vpn_leaks.adapters.base import VPNAdapter
from vpn_leaks.adapters.manual import ManualAdapter
from vpn_leaks.adapters.wireguard import WireGuardAdapter


def get_adapter(slug: str, vpn_config: dict[str, Any]) -> VPNAdapter:
    mode = (vpn_config.get("connection_mode") or "manual_gui").lower()
    adapter_name = (vpn_config.get("adapter") or "").lower()

    if adapter_name == "wireguard" or mode == "wireguard":
        return WireGuardAdapter(slug)
    if adapter_name == "manual" or mode == "manual_gui":
        return ManualAdapter(slug)

    # default: manual assist
    return ManualAdapter(slug)
