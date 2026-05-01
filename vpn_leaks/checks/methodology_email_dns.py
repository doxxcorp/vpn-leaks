"""Pure TXT parsing helpers for methodology Phase 8 (unit-tested)."""

from __future__ import annotations

import re
from typing import Any

DMARC_KV_RE = re.compile(r"([a-z]{1,14})=([^;\s]+(?:\s+[^;\s]+)*)", re.IGNORECASE)


def parse_dmarc_aggregate_record(joined_txt: str) -> dict[str, str | None]:
    """Extract common DMARC tags from one logical TXT record (joined chunks)."""
    out: dict[str, str | None] = {"p": None, "sp": None, "pct": None, "rua": None}
    if "v=dmarc1" not in joined_txt.lower():
        return out
    for m in DMARC_KV_RE.finditer(joined_txt):
        tag = m.group(1).lower().strip()
        val = m.group(2).strip().strip('"')
        if tag in out:
            out[tag] = val
    return out


def summarize_spf_mechanisms(spf_flat: str) -> dict[str, Any]:
    """Non-DNS SPF token scan (supports unit tests independent of resolver)."""
    low = spf_flat.lower()
    includes: list[str] = []
    redirects: list[str] = []
    if "v=spf1" not in low and not low.startswith("v=spf1"):
        pass
    for token in low.replace(";", " ").split():
        if token.startswith("include:"):
            includes.append(token.split(":", 1)[1].strip().rstrip(".").lower())
        if token.startswith("redirect="):
            redirects.append(token.split("=", 1)[1].strip().rstrip(".").lower())
    return {
        "include": sorted(set(includes)),
        "redirect": sorted(set(redirects)),
    }
