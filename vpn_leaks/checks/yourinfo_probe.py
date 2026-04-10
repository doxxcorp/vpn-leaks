"""Load yourinfo.ai in Playwright; capture HAR, title, text excerpt.

There is no stable public JSON API for this site.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from vpn_leaks.config_loader import repo_root

YOURINFO_DEFAULT_URL = "https://yourinfo.ai/"

TEXT_EXCERPT_MAX = 4000


def run_yourinfo_probe(
    *,
    raw_dir: Path,
    services_contacted: list[str],
    skip: bool,
) -> dict[str, Any] | None:
    """
    Always-on third-party benchmark page (Doxx YourInfo demo). Skip with --skip-yourinfo.
    Writes raw/<loc>/yourinfo_probe/yourinfo.json and yourinfo.har.
    """
    if skip:
        return None

    probe_dir = raw_dir / "yourinfo_probe"
    probe_dir.mkdir(parents=True, exist_ok=True)
    har_path = probe_dir / "yourinfo.har"
    services_contacted.append("yourinfo.ai:playwright_chromium")

    snapshot: dict[str, Any] = {
        "url": YOURINFO_DEFAULT_URL,
        "final_url": None,
        "status": None,
        "title": None,
        "text_excerpt": None,
        "text_excerpt_truncated": False,
        "har_path": str(har_path.relative_to(repo_root())),
        "cdn_headers": {},
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
                resp = page.goto(
                    YOURINFO_DEFAULT_URL,
                    wait_until="domcontentloaded",
                    timeout=60000,
                )
                page.wait_for_timeout(5000)
                try:
                    page.wait_for_load_state("networkidle", timeout=15000)
                except Exception:
                    pass
                if resp:
                    snapshot["status"] = resp.status
                    snapshot["final_url"] = resp.url
                    h = {k.lower(): v for k, v in resp.headers.items()}
                    for key in ("server", "cf-ray", "via", "x-cache", "x-served-by"):
                        if key in h:
                            snapshot["cdn_headers"][key] = h[key]
                snapshot["title"] = page.title()
                text = page.evaluate("() => (document.body && document.body.innerText) || ''")
                raw_text = text or ""
                if len(raw_text) > TEXT_EXCERPT_MAX:
                    snapshot["text_excerpt"] = raw_text[:TEXT_EXCERPT_MAX]
                    snapshot["text_excerpt_truncated"] = True
                else:
                    snapshot["text_excerpt"] = raw_text
            finally:
                if context is not None:
                    context.close()
                browser.close()
    except Exception as e:
        snapshot["error"] = str(e)[:500]

    (probe_dir / "yourinfo.json").write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return snapshot
