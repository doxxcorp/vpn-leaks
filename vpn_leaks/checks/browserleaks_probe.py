"""Pinned browserleaks.com pages: HAR + per-page title/status/text excerpt."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vpn_leaks.config_loader import repo_root

TEXT_EXCERPT_MAX = 3500


def run_browserleaks_probe(
    *,
    leak_cfg: dict[str, Any],
    raw_dir: Path,
    services_contacted: list[str],
    skip: bool,
) -> dict[str, Any] | None:
    """
    Optional multi-page load from configs/tools/leak-tests.yaml under `browserleaks_probe`.
    Skip with --skip-browserleaks.
    """
    if skip:
        return None

    bl = leak_cfg.get("browserleaks_probe") or {}
    if not isinstance(bl, dict) or not bl.get("enabled", True):
        return None

    urls = [str(u) for u in (bl.get("urls") or []) if u]
    if not urls:
        return None

    probe_dir = raw_dir / "browserleaks_probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    har_path = probe_dir / "browserleaks.har"
    services_contacted.append("browserleaks.com:playwright_chromium")

    snapshot: dict[str, Any] = {
        "pages": [],
        "har_path": str(har_path.relative_to(repo_root())),
        "error": None,
    }

    from playwright.sync_api import sync_playwright

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = None
            try:
                context = browser.new_context(record_har_path=str(har_path))
                page = context.new_page()
                for url in urls:
                    services_contacted.append(url.split("?")[0])
                    row: dict[str, Any] = {
                        "url": url,
                        "final_url": None,
                        "status": None,
                        "title": None,
                        "text_excerpt": None,
                        "text_excerpt_truncated": False,
                        "cdn_headers": {},
                        "error": None,
                    }
                    try:
                        resp = page.goto(url, wait_until="domcontentloaded", timeout=60000)
                        page.wait_for_timeout(2000)
                        try:
                            page.wait_for_load_state("networkidle", timeout=12000)
                        except Exception:
                            pass
                        if resp:
                            row["status"] = resp.status
                            row["final_url"] = resp.url
                            h = {k.lower(): v for k, v in resp.headers.items()}
                            for key in ("server", "cf-ray", "via", "x-cache", "x-served-by"):
                                if key in h:
                                    row["cdn_headers"][key] = h[key]
                        row["title"] = page.title()
                        text = page.evaluate(
                            "() => (document.body && document.body.innerText) || ''",
                        )
                        raw_text = text or ""
                        if len(raw_text) > TEXT_EXCERPT_MAX:
                            row["text_excerpt"] = raw_text[:TEXT_EXCERPT_MAX]
                            row["text_excerpt_truncated"] = True
                        else:
                            row["text_excerpt"] = raw_text
                    except Exception as e:
                        row["error"] = str(e)[:500]
                    snapshot["pages"].append(row)
            finally:
                if context is not None:
                    context.close()
                browser.close()
    except Exception as e:
        snapshot["error"] = str(e)[:500]

    out_json = probe_dir / "browserleaks.json"
    out_json.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return snapshot
