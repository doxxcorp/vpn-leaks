"""Fetch privacy policy HTML and record hashes."""

from __future__ import annotations

import hashlib
from pathlib import Path

import httpx

from vpn_leaks.models import PolicyRecord, utc_now_iso
from vpn_leaks.policy.summarize_policy import summarize_html

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Cloudflare interstitial / challenge pages (plain httpx gets HTML but not the policy).
_CF_MARKERS = (
    b"Just a moment",
    b"cf-browser-verification",
    b"/cdn-cgi/challenge-platform/",
)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _looks_like_cloudflare_challenge(body: bytes) -> bool:
    return any(m in body for m in _CF_MARKERS)


def _needs_playwright_for_spa(url: str, body: bytes) -> bool:
    """Detect JS-heavy pages where the static HTML shell omits policy text (e.g. Nord Account)."""
    if "my.nordaccount.com" not in url:
        return False
    return len(body) < 80_000


def _fetch_policy_playwright(url: str, *, services_contacted: list[str]) -> bytes:
    services_contacted.append("policy:playwright_chromium")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            if "my.nordaccount.com" in url:
                page.wait_for_load_state("networkidle", timeout=90_000)
            else:
                try:
                    page.wait_for_load_state("networkidle", timeout=30_000)
                except Exception:
                    page.wait_for_timeout(8000)
            return page.content().encode("utf-8")
        finally:
            browser.close()


def fetch_policies(
    *,
    policy_dir: Path,
    urls: list[str],
    role: str,
    services_contacted: list[str],
) -> list[PolicyRecord]:
    policy_dir.mkdir(parents=True, exist_ok=True)
    out: list[PolicyRecord] = []
    with httpx.Client(
        timeout=60.0,
        follow_redirects=True,
        headers=_BROWSER_HEADERS,
    ) as client:
        for i, url in enumerate(urls):
            if not url:
                continue
            services_contacted.append(url)
            try:
                body: bytes | None = None
                r = client.get(url)
                cand = r.content
                if (
                    r.is_success
                    and not _looks_like_cloudflare_challenge(cand)
                    and not _needs_playwright_for_spa(url, cand)
                ):
                    body = cand
                if body is None:
                    body = _fetch_policy_playwright(url, services_contacted=services_contacted)

                h = _sha256_bytes(body)
                fname = f"{role}_{i}.html"
                fpath = policy_dir / fname
                fpath.write_bytes(body)
                bullets = summarize_html(fpath)
                out.append(
                    PolicyRecord(
                        role=role,
                        url=url,
                        fetched_at_utc=utc_now_iso(),
                        sha256=h,
                        summary_bullets=bullets,
                    ),
                )
            except Exception as e:
                out.append(
                    PolicyRecord(
                        role=role,
                        url=url,
                        fetched_at_utc=utc_now_iso(),
                        summary_bullets=[f"fetch error: {e}"],
                    ),
                )
    return out
