"""Marketing/portal page loads (SPEC §13.5); HAR + headers via competitor web probes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vpn_leaks.checks.competitor_probes import run_web_probes
from vpn_leaks.checks.har_summary import summarize_competitor_har_paths
from vpn_leaks.config_loader import repo_root


def run_surface_probes(
    vpn_config: dict[str, Any],
    *,
    raw_base: Path,
    services_contacted: list[str],
) -> dict[str, Any] | None:
    """If `surface_urls` is set, run Playwright probes and tag page_type."""
    raw = vpn_config.get("surface_urls")
    if not raw:
        return None

    pairs: list[tuple[str, str]] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                pt = str(item.get("page_type") or "unknown")
                url = str(item.get("url") or "").strip()
                if url:
                    pairs.append((pt, url))
            elif isinstance(item, str) and item.strip():
                pairs.append(("unknown", item.strip()))

    if not pairs:
        return None

    out_dir = raw_base / "surface_probe"
    urls = [u for _, u in pairs]
    rows = run_web_probes(urls, raw_dir=out_dir, services_contacted=services_contacted)
    for i, row in enumerate(rows):
        if i < len(pairs):
            row["page_type"] = pairs[i][0]

    root = repo_root()
    har_paths: list[Path] = []
    for row in rows:
        hp = row.get("har_path")
        if isinstance(hp, str):
            p = root / hp
            if p.is_file():
                har_paths.append(p)

    out: dict[str, Any] = {
        "probes": rows,
        "surface_probe_dir": str(out_dir.relative_to(root)),
    }
    if har_paths:
        out["har_summary"] = summarize_competitor_har_paths(har_paths)
        services_contacted.append("surface_probe:har_summary")
        (out_dir / "har_summary.json").write_text(
            json.dumps(out["har_summary"], indent=2),
            encoding="utf-8",
        )
    return out
