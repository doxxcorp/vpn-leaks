"""RIPEstat Data API — prefix overview / related prefixes."""

from __future__ import annotations

from typing import Any

import httpx


def prefix_overview(resource: str, base_url: str) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/prefix-overview/data.json"
    params = {"resource": resource}
    with httpx.Client(timeout=30.0) as client:
        r = client.get(url, params=params)
        r.raise_for_status()
        return r.json()


def announced_prefixes(resource_asn: str, base_url: str) -> dict[str, Any]:
    """
    RIPEstat announced-prefixes for an ASN, e.g. resource_asn='AS15169'.
    https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS15169
    """
    url = f"{base_url.rstrip('/')}/announced-prefixes/data.json"
    params = {"resource": resource_asn}
    with httpx.Client(timeout=45.0) as client:
        r = client.get(url, params=params)
        r.raise_for_status()
        return r.json()


def announced_prefix_strings(data: dict[str, Any], *, limit: int = 2000) -> list[str]:
    """Flatten RIPEstat announced-prefixes JSON to sorted unique CIDR strings."""
    out: list[str] = []
    try:
        block = (data.get("data") or {}).get("prefixes") or []
        for row in block:
            if not isinstance(row, dict):
                continue
            p = row.get("prefix")
            if isinstance(p, str) and p:
                out.append(p)
    except (TypeError, KeyError):
        pass
    uniq = sorted(set(out))
    return uniq[:limit]


def extract_asn_holder(data: dict[str, Any]) -> tuple[int | None, str | None, str | None]:
    """Best-effort from prefix-overview JSON."""
    try:
        block = data.get("data") or {}
        rows = block.get("asns") or block.get("prefixes") or []
        if isinstance(rows, dict):
            rows = [rows]
        if not rows:
            return None, None, None
        first = rows[0] if isinstance(rows[0], dict) else {}
        asn = int(first.get("asn")) if first.get("asn") is not None else None
        holder = first.get("holder") or first.get("name")
        return asn, holder, None
    except (KeyError, TypeError, ValueError):
        return None, None, None
