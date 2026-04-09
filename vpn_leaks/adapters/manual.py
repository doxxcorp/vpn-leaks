"""Human-in-the-loop adapter: user connects via vendor GUI, then confirms."""

from __future__ import annotations

import sys
from typing import Any

from vpn_leaks.adapters.base import AdapterCapabilities, VPNAdapter


class ManualAdapter(VPNAdapter):
    def __init__(self, slug: str) -> None:
        self.slug = slug

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(automated_tunnel=False, manual_gui_assist=True)

    def connect(self, location: dict[str, Any]) -> None:
        label = location.get("label") or location.get("id") or "unknown"
        print(
            f"\n[manual adapter] Connect to location: {label}\n"
            "When the VPN shows connected, press Enter to continue...",
            file=sys.stderr,
        )
        try:
            input()
        except EOFError:
            pass

    def disconnect(self) -> None:
        print(
            "\n[manual adapter] Disconnect VPN in the client, then press Enter...",
            file=sys.stderr,
        )
        try:
            input()
        except EOFError:
            pass
