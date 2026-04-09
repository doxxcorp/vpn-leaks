"""PeeringDB network lookup by ASN."""

from __future__ import annotations

from typing import Any

import httpx


def net_by_asn(asn: int) -> dict[str, Any]:
    url = "https://www.peeringdb.com/api/net"
    with httpx.Client(timeout=30.0) as client:
        r = client.get(url, params={"asn": asn})
        r.raise_for_status()
        return r.json()
