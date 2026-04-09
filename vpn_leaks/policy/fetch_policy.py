"""Fetch privacy policy HTML and record hashes."""

from __future__ import annotations

import hashlib
from pathlib import Path

import httpx

from vpn_leaks.models import PolicyRecord, utc_now_iso
from vpn_leaks.policy.summarize_policy import summarize_html


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_policies(
    *,
    policy_dir: Path,
    urls: list[str],
    role: str,
    services_contacted: list[str],
) -> list[PolicyRecord]:
    policy_dir.mkdir(parents=True, exist_ok=True)
    out: list[PolicyRecord] = []
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        for i, url in enumerate(urls):
            if not url:
                continue
            services_contacted.append(url)
            try:
                r = client.get(url)
                r.raise_for_status()
                body = r.content
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
