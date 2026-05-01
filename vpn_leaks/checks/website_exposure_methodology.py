"""Automated website exposure methodology Phases 1–9 (desk automation tier).

Uses existing competitor_probe + surface_probe artifacts; persists raw JSON alongside.
"""

from __future__ import annotations

import ipaddress
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from dns import resolver as dns_resolver
from dns.exception import DNSException
from dns.rdatatype import RdataType

from vpn_leaks.attribution.merge import merge_attribution_for_ip
from vpn_leaks.models import WebsiteExposureMethodology

SPF_INCLUDE = re.compile(r"include:([^\s;]+)", re.IGNORECASE)
SPF_REDIRECT = re.compile(r"redirect=([^\s;]+)", re.IGNORECASE)
DKIM_SELECTORS_COMMON = (
    "google",
    "zendesk1",
    "zendesk2",
    "default",
    "s1",
    "s2",
    "k1",
    "selector1",
    "selector2",
    "smtp",
    "mail",
)
COMMON_SUBDOMAIN_CNAME = (
    "mail",
    "support",
    "help",
    "status",
    "blog",
    "docs",
    "api",
    "autodiscover",
)


def _hosts_from_urls(urls: list[str]) -> set[str]:
    out: set[str] = set()
    for u in urls:
        u = str(u).strip()
        if not u:
            continue
        try:
            p = urlparse(u if "://" in u else f"https://{u}")
        except Exception:
            continue
        if p.hostname:
            out.add(p.hostname.lower().strip("."))
    return out


def _har_hosts_from_summary(hs: dict[str, Any] | None) -> set[str]:
    if not isinstance(hs, dict):
        return set()
    hosts: set[str] = set()
    for k in ("merged_unique_hosts", "unique_hosts"):
        for h in hs.get(k) or []:
            if isinstance(h, str) and h.strip():
                hosts.add(h.strip().lower())
    return hosts


def _collect_hosts_inventory(
    vpn_config: dict[str, Any],
    competitor_surface: dict[str, Any] | None,
    surface_probe: dict[str, Any] | None,
) -> dict[str, Any]:
    hosts: set[str] = set()
    sources: dict[str, list[str]] = {}

    cp = vpn_config.get("competitor_probe") or {}
    if isinstance(cp, dict):
        for u in cp.get("probe_urls") or []:
            h = _hosts_from_urls([str(u)])
            for x in h:
                hosts.add(x)
        for h in cp.get("portal_hosts") or []:
            if isinstance(h, str) and h.strip():
                hosts.add(h.strip().lower())
        for d in cp.get("provider_domains") or []:
            if isinstance(d, str) and d.strip():
                hosts.add(d.strip().lower())

    for su in vpn_config.get("surface_urls") or []:
        if isinstance(su, dict) and su.get("url"):
            hosts |= _hosts_from_urls([str(su["url"])])

    if isinstance(competitor_surface, dict):
        hs = competitor_surface.get("har_summary")
        hh = _har_hosts_from_summary(hs if isinstance(hs, dict) else None)
        if hh:
            hosts |= hh
            sources["competitor_har"] = sorted(hh)[:200]
        for row in competitor_surface.get("web_probes") or []:
            if isinstance(row, dict) and row.get("url"):
                hosts |= _hosts_from_urls([str(row["url"])])

    if isinstance(surface_probe, dict):
        hs = surface_probe.get("har_summary")
        sh = _har_hosts_from_summary(hs if isinstance(hs, dict) else None)
        if sh:
            hosts |= sh
            sources["surface_har"] = sorted(sh)[:200]
        for row in surface_probe.get("probes") or []:
            if isinstance(row, dict) and row.get("url"):
                hosts |= _hosts_from_urls([str(row["url"])])

    return {"unique_hosts": sorted(hosts), "approx_count": len(hosts), "sources": sources}


