"""HAR aggregation helpers."""

from __future__ import annotations

import json
from pathlib import Path

from vpn_leaks.checks.har_summary import summarize_competitor_har_paths, summarize_har_file


def test_summarize_har_minimal(tmp_path: Path) -> None:
    har = {
        "log": {
            "entries": [
                {
                    "request": {
                        "url": "https://www.googletagmanager.com/gtag/js?id=G-1",
                    },
                },
                {
                    "request": {
                        "url": "https://cdn.example.com/app.js",
                    },
                },
            ],
        },
    }
    p = tmp_path / "t.har"
    p.write_text(json.dumps(har), encoding="utf-8")
    s = summarize_har_file(p)
    assert s["entry_count"] == 2
    assert "www.googletagmanager.com" in s["unique_hosts"]
    assert s["tracker_candidates"]


def test_summarize_merged(tmp_path: Path) -> None:
    har = {"log": {"entries": [{"request": {"url": "https://a.test/x"}}]}}
    p = tmp_path / "a.har"
    p.write_text(json.dumps(har), encoding="utf-8")
    m = summarize_competitor_har_paths([p])
    assert "a.test" in m["merged_unique_hosts"]
