"""Aggregate unique hosts from HAR files; light tracker/CDN classification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

# Substrings on full URL or hostname (lowercased)
_TRACKER_HINTS = frozenset(
    {
        "google-analytics.com",
        "googletagmanager.com",
        "googleadservices.com",
        "doubleclick.net",
        "facebook.net",
        "facebook.com/tr",
        "scorecardresearch.com",
        "hotjar.com",
        "segment.io",
        "segment.com",
        "cdn.segment.com",
        "mixpanel.com",
        "clarity.ms",
        "bat.bing.com",
        "adservice.google",
        "ads.linkedin.com",
        "snap.licdn.com",
        "twitter.com/i/ads",
        "pixel.",
        "/gtag/",
        "/gtm.js",
        "plausible.io",
        "matomo",
        "heap-analytics",
        "cdn-cgi/rum",
    }
)

_CDN_HINTS = frozenset(
    {
        "cloudflare",
        "fastly",
        "akamai",
        "edgekey.net",
        "edgesuite.net",
        "cloudfront.net",
        "amazonaws.com",
        "azureedge.net",
        "cdn.",
        "kxcdn.com",
        "stackpath",
        "incapsula",
        "imperva",
    }
)


def _classify_url(url: str) -> list[str]:
    tags: list[str] = []
    u = url.lower()
    for h in _TRACKER_HINTS:
        if h in u:
            tags.append("tracker_candidate")
            break
    for h in _CDN_HINTS:
        if h in u:
            tags.append("cdn_candidate")
            break
    return tags


def summarize_har_file(har_path: Path) -> dict[str, Any]:
    """Parse one HAR; return hosts, urls sample, and classification hints."""
    out: dict[str, Any] = {
        "har_path": str(har_path),
        "entry_count": 0,
        "unique_hosts": [],
        "unique_schemes": [],
        "tracker_candidates": [],
        "cdn_candidates": [],
        "error": None,
    }
    try:
        data = json.loads(har_path.read_text(encoding="utf-8"))
    except Exception as e:
        out["error"] = str(e)[:300]
        return out

    log = (data or {}).get("log") or {}
    entries = log.get("entries") or []
    out["entry_count"] = len(entries)

    hosts: set[str] = set()
    schemes: set[str] = set()
    trackers: set[str] = set()
    cdns: set[str] = set()

    for ent in entries:
        req = (ent or {}).get("request") or {}
        url = req.get("url") or ""
        if not url:
            continue
        try:
            p = urlparse(url)
        except Exception:
            continue
        if p.scheme:
            schemes.add(p.scheme.lower())
        if p.netloc:
            host = p.netloc.split("@")[-1].lower()
            hosts.add(host)
            for tag in _classify_url(url):
                if tag == "tracker_candidate":
                    trackers.add(host)
                elif tag == "cdn_candidate":
                    cdns.add(host)

    out["unique_hosts"] = sorted(hosts)
    out["unique_schemes"] = sorted(schemes)
    out["tracker_candidates"] = sorted(trackers)
    out["cdn_candidates"] = sorted(cdns)
    return out


def summarize_competitor_har_paths(har_paths: list[Path]) -> dict[str, Any]:
    """Merge summaries for multiple HAR files (e.g. all web probe HARs)."""
    all_hosts: set[str] = set()
    all_trackers: set[str] = set()
    all_cdns: set[str] = set()
    per_file: list[dict[str, Any]] = []
    for hp in har_paths:
        if not hp.is_file():
            continue
        one = summarize_har_file(hp)
        per_file.append(one)
        if one.get("error"):
            continue
        all_hosts.update(one.get("unique_hosts") or [])
        all_trackers.update(one.get("tracker_candidates") or [])
        all_cdns.update(one.get("cdn_candidates") or [])

    return {
        "har_files": per_file,
        "merged_unique_hosts": sorted(all_hosts),
        "merged_tracker_candidates": sorted(all_trackers),
        "merged_cdn_candidates": sorted(all_cdns),
    }