def _resolve_host(
    res: dns_resolver.Resolver, host: str
) -> dict[str, Any]:
    row: dict[str, Any] = {"a": [], "aaaa": [], "error": None}
    try:
        ans = res.resolve(host, RdataType.A)
        row["a"] = sorted({str(r) for r in ans})
    except DNSException as e:
        row["error"] = f"A:{e}"[:200]
    try:
        ans = res.resolve(host, RdataType.AAAA)
        row["aaaa"] = sorted({str(r) for r in ans})
    except DNSException:
        pass
    return row


def _collect_resolver_results(
    hosts: list[str],
    *,
    services_contacted: list[str],
    attr_cfg: dict[str, Any] | None,
) -> dict[str, Any]:
    res = dns_resolver.Resolver()
    res.timeout = 4
    res.lifetime = 8
    out: dict[str, Any] = {"by_host": {}, "ip_attribution_sample": {}}
    ip_cache: dict[str, dict[str, Any]] = {}
    for host in hosts[:400]:
        services_contacted.append(f"dns:resolve:{host}")
        out["by_host"][host] = _resolve_host(res, host)
        for fam in ("a", "aaaa"):
            for ip_s in out["by_host"][host].get(fam) or []:
                if ip_s in ip_cache:
                    continue
                try:
                    ip_obj = ipaddress.ip_address(ip_s)
                except ValueError:
                    continue
                if ip_obj.is_private or ip_obj.is_loopback:
                    continue
                if not attr_cfg:
                    continue
                services_contacted.append(f"attribution:methodology:{ip_s}")
                ip_cache[ip_s] = merge_attribution_for_ip(
                    ip_s, attr_cfg, role="website_host"
                ).model_dump(mode="json")
    out["ip_attribution_sample"] = ip_cache
    return out


