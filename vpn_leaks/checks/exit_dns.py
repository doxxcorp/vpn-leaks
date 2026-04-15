"""Reverse DNS (PTR) lookups for exit addresses."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _ptr_for_ip(ip: str) -> dict[str, Any]:
    from dns import reversename
    from dns.exception import DNSException
    from dns.rdatatype import RdataType
    from dns.resolver import Resolver

    out: dict[str, Any] = {"ip": ip, "ptr": [], "error": None}
    try:
        rev = reversename.from_address(ip)
    except Exception as e:
        out["error"] = f"reversename: {e}"
        return out

    res = Resolver()
    res.timeout = 5
    res.lifetime = 10
    try:
        ans = res.resolve(rev, RdataType.PTR)
        out["ptr"] = sorted({str(r.target).rstrip(".").lower() for r in ans})
    except DNSException as e:
        out["error"] = str(e)[:400]
    return out


def write_exit_dns_json(
    *,
    raw_dir: Path,
    exit_ip_v4: str | None,
    exit_ip_v6: str | None,
) -> dict[str, Any]:
    """
    Write raw/<loc>/exit_dns.json with PTR for v4 and v6 when present.
    """
    raw_dir.mkdir(parents=True, exist_ok=True)
    payload: dict[str, Any] = {
        "ptr_v4": None,
        "ptr_v6": None,
    }
    if exit_ip_v4:
        payload["ptr_v4"] = _ptr_for_ip(exit_ip_v4)
    if exit_ip_v6:
        payload["ptr_v6"] = _ptr_for_ip(exit_ip_v6)

    path = raw_dir / "exit_dns.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
