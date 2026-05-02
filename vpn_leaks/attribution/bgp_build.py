"""Download a Route Views MRT RIB dump and build a SQLite BGP prefix database."""

from __future__ import annotations

import ipaddress
import re
import sqlite3
import tempfile
import time
from pathlib import Path
from typing import Any

import httpx

_ROUTEVIEWS_BASE = "https://archive.routeviews.org/route-views2/bgpdata"
_BATCH_SIZE = 10_000
_DOWNLOAD_TIMEOUT_S = 600  # full RIB ~100-200 MB


def _latest_rib_url(base: str = _ROUTEVIEWS_BASE) -> str:
    """Scrape the Route Views archive index for the most recent rib.*.bz2 URL."""
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    candidates = [
        (now.year, now.month),
        (now.year if now.month > 1 else now.year - 1, now.month - 1 if now.month > 1 else 12),
    ]
    for y, m in candidates:
        url = f"{base}/{y}.{m:02d}/RIBS/"
        try:
            resp = httpx.get(url, timeout=30, follow_redirects=True)
        except Exception:
            continue
        if resp.status_code != 200:
            continue
        files = sorted(set(re.findall(r"rib\.\d{8}\.\d{4}\.bz2", resp.text)))
        if files:
            return f"{url}{files[-1]}"
    raise RuntimeError(
        "Could not locate latest RIB at Route Views archive. "
        "Try passing --url manually."
    )


def _extract_as_path(rib_entries: list[Any]) -> list[str]:
    """Return flat ASN string list from the first rib entry's AS_PATH attribute."""
    for entry in rib_entries[:1]:
        for attr in entry.get("path_attributes", []):
            # AS_PATH type key = 2 (integer)
            if 2 in attr.get("type", {}):
                flat: list[str] = []
                for seg in attr.get("value", []):
                    # AS_SEQUENCE type key = 2; skip AS_SET (key 1)
                    if 2 in seg.get("type", {}):
                        flat.extend(str(a) for a in seg.get("value", []))
                return flat
    return []


def build_bgp_db(
    db_path: Path,
    *,
    rib_url: str | None = None,
    rib_file: Path | None = None,
    base_url: str = _ROUTEVIEWS_BASE,
    progress: bool = True,
) -> dict[str, Any]:
    """
    Download a Route Views RIB and build a SQLite BGP prefix lookup database.

    Returns summary: {prefix_count, db_path, db_size_mb, source_url, elapsed_s}
    """
    try:
        import mrtparse  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "mrtparse is required: pip install mrtparse"
        ) from exc

    import mrtparse

    db_path.parent.mkdir(parents=True, exist_ok=True)
    t_start = time.time()

    if rib_file:
        source_url = str(rib_file.resolve())
        tmp_path = rib_file
        own_tmp = False
    else:
        url = rib_url or _latest_rib_url(base_url)
        source_url = url
        if progress:
            print(f"[bgp-update] Downloading {url} …")
        with (
            tempfile.NamedTemporaryFile(suffix=".bz2", delete=False) as tmp,
            httpx.stream(
                "GET", url, timeout=_DOWNLOAD_TIMEOUT_S, follow_redirects=True
            ) as resp,
        ):
            resp.raise_for_status()
            total = int(resp.headers.get("content-length", 0))
            downloaded = 0
            for chunk in resp.iter_bytes(chunk_size=1024 * 512):
                tmp.write(chunk)
                downloaded += len(chunk)
                if progress and total:
                    pct = downloaded / total * 100
                    print(f"\r  {downloaded / 1e6:.1f}/{total / 1e6:.0f} MB ({pct:.0f}%)", end="")
            tmp_path = Path(tmp.name)
            own_tmp = True
        if progress:
            print(f"\r  {downloaded / 1e6:.1f} MB downloaded.")

    if progress:
        print("[bgp-update] Parsing MRT entries …")

    try:
        if db_path.exists():
            db_path.unlink()

        conn = sqlite3.connect(str(db_path))
        conn.execute("""
            CREATE TABLE bgp_prefixes (
                net_start  INTEGER NOT NULL,
                net_end    INTEGER NOT NULL,
                prefix_len INTEGER NOT NULL,
                origin_asn TEXT    NOT NULL,
                as_path    TEXT    NOT NULL
            )
        """)
        conn.execute("CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT)")

        batch: list[tuple[int, int, int, str, str]] = []
        prefix_count = 0

        for entry in mrtparse.Reader(str(tmp_path)):
            data = entry.data
            subtype = data.get("subtype", {})
            # 2 = RIB_IPV4_UNICAST
            if 2 not in subtype:
                continue

            prefix_str = data.get("prefix")
            # mrtparse stores prefix length in data["length"] for TABLE_DUMP_V2
            prefix_len = data.get("length")
            if not prefix_str or prefix_len is None:
                continue

            try:
                net = ipaddress.IPv4Network(f"{prefix_str}/{prefix_len}", strict=False)
            except (ValueError, TypeError):
                continue

            rib_entries = data.get("rib_entries") or []
            as_path = _extract_as_path(rib_entries)
            if not as_path:
                continue

            batch.append((
                int(net.network_address),
                int(net.broadcast_address),
                int(prefix_len),
                f"AS{as_path[-1]}",
                " ".join(as_path),
            ))
            prefix_count += 1

            if len(batch) >= _BATCH_SIZE:
                conn.executemany("INSERT INTO bgp_prefixes VALUES (?, ?, ?, ?, ?)", batch)
                batch.clear()
                if progress:
                    print(f"\r  {prefix_count:,} prefixes …", end="")

        if batch:
            conn.executemany("INSERT INTO bgp_prefixes VALUES (?, ?, ?, ?, ?)", batch)

        if progress:
            print(f"\r  {prefix_count:,} prefixes parsed; building index …")

        conn.execute("CREATE INDEX idx_range ON bgp_prefixes(net_end, net_start)")
        conn.execute("ANALYZE")
        conn.commit()  # VACUUM must run outside a transaction
        conn.execute("VACUUM")

        built_at = time.time()
        conn.executemany("INSERT INTO meta VALUES (?, ?)", [
            ("source_url", source_url),
            ("prefix_count", str(prefix_count)),
            ("built_at", str(built_at)),
        ])
        conn.commit()
        conn.close()

    finally:
        if own_tmp:
            tmp_path.unlink(missing_ok=True)

    db_size_mb = db_path.stat().st_size / 1e6
    elapsed = time.time() - t_start
    if progress:
        print(
            f"[bgp-update] Done: {prefix_count:,} prefixes → {db_path} "
            f"({db_size_mb:.0f} MB, {elapsed:.0f}s)"
        )

    return {
        "prefix_count": prefix_count,
        "db_path": str(db_path),
        "db_size_mb": db_size_mb,
        "source_url": source_url,
        "elapsed_s": elapsed,
    }
