"""Team Cymru origin ASN via DNS TXT (dig) — best effort."""

from __future__ import annotations

import ipaddress
import subprocess
from typing import Any

_CYMRU_DIG_TIMEOUT_S = 15


def ip_to_cymru_domain(ip: str) -> str | None:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return None
    if addr.version != 4:
        return None
    octets = str(addr).split(".")
    return ".".join(reversed(octets)) + ".origin.asn.cymru.com"


def cymru_asn_lookup(ip: str) -> dict[str, Any]:
    domain = ip_to_cymru_domain(ip)
    if not domain:
        return {"error": "IPv6 or invalid IP for Cymru v4 query", "disclaimer": []}

    try:
        proc = subprocess.run(
            ["dig", "+short", "TXT", domain],
            capture_output=True,
            text=True,
            timeout=_CYMRU_DIG_TIMEOUT_S,
            check=False,
        )
    except FileNotFoundError:
        return {
            "error": "dig not found",
            "disclaimer": [
                "Install bind-utils/dnsutils for Team Cymru DNS lookup cross-check.",
            ],
        }
    except subprocess.TimeoutExpired:
        return {
            "error": f"dig timed out after {_CYMRU_DIG_TIMEOUT_S}s",
            "disclaimer": [
                "Team Cymru DNS lookup timed out; cross-check skipped.",
            ],
        }

    out = proc.stdout.strip()
    if not out:
        return {"error": "empty dig response", "raw": proc.stderr}

    # TXT may be quoted
    line = out.splitlines()[0].strip().strip('"')
    parts = [p.strip() for p in line.split("|")]
    asn: int | None = None
    if parts and parts[0].isdigit():
        asn = int(parts[0])
    return {
        "asn": asn,
        "raw_line": line,
        "parts": parts,
        "disclaimer": [
            "Team Cymru notes some upstream inference is imperfect; treat as cross-check.",
        ],
    }
