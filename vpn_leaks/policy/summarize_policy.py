"""Heuristic policy summarization (keyword sections)."""

from __future__ import annotations

import re
from pathlib import Path

_KEYWORDS = [
    ("retention", re.compile(r"retention|retain|stored for", re.I)),
    ("logging", re.compile(r"log|logging|traffic", re.I)),
    ("law enforcement", re.compile(r"law enforcement|subpoena|government", re.I)),
    ("third parties", re.compile(r"third party|share|disclose", re.I)),
    ("telemetry", re.compile(r"telemetry|diagnostic|analytics", re.I)),
]


def summarize_html(html_path: Path) -> list[str]:
    text = html_path.read_text(encoding="utf-8", errors="replace")
    # crude de-tag
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    bullets: list[str] = []
    for label, pat in _KEYWORDS:
        if pat.search(text):
            bullets.append(f"Mentions {label} (keyword hit; review source)")
    if not bullets:
        bullets.append("No keyword hits for common sections; manual review recommended")
    return bullets[:20]
