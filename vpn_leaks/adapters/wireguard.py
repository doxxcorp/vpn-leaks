"""WireGuard via `wg-quick` (optional; requires root on most systems)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from vpn_leaks.adapters.base import AdapterCapabilities, VPNAdapter


class WireGuardAdapter(VPNAdapter):
    """Uses WG_QUICK_UP / config path from location or env."""

    def __init__(self, slug: str) -> None:
        self.slug = slug
        self._iface: str | None = None

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities(automated_tunnel=True, manual_gui_assist=False)

    def connect(self, location: dict[str, Any]) -> None:
        conf = location.get("wg_config_path") or os.environ.get("VPN_LEAKS_WG_CONFIG")
        if not conf:
            raise RuntimeError(
                "WireGuardAdapter: set location.wg_config_path or VPN_LEAKS_WG_CONFIG",
            )
        path = Path(conf).expanduser()
        if not path.is_file():
            raise FileNotFoundError(path)
        iface = location.get("wg_interface") or path.stem
        self._iface = iface
        cmd = ["wg-quick", "up", str(path)]
        print(f"[wireguard] {' '.join(cmd)}", file=sys.stderr)
        subprocess.run(cmd, check=True)

    def disconnect(self) -> None:
        if not self._iface:
            return
        cmd = ["wg-quick", "down", self._iface]
        print(f"[wireguard] {' '.join(cmd)}", file=sys.stderr)
        subprocess.run(cmd, check=False)
        self._iface = None
