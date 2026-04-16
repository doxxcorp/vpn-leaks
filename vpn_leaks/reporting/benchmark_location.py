"""Compact display labels for benchmark locations: City, ST, CCC (ISO-3166-1 alpha-3)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from vpn_leaks.config_loader import repo_root

# US state / territory full names (as in geo APIs) -> USPS code.
_US_STATE_NAME_TO_CODE: dict[str, str] = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "district of columbia": "DC",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
    "american samoa": "AS",
    "guam": "GU",
    "northern mariana islands": "MP",
    "puerto rico": "PR",
    "us virgin islands": "VI",
    "virgin islands": "VI",
}

# English country names often seen in vpn_location_label / geo APIs -> ISO 3166-1 alpha-2.
_COUNTRY_NAME_TO_A2: dict[str, str] = {
    "united states": "US",
    "united states of america": "US",
    "usa": "US",
    "united kingdom": "GB",
    "great britain": "GB",
    "uk": "GB",
    "england": "GB",
    "scotland": "GB",
    "wales": "GB",
    "northern ireland": "GB",
    "germany": "DE",
    "france": "FR",
    "japan": "JP",
    "canada": "CA",
    "australia": "AU",
    "netherlands": "NL",
    "the netherlands": "NL",
    "spain": "ES",
    "italy": "IT",
    "sweden": "SE",
    "norway": "NO",
    "denmark": "DK",
    "finland": "FI",
    "switzerland": "CH",
    "austria": "AT",
    "belgium": "BE",
    "poland": "PL",
    "brazil": "BR",
    "mexico": "MX",
    "india": "IN",
    "singapore": "SG",
    "hong kong": "HK",
    "taiwan": "TW",
    "south korea": "KR",
    "korea": "KR",
    "israel": "IL",
    "ireland": "IE",
    "new zealand": "NZ",
    "czech republic": "CZ",
    "czechia": "CZ",
    "portugal": "PT",
    "romania": "RO",
    "hungary": "HU",
    "turkey": "TR",
    "russia": "RU",
    "ukraine": "UA",
    "south africa": "ZA",
    "argentina": "AR",
    "chile": "CL",
    "colombia": "CO",
}


@lru_cache(maxsize=1)
def _alpha2_to_alpha3_map() -> dict[str, str]:
    path = repo_root() / "configs" / "geo" / "iso3166_alpha2_to_alpha3.json"
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, dict):
        return {}
    return {str(k).upper(): str(v).upper() for k, v in raw.items()}


def _alpha2_to_alpha3(alpha2: str) -> str:
    cc = alpha2.strip().upper()
    if len(cc) != 2:
        return cc or "?"
    m = _alpha2_to_alpha3_map()
    return m.get(cc, cc)


def _us_state_code(region: str) -> str:
    key = region.strip().lower()
    if key in _US_STATE_NAME_TO_CODE:
        return _US_STATE_NAME_TO_CODE[key]
    u = region.strip().upper()
    if len(u) == 2 and u.isalpha():
        return u
    return _region_token_two_letter(region)


def _region_token_two_letter(region: str) -> str:
    """Non-US: best-effort 2-letter token from region name (not an official subdivision code)."""
    s = "".join(ch for ch in region if ch.isalnum() or ch.isspace())
    parts = s.split()
    if not parts:
        return "??"
    tok = parts[0]
    letters = "".join(c for c in tok if c.isalpha())
    if len(letters) >= 2:
        return letters[:2].upper()
    return (letters + "??")[:2].upper()


def _country_name_to_alpha2(name: str) -> str | None:
    k = name.strip().lower()
    if k in _COUNTRY_NAME_TO_A2:
        return _COUNTRY_NAME_TO_A2[k]
    if len(k) == 2 and k.isalpha():
        return k.upper()
    return None


def _format_from_geo(geo: dict[str, Any]) -> str | None:
    city = str(geo.get("city") or "").strip()
    region = str(geo.get("region") or "").strip()
    cc2 = str(geo.get("country_code") or "").strip().upper()
    if len(cc2) != 2 or not cc2.isalpha():
        return None
    c3 = _alpha2_to_alpha3(cc2)
    if not city:
        return None
    if cc2 == "US":
        mid = _us_state_code(region) if region else "??"
    else:
        mid = _region_token_two_letter(region) if region else cc2
    return f"{city}, {mid}, {c3}"


def _format_from_label(label: str) -> str:
    raw = " ".join(label.split())
    if not raw:
        return ""
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) >= 3:
        city, region, country_s = parts[0], parts[1], parts[2]
        cc2 = _country_name_to_alpha2(country_s)
        if not cc2:
            cc2 = _country_name_to_alpha2(country_s.split()[0]) if country_s.split() else None
        c3 = _alpha2_to_alpha3(cc2) if cc2 else "???"
        if cc2 == "US":
            mid = _us_state_code(region)
        else:
            mid = _region_token_two_letter(region) if region else (cc2 or "??")
        return f"{city}, {mid}, {c3}"
    if len(parts) == 2:
        city, country_s = parts[0], parts[1]
        cc2 = _country_name_to_alpha2(country_s)
        if cc2:
            c3 = _alpha2_to_alpha3(cc2)
            return f"{city}, {cc2}, {c3}"
        return f"{city}, {country_s}"
    return raw


def format_benchmark_location_display(data: dict[str, Any]) -> str:
    """
    Return a short single-line label: City, ST, CCC (ISO-3166-1 alpha-3).

    Prefer structured ``extra.exit_geo``; otherwise parse ``vpn_location_label``.
    Non-US middle token is a best-effort 2-letter token from the region field, not
    necessarily an official ISO-3166-2 code.
    """
    extra = data.get("extra")
    if isinstance(extra, dict):
        geo = extra.get("exit_geo")
        if isinstance(geo, dict):
            s = _format_from_geo(geo)
            if s:
                return s
    label = str(data.get("vpn_location_label") or data.get("vpn_location_id") or "").strip()
    if not label:
        return ""
    return _format_from_label(label)

