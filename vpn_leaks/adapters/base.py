"""VPN adapter interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class AdapterCapabilities:
    automated_tunnel: bool = False
    manual_gui_assist: bool = False


class VPNAdapter(ABC):
    slug: str

    @property
    def capabilities(self) -> AdapterCapabilities:
        return AdapterCapabilities()

    @abstractmethod
    def connect(self, location: dict[str, Any]) -> None:
        """Establish VPN for the given location definition from config."""

    @abstractmethod
    def disconnect(self) -> None:
        """Tear down VPN."""

    def status(self) -> dict[str, Any]:
        return {}

    def list_locations(self, vpn_config: dict[str, Any]) -> list[dict[str, Any]]:
        locs = vpn_config.get("locations")
        if isinstance(locs, list):
            return [x for x in locs if isinstance(x, dict)]
        return []
