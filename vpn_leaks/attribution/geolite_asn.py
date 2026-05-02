"""Optional MaxMind GeoLite2 ASN and City lookups (offline)."""

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


def lookup_city(mmdb_path: str | None, ip: str) -> dict[str, Any]:
    """
    Return country/region/city from GeoLite2-City.mmdb.

    Result keys: country_iso, country_name, subdivision, city
    Returns {"skipped": True} when path not configured or file missing.
    """
    if not mmdb_path:
        return {"skipped": True, "reason": "geolite_city_path not set"}
    path = Path(mmdb_path).expanduser()
    if not path.is_file():
        return {"error": f"mmdb not found: {path}"}

    try:
        import geoip2.database
        import geoip2.errors
    except ImportError:
        return {"error": "geoip2 package not installed; pip install geoip2"}

    try:
        with geoip2.database.Reader(str(path)) as reader:
            rec = reader.city(ip)
            return {
                "country_iso": rec.country.iso_code or "—",
                "country_name": rec.country.name or "—",
                "subdivision": (rec.subdivisions.most_specific.name or "—"),
                "city": rec.city.name or "—",
            }
    except geoip2.errors.AddressNotFoundError:
        return {"error": "address_not_found"}
    except Exception as exc:
        return {"error": str(exc)}
