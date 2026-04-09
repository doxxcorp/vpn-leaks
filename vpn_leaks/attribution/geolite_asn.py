"""Optional MaxMind GeoLite2 ASN (offline)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def lookup_asn(mmdb_path: str | None, ip: str) -> dict[str, Any]:
    if not mmdb_path:
        return {"skipped": True, "reason": "geolite_asn_path not set"}
    path = Path(mmdb_path).expanduser()
    if not path.is_file():
        return {"error": f"mmdb not found: {path}"}

    try:
        import geoip2.database
    except ImportError:
        return {"error": "geoip2 package not installed; pip install geoip2"}

    with geoip2.database.Reader(str(path)) as reader:
        rec = reader.asn(ip)
        return {
            "asn": rec.autonomous_system_number,
            "organization": rec.autonomous_system_organization,
        }
