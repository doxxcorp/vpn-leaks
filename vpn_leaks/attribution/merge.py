"""Merge attribution sources with confidence."""

from __future__ import annotations

import ipaddress
import json
from pathlib import Path
from typing import Any

from vpn_leaks.attribution.cymru import cymru_asn_lookup
from vpn_leaks.attribution.geolite_asn import lookup_asn
from vpn_leaks.attribution.peeringdb import net_by_asn
from vpn_leaks.attribution.ripestat import extract_asn_holder, prefix_overview
from vpn_leaks.models import AttributionResult, AttributionSource


def collect_attribution_sources(
    ip: str,
    attr_cfg: dict[str, Any],
) -> tuple[list[AttributionSource], list[str]]:
    """RIPEstat, Team Cymru (IPv4), PeeringDB, GeoLite for one address."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return [], [f"Invalid IP for attribution: {ip!r}"]

    base = (attr_cfg.get("ripestat_base") or "https://stat.ripe.net/data").rstrip("/")
    sources: list[AttributionSource] = []
    disclaimers: list[str] = []

    try:
        ripe_raw = prefix_overview(ip, base)
        asn, holder, _cc = extract_asn_holder(ripe_raw)
        sources.append(
            AttributionSource(
                name="ripestat",
                asn=asn,
                holder=holder,
                raw={"prefix_overview": ripe_raw},
            ),
        )
    except Exception as e:
        sources.append(
            AttributionSource(name="ripestat", raw={"error": str(e)}),
        )

    cymru: dict[str, Any]
    if addr.version == 4:
        cymru = cymru_asn_lookup(ip)
        if cymru.get("disclaimer"):
            disclaimers.extend(cymru["disclaimer"])
        sources.append(AttributionSource(name="team_cymru", asn=cymru.get("asn"), raw=cymru))
    else:
        cymru = {"note": "IPv6: Team Cymru DNS TXT origin lookup not used (v4-only in harness)"}
        sources.append(AttributionSource(name="team_cymru", raw=cymru))

    asn_for_pdb: int | None = next(
        (s.asn for s in sources if s.name == "ripestat" and s.asn is not None),
        None,
    )
    if asn_for_pdb is None and addr.version == 4:
        asn_for_pdb = cymru.get("asn") if isinstance(cymru.get("asn"), int) else None
    if asn_for_pdb is None and addr.version == 6:
        geo_early = lookup_asn(attr_cfg.get("geolite_asn_path"), ip)
        if isinstance(geo_early.get("asn"), int):
            asn_for_pdb = geo_early["asn"]

    if attr_cfg.get("peeringdb_enabled", True) and isinstance(asn_for_pdb, int):
        try:
            pdb = net_by_asn(asn_for_pdb)
            sources.append(AttributionSource(name="peeringdb", raw=pdb))
        except Exception as e:
            sources.append(AttributionSource(name="peeringdb", raw={"error": str(e)}))

    geo = lookup_asn(attr_cfg.get("geolite_asn_path"), ip)
    if not geo.get("skipped"):
        sources.append(AttributionSource(name="geolite_asn", raw=geo))

    return sources, disclaimers


def merge_attribution(
    *,
    exit_ip_v4: str | None,
    attr_cfg: dict[str, Any],
    raw_dir: Path,
) -> AttributionResult:
    raw_dir.mkdir(parents=True, exist_ok=True)

    if not exit_ip_v4:
        return AttributionResult(
            confidence=0.0,
            confidence_notes="No exit IPv4 for attribution",
            disclaimers=["No exit IPv4; ASN mapping skipped"],
        )

    sources, extra_disclaimers = collect_attribution_sources(exit_ip_v4, attr_cfg)

    (raw_dir / "attribution.json").write_text(
        json.dumps([s.model_dump(mode="json") for s in sources], indent=2),
        encoding="utf-8",
    )

    result = _score(sources, exit_ip_v4)
    result.disclaimers = list(result.disclaimers) + extra_disclaimers
    return result


def merge_attribution_for_ip(
    ip: str,
    attr_cfg: dict[str, Any],
    *,
    role: str = "provider_ns_glue",
) -> AttributionResult:
    """
    Attribution for an arbitrary IP (e.g. DNS NS glue). Does not write `attribution.json`
    under the location raw dir (distinct from tunnel exit attribution).
    """
    sources, extra_disclaimers = collect_attribution_sources(ip, attr_cfg)
    result = _score(sources, ip)
    result.disclaimers = list(result.disclaimers) + extra_disclaimers
    prefix = f"[{role}] "
    result.confidence_notes = (
        prefix + (result.confidence_notes or "attribution")
        if result.confidence_notes
        else prefix + "attribution"
    )
    return result


def _score(sources: list[AttributionSource], ip: str) -> AttributionResult:
    asns = [s.asn for s in sources if s.asn is not None]
    holders = [s.holder for s in sources if s.holder]
    uniq_asn = sorted(set(asns))
    confidence = 0.7 if len(uniq_asn) == 1 and uniq_asn else 0.4
    if len(uniq_asn) > 1:
        confidence = 0.35
    notes = f"ASNs seen: {uniq_asn}" if uniq_asn else "No consistent ASN"
    holder = holders[0] if holders else None
    return AttributionResult(
        asn=uniq_asn[0] if len(uniq_asn) == 1 else (uniq_asn[0] if uniq_asn else None),
        holder=holder,
        confidence=confidence,
        confidence_notes=notes,
        supporting_sources=sources,
        disclaimers=[
            "Upstream/peering inference can be imperfect; see Team Cymru and RIPEstat docs.",
        ],
    )
