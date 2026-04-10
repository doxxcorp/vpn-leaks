"""Preflight: exit IP, duplicate-run detection, optional geo-based location id/label."""

from __future__ import annotations

import asyncio
import json
import re
import tempfile
from pathlib import Path
from typing import Any

import httpx

from vpn_leaks.checks.ip_check import run_ip_check
from vpn_leaks.config_loader import repo_root


def _slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "x"


def quick_exit_ip(leak_cfg: dict[str, Any]) -> tuple[str | None, list[str]]:
    """Return (ipv4, services_contacted) using the first configured IP endpoint only."""
    endpoints = leak_cfg.get("ip_endpoints") or [
        {"url": "https://api.ipify.org", "format": "text"},
    ]
    ep = endpoints[0]
    with tempfile.TemporaryDirectory(prefix="vpn-leaks-preflight-") as td:
        tmp = Path(td)
        services: list[str] = []
        _sources, v4, _v6 = asyncio.run(
            run_ip_check(raw_dir=tmp, endpoints=[ep], services_contacted=services),
        )
        return v4, services


def find_prior_run_with_same_exit(
    *,
    vpn_provider: str,
    exit_ip_v4: str,
    runs_root: Path | None = None,
) -> Path | None:
    """Return path to an existing normalized.json with same provider and exit IPv4, if any."""
    root = runs_root or (repo_root() / "runs")
    if not root.is_dir():
        return None
    for run_dir in sorted(root.iterdir()):
        if not run_dir.is_dir():
            continue
        loc_root = run_dir / "locations"
        if not loc_root.is_dir():
            continue
        for norm in loc_root.glob("*/normalized.json"):
            try:
                data = json.loads(norm.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if data.get("vpn_provider") != vpn_provider:
                continue
            if data.get("exit_ip_v4") == exit_ip_v4:
                return norm
    return None


async def _fetch_ipwho(ip: str) -> dict[str, Any]:
    url = f"https://ipwho.is/{ip}"
    async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


def fetch_geo_sync(ip: str) -> dict[str, Any]:
    return asyncio.run(_fetch_ipwho(ip))


def build_location_from_geo(geo: dict[str, Any], exit_ip: str) -> tuple[str, str, dict[str, Any]]:
    """
    Build location id, human label, and a small geo snapshot for ``extra``.

    Id format: ``{cc}-{region}-{city}`` with fallbacks; disambiguate with last octet if needed.
    """
    if not geo.get("success", True):
        tail = exit_ip.split(".")[-1] if "." in exit_ip else exit_ip[-4:]
        lid = f"auto-ip-{tail}"
        return lid, f"exit {exit_ip} (geo lookup failed)", {"ipwho": geo}

    cc = str(geo.get("country_code") or geo.get("country") or "xx").lower()[:2]
    region = str(geo.get("region") or geo.get("continent") or "unknown")
    city = str(geo.get("city") or "unknown")
    last = exit_ip.split(".")[-1] if "." in exit_ip else "x"
    lid = f"{cc}-{_slug(region)}-{_slug(city)}-{last}"
    if len(lid) > 96:
        lid = lid[:96].rstrip("-")

    parts = [city, region, geo.get("country") or geo.get("country_code")]
    label = ", ".join(str(p) for p in parts if p and str(p) not in ("unknown",))

    snapshot = {
        "source": "ipwho.is",
        "ip": geo.get("ip") or exit_ip,
        "country_code": geo.get("country_code"),
        "region": geo.get("region"),
        "city": geo.get("city"),
        "connection": geo.get("connection"),
        "location_id": lid,
        "location_label": label,
    }
    return lid, label or lid, snapshot
