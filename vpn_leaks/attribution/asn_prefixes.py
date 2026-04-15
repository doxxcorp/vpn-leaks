"""RIPEstat announced prefixes per ASN with simple file cache."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from vpn_leaks.attribution.ripestat import announced_prefix_strings, announced_prefixes
from vpn_leaks.config_loader import repo_root


def _cache_path(asn: int) -> Path:
    base = repo_root() / ".cache" / "vpn_leaks" / "ripestat"
    base.mkdir(parents=True, exist_ok=True)
    return base / f"announced_prefixes_as{asn}.json"


def fetch_announced_prefixes_cached(
    asn: int,
    attr_cfg: dict[str, Any],
) -> dict[str, Any]:
    """
    Return { prefixes: [...], raw: {...}, cache_hit: bool, fetched_epoch: float, error?: str }.
    """
    ttl_sec = float(attr_cfg.get("announced_prefixes_cache_ttl_sec") or 86400)
    base = (attr_cfg.get("ripestat_base") or "https://stat.ripe.net/data").rstrip("/")

    cp = _cache_path(asn)
    now = time.time()
    if cp.is_file():
        try:
            prev = json.loads(cp.read_text(encoding="utf-8"))
            ts = float(prev.get("fetched_epoch") or 0)
            if now - ts < ttl_sec and prev.get("prefixes"):
                return {
                    "asn": asn,
                    "prefixes": prev.get("prefixes") or [],
                    "raw": prev.get("raw"),
                    "cache_hit": True,
                    "fetched_epoch": ts,
                    "source": "ripestat_announced_prefixes",
                }
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

    resource = f"AS{asn}"
    try:
        raw = announced_prefixes(resource, base)
        plist = announced_prefix_strings(raw)
    except Exception as e:
        return {
            "asn": asn,
            "prefixes": [],
            "raw": None,
            "cache_hit": False,
            "fetched_epoch": now,
            "source": "ripestat_announced_prefixes",
            "error": str(e)[:500],
        }

    payload = {
        "asn": asn,
        "prefixes": plist,
        "raw": raw,
        "fetched_epoch": now,
        "source": "ripestat_announced_prefixes",
    }
    try:
        cp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    except OSError:
        pass

    return {
        "asn": asn,
        "prefixes": plist,
        "raw": raw,
        "cache_hit": False,
        "fetched_epoch": now,
        "source": "ripestat_announced_prefixes",
    }
