"""Optional lightweight fingerprint snapshot (navigator + UA only by default)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def run_fingerprint_snapshot(
    *,
    raw_dir: Path,
    leak_cfg: dict[str, Any],
    services_contacted: list[str],
) -> dict[str, Any]:
    fcfg = leak_cfg.get("fingerprint") or {}
    if not fcfg.get("enabled", False):
        return {}

    from playwright.sync_api import sync_playwright

    raw_dir.mkdir(parents=True, exist_ok=True)
    services_contacted.append("fingerprint:playwright_navigator")

    snap: dict[str, Any] = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            snap = page.evaluate(
                """() => ({
  userAgent: navigator.userAgent,
  language: navigator.language,
  hardwareConcurrency: navigator.hardwareConcurrency,
  platform: navigator.platform,
})""",
            )
        finally:
            browser.close()

    (raw_dir / "fingerprint.json").write_text(json.dumps(snap, indent=2), encoding="utf-8")
    return snap