def _classify_hosts(
    hosts: list[str],
    har_trackers: set[str],
    har_cdns: set[str],
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for h in hosts[:500]:
        tags: list[str] = []
        if h in har_trackers:
            tags.append("tracker_candidate")
        if h in har_cdns:
            tags.append("cdn_candidate")
        if not tags:
            tags.append("unknown")
        rows.append({"host": h, "tags": tags})
    return {"rows": rows, "notes": "Heuristic tags from HAR hints + host presence only."}


def _walk_spf_includes(
    res: dns_resolver.Resolver,
    domain: str,
    *,
    seen: set[str],
    depth: int,
    services_contacted: list[str],
    max_depth: int = 14,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    includes: list[str] = []
    if depth > max_depth or domain.lower() in seen:
        return includes, errors
    seen.add(domain.lower())
    try:
        ans = res.resolve(domain, RdataType.TXT)
    except DNSException as e:
        errors.append(str(e)[:200])
        return includes, errors
    services_contacted.append(f"spf:txt:{domain}")
    blobs: list[str] = []
    for r in ans:
        chunks = getattr(r, "strings", None) or ()
        blobs.append(b"".join(chunks).decode("utf-8", errors="replace"))

    redirects: list[str] = []
    for txt in blobs:
        if "spf" not in txt.lower():
            continue
        for raw in SPF_INCLUDE.findall(txt):
            tgt = raw.rstrip(";").strip().strip(".").lower()
            if tgt:
                includes.append(tgt)
        for raw in SPF_REDIRECT.findall(txt):
            tgt = raw.rstrip(";").strip().strip(".").lower()
            if tgt:
                redirects.append(tgt)
    merged = list(sorted(set(includes + redirects)))
    sub_includes: list[str] = list(merged)
    for tgt in merged:
        more, errs = _walk_spf_includes(
            res,
            tgt,
            seen=seen,
            depth=depth + 1,
            services_contacted=services_contacted,
            max_depth=max_depth,
        )
        sub_includes.extend(more)
        errors.extend(errs)
    return list(sorted(set(sub_includes))), errors


def _phase8_deep_audit(
    domains: list[str],
    *,
    raw_dir: Path,
    existing_provider_dns: dict[str, Any] | None,
    services_contacted: list[str],
) -> dict[str, Any]:
    res = dns_resolver.Resolver()
    res.timeout = 4
    res.lifetime = 10
    out: dict[str, Any] = {
        "per_domain": {},
        "spf_include_graph_flat": [],
        "subdomain_cname_scans": {},
        "errors": [],
    }

    apex_seed = sorted({str(d).strip().lower().rstrip(".") for d in domains if d})

    for domain in apex_seed[:32]:
        drow: dict[str, Any] = {
            "dmarc_txt": [],
            "dkim_hit_selectors": {},
            "cname_aliases": [],
        }

        dmarc_dom = f"_dmarc.{domain}"
        services_contacted.append(f"dns:dmarc:{dmarc_dom}")
        try:
            ans = res.resolve(dmarc_dom, RdataType.TXT)
            dmarc_chunks: list[str] = []
            for r in ans:
                ch = getattr(r, "strings", None) or ()
                dmarc_chunks.append(b"".join(ch).decode("utf-8", errors="replace")[:480])
            drow["dmarc_txt"] = dmarc_chunks
        except DNSException as e:
            drow["dmarc_txt_error"] = str(e)[:200]

        dkim_hit: dict[str, list[str]] = {}
        for sel in DKIM_SELECTORS_COMMON:
            q = f"{sel}._domainkey.{domain}"
            services_contacted.append(f"dns:dkim:{q}")
            try:
                ans = res.resolve(q, RdataType.TXT)
                lines: list[str] = []
                for r in ans:
                    ch = getattr(r, "strings", None) or ()
                    lines.append(b"".join(ch).decode("utf-8", errors="replace")[:400])
                if lines:
                    dkim_hit[sel] = lines
            except DNSException:
                pass
        drow["dkim_hit_selectors"] = dkim_hit

        submap: dict[str, Any] = {}
        for sub in COMMON_SUBDOMAIN_CNAME:
            fq = f"{sub}.{domain}"
            services_contacted.append(f"dns:cname_scan:{fq}")
            try:
                ans = res.resolve(fq, RdataType.CNAME)
                names = [str(r.target).rstrip(".").lower() for r in ans]
                if names:
                    submap[sub] = names
            except DNSException:
                pass
        drow["subdomain_cname_scan"] = submap

        spf_inc, spf_err = _walk_spf_includes(
            res,
            domain,
            seen=set(),
            depth=0,
            services_contacted=services_contacted,
        )
        drow["spf_include_expansion"] = spf_inc
        drow["spf_errors"] = spf_err
        out["per_domain"][domain] = drow

    out.setdefault("provider_dns_snapshot_ref", "competitor_surface.provider_dns")

    methodology_dir = raw_dir / "website_exposure"
    methodology_dir.mkdir(parents=True, exist_ok=True)
    if isinstance(existing_provider_dns, dict):
        out.setdefault("apex_copy", existing_provider_dns.get("domains", {}))
    else:
        out.setdefault("apex_copy", {})
    audit_path = methodology_dir / "phase8_dns_audit.json"
    audit_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def _phase9_inventory(
    *,
    hosts_inv: dict[str, Any],
    phase8: dict[str, Any],
    har_trackers: set[str],
    har_cdns: set[str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_row(company: str, role: str, how: str, evidence: str) -> None:
        key = (company.lower(), role)
        if key in seen:
            return
        seen.add(key)
        rows.append(
            {
                "company_hypothesis": company,
                "role": role,
                "how_discovered": how,
                "evidence_summary": evidence,
                "evidence_tier": "desk_automation",
            }
        )

    for h in har_trackers:
        add_row(h, "website_script_or_beacon", "har_tracker_hint", f"host:{h}")
    for h in har_cdns:
        add_row(h, "cdn_or_edge", "har_cdn_hint", f"host:{h}")

    per = (phase8.get("per_domain") or {}) if isinstance(phase8, dict) else {}
    for dom, drow in per.items():
        if not isinstance(drow, dict):
            continue
        ac = phase8.get("apex_copy")
        apex = ac.get(dom) if isinstance(ac, dict) else None
        if isinstance(apex, dict):
            for mx in apex.get("mx") or []:
                if "google" in str(mx).lower():
                    add_row("Google", "email_mx_inferred", "apex_mx", f"{dom}:{mx}")
                if "zendesk" in str(mx).lower():
                    add_row("Zendesk", "support_or_email_inferred", "apex_mx", f"{dom}:{mx}")
            for ns in apex.get("ns") or []:
                if "cloudflare" in str(ns).lower():
                    add_row("Cloudflare", "dns_authority_inferred", "ns", f"{dom}:{ns}")
            for txt in apex.get("txt") or []:
                tlow = str(txt).lower()
                if "facebook-domain-verification" in tlow:
                    add_row("Meta/Facebook", "domain_verification_txt", "txt", dom)
                if "google-site-verification" in tlow:
                    add_row("Google", "domain_verification_txt", "txt", dom)
                if "stripe-verification" in tlow:
                    add_row("Stripe", "domain_verification_txt", "txt", dom)

        for sel, lines in (drow.get("dkim_hit_selectors") or {}).items():
            if lines:
                add_row(
                    f"DKIM:{sel}",
                    "email_signing_inferred",
                    "dkim_txt",
                    f"{dom} selector {sel}",
                )

        for sub, targets in (drow.get("subdomain_cname_scan") or {}).items():
            if not isinstance(targets, list):
                continue
            for t in targets:
                tl = str(t).lower()
                if "zendesk" in tl:
                    add_row("Zendesk", "support_platform_inferred", "cname", f"{sub}.{dom}->{t}")
                if "sparkpost" in tl or "bird.com" in tl:
                    add_row(
                        "SparkPost/Bird",
                        "transactional_email_inferred",
                        "cname",
                        f"{sub}.{dom}->{t}",
                    )

        for inc in drow.get("spf_include_expansion") or []:
            il = str(inc).lower()
            if "google" in il or "_spf.google" in il:
                add_row("Google", "spf_email_sender_inferred", "spf_include", f"{dom}->{inc}")
            if "zendesk" in il:
                add_row("Zendesk", "spf_email_sender_inferred", "spf_include", f"{dom}->{inc}")
            if "salesforce" in il:
                add_row("Salesforce", "spf_email_sender_inferred", "spf_include", f"{dom}->{inc}")
            if "mailgun" in il:
                add_row("Mailgun", "spf_email_sender_inferred", "spf_include", f"{dom}->{inc}")

    approx = int(hosts_inv.get("approx_count") or 0)
    add_row(
        "(provider first-party)",
        "marketing_and_app_surface",
        "config_urls",
        f"~{approx} web hosts observed",
    )

    return rows


def run_website_exposure_methodology(
    *,
    vpn_config: dict[str, Any],
    competitor_surface: Any,
    surface_probe: dict[str, Any] | None,
    raw_dir: Path,
    services_contacted: list[str],
    attr_cfg: dict[str, Any] | None,
) -> WebsiteExposureMethodology:
    errors: list[str] = []
    limits: list[str] = [
        "Does_not_replace_human_narrative_for_executive_disclosure",
        "Cloudflare_or_bot_WAF_may_distort_HAR_coverage",
    ]

    cs_dict: dict[str, Any] | None
    if competitor_surface is None:
        cs_dict = None
    elif hasattr(competitor_surface, "model_dump"):
        cs_dict = competitor_surface.model_dump(mode="json")
    else:
        cs_dict = dict(competitor_surface) if isinstance(competitor_surface, dict) else None

    inv = _collect_hosts_inventory(vpn_config, cs_dict, surface_probe)
    hosts = list(inv.get("unique_hosts") or [])

    har_trackers: set[str] = set()
    har_cdns: set[str] = set()
    for blob in (cs_dict, surface_probe):
        if not isinstance(blob, dict):
            continue
        hs = blob.get("har_summary") or {}
        if not isinstance(hs, dict):
            continue
        for t in hs.get("merged_tracker_candidates") or hs.get("tracker_candidates") or []:
            if isinstance(t, str):
                har_trackers.add(t.strip().lower())
        for c in hs.get("merged_cdn_candidates") or hs.get("cdn_candidates") or []:
            if isinstance(c, str):
                har_cdns.add(c.strip().lower())

    resolver: dict[str, Any] = {}
    if hosts:
        try:
            resolver = _collect_resolver_results(
                hosts,
                services_contacted=services_contacted,
                attr_cfg=attr_cfg,
            )
        except Exception as e:
            errors.append(f"resolver:{e}")
            resolver = {"error": str(e)[:400]}

    classification = _classify_hosts(hosts, har_trackers, har_cdns)

    cp = vpn_config.get("competitor_probe") or {}
    provider_domains: list[str] = []
    if isinstance(cp, dict):
        provider_domains = [str(x) for x in (cp.get("provider_domains") or []) if x]

    phase8: dict[str, Any] = {}
    if provider_domains:
        try:
            existing_pd = (cs_dict or {}).get("provider_dns") if cs_dict else None
            phase8 = _phase8_deep_audit(
                provider_domains,
                raw_dir=raw_dir,
                existing_provider_dns=existing_pd if isinstance(existing_pd, dict) else None,
                services_contacted=services_contacted,
            )
        except Exception as e:
            errors.append(f"phase8:{e}")
            phase8 = {"errors": [str(e)[:400]]}
    else:
        limits.append("Skipped_phase8_no_provider_domains_in_config")

    phase9 = _phase9_inventory(
        hosts_inv=inv,
        phase8=phase8,
        har_trackers=har_trackers,
        har_cdns=har_cdns,
    )

    methodology_dir = raw_dir / "website_exposure"
    methodology_dir.mkdir(parents=True, exist_ok=True)
    (methodology_dir / "hosts_inventory.json").write_text(
        json.dumps(inv, indent=2),
        encoding="utf-8",
    )
    (methodology_dir / "resolver_sample.json").write_text(
        json.dumps(resolver, indent=2),
        encoding="utf-8",
    )
    (methodology_dir / "phase9_inventory.json").write_text(
        json.dumps(phase9, indent=2),
        encoding="utf-8",
    )

    try:
        from vpn_leaks.config_loader import repo_root

        rr = repo_root()
        raw_relpaths = {
            "hosts_inventory": str((methodology_dir / "hosts_inventory.json").relative_to(rr)),
            "resolver_sample": str((methodology_dir / "resolver_sample.json").relative_to(rr)),
            "phase9_inventory": str((methodology_dir / "phase9_inventory.json").relative_to(rr)),
        }
        if (methodology_dir / "phase8_dns_audit.json").is_file():
            raw_relpaths["phase8_dns_audit"] = str(
                (methodology_dir / "phase8_dns_audit.json").relative_to(rr)
            )
    except ValueError:
        raw_relpaths = {}

    phases_summary = {
        "1_fetch": "urls_from_config_and_har_summaries",
        "2_extract": "hosts_parsed_via_urlparse",
        "3_dedupe": f"unique_hosts={inv.get('approx_count')}",
        "4_resolve": "A_AAAA_optional_public_ip_attribution",
        "5_whois_via_attribution": "sample_only_for_selected_public_ips",
        "6_classify": "har_tracker_cdn_hints_plus_unknown_bucket",
        "7_document": "machine_json_hosts_inventory_plus_resolver_samples",
        "8_dns_infra": "spf_walk_dkim_dmarc_cname_scan" if provider_domains else "skipped",
        "9_inventory": f"rows={len(phase9)}",
    }

    return WebsiteExposureMethodology(
        methodology_schema_version="1.0",
        phases=phases_summary,
        hosts_inventory=inv,
        resolver_results=resolver,
        classifications=classification,
        phase8_dns_infra=phase8,
        phase9_third_party_inventory=phase9,
        raw_relpaths=raw_relpaths,
        limits=limits,
        errors=errors,
    )
