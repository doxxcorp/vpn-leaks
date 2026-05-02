"""Offline BGP prefix → ASN lookup from Route Views SQLite database."""

from __future__ import annotations

import ipaddress
import sqlite3
from pathlib import Path
from typing import Any

# Module-level connection cache: keyed by resolved db path string
_db_conn_cache: dict[str, sqlite3.Connection] = {}


def _default_db_path() -> Path:
    from vpn_leaks.config_loader import repo_root

    return repo_root() / ".cache" / "vpn_leaks" / "bgp_prefixes.db"


def _get_conn(db_path: Path) -> sqlite3.Connection | None:
    key = str(db_path.resolve())
    if key not in _db_conn_cache:
        if not db_path.is_file():
            return None
        conn = sqlite3.connect(key, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        _db_conn_cache[key] = conn
    return _db_conn_cache.get(key)


def lookup_ip(ip: str, db_path: str | Path | None = None) -> dict[str, Any]:
    """
    Return BGP origin data for an IPv4 address from the local Route Views database.

    Result keys (when found):
        asn          "AS15169"
        upstream_asn "AS3356"  (transit provider, second-to-last in path), or None
        prefix       "8.8.8.0/24"
        as_path      "3356 15169"  (space-separated, first=ingress, last=origin)
        source       "routeviews_bgp"

    Returns {"source": "bgp_db_unavailable"} when the database has not been built.
    Returns {"source": "private_ip"} for RFC-1918 / loopback / link-local addresses.
    Returns {"source": "bgp_not_found"} when no covering prefix is in the table.
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return {"source": "invalid_ip"}

    if addr.version != 4:
        return {"source": "ipv6_unsupported"}

    if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_reserved:
        return {"source": "private_ip"}

    resolved = Path(db_path).resolve() if db_path else _default_db_path()
    conn = _get_conn(resolved)
    if conn is None:
        return {"source": "bgp_db_unavailable"}

    ip_int = int(addr)
    try:
        row = conn.execute(
            """
            SELECT origin_asn, as_path, prefix_len, net_start
            FROM   bgp_prefixes
            WHERE  net_start <= ? AND net_end >= ?
            ORDER  BY prefix_len DESC
            LIMIT  1
            """,
            (ip_int, ip_int),
        ).fetchone()
    except sqlite3.Error:
        return {"source": "bgp_db_error"}

    if row is None:
        return {"source": "bgp_not_found"}

    origin_asn: str = row["origin_asn"]
    as_path_str: str = row["as_path"]
    prefix_len: int = row["prefix_len"]
    net_start: int = row["net_start"]

    network_addr = str(ipaddress.IPv4Address(net_start))
    prefix = f"{network_addr}/{prefix_len}"

    as_path_asns = as_path_str.split()
    upstream_asn = f"AS{as_path_asns[-2]}" if len(as_path_asns) >= 2 else None

    return {
        "asn": origin_asn,
        "upstream_asn": upstream_asn,
        "prefix": prefix,
        "as_path": as_path_str,
        "source": "routeviews_bgp",
    }


def db_meta(db_path: str | Path | None = None) -> dict[str, str]:
    """Return metadata stored in the BGP database (source URL, prefix count, build time)."""
    resolved = Path(db_path).resolve() if db_path else _default_db_path()
    conn = _get_conn(resolved)
    if conn is None:
        return {}
    try:
        rows = conn.execute("SELECT key, value FROM meta").fetchall()
        return {r["key"]: r["value"] for r in rows}
    except sqlite3.Error:
        return {}
