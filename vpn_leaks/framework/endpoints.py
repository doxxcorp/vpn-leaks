"""Extract hosts from normalized run and apply classification rules."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from vpn_leaks.models import EvidenceRef, NormalizedRun, ObservedEndpoint


def _host_from_url(url: str) -> str | None:
    u = url.strip()
    if not u:
        return None
    if "://" not in u and "/" in u:
        return None
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", u):
        u = "https://" + u
    try:
        p = urlparse(u)
    except ValueError:
        return None
    host = (p.hostname or "").lower().rstrip(".")
    return host or None


def _iter_hosts_services_contacted(run: NormalizedRun) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for u in run.services_contacted:
        h = _host_from_url(str(u))
        if h:
            out.append((h, "services_contacted"))
    return out


def _iter_hosts_web_probes(run: NormalizedRun) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    cs = run.competitor_surface
    if not cs:
        return out
    for row in cs.web_probes or []:
        if not isinstance(row, dict):
            continue
        url = row.get("url") or row.get("final_url")
        if url:
            h = _host_from_url(str(url))
            if h:
                out.append((h, "competitor_surface.web_probes"))
    return out


def _classify_host(host: str, rules: dict[str, Any]) -> tuple[str, float]:
    overrides = rules.get("overrides") or {}
    if isinstance(overrides, dict) and host in overrides:
        return str(overrides[host]), 0.95

    host_l = host.lower()
    best_cls = "unknown"
    best_conf = 0.4
    best_suf_len = -1
    suffix_rules = rules.get("suffix_rules") or []
    if isinstance(suffix_rules, list):
        for rule in suffix_rules:
            if not isinstance(rule, dict):
                continue
            suf = str(rule.get("suffix") or "").lower().strip(".")
            if not suf:
                continue
            if host_l == suf or host_l.endswith("." + suf):
                cls = str(rule.get("classification") or "unknown")
                conf = float(rule.get("confidence") or 0.6)
                if len(suf) > best_suf_len or (
                    len(suf) == best_suf_len and conf > best_conf
                ):
                    best_cls = cls
                    best_conf = conf
                    best_suf_len = len(suf)
    return best_cls, best_conf


def collect_observed_endpoints(
    run: NormalizedRun,
    rules: dict[str, Any],
) -> list[ObservedEndpoint]:
    seen: dict[str, ObservedEndpoint] = {}
    for host, src in _iter_hosts_services_contacted(run) + _iter_hosts_web_probes(run):
        if host in seen:
            continue
        cls, conf = _classify_host(host, rules)
        seen[host] = ObservedEndpoint(
            host=host,
            classification=cls,
            confidence=conf,
            source=src,
            evidence_refs=[
                EvidenceRef(
                    normalized_pointer="services_contacted"
                    if src == "services_contacted"
                    else "competitor_surface.web_probes",
                ),
            ],
        )
    return sorted(seen.values(), key=lambda x: x.host)
