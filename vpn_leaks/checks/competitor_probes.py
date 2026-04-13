"""Competitor-surface probes: provider DNS, web/CDN/HAR, portals, transit, stray JSON paths."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import httpx

from vpn_leaks.attribution.merge import merge_attribution_for_ip
from vpn_leaks.config_loader import repo_root
from vpn_leaks.models import CompetitorSurfaceSnapshot

CDN_HEADER_KEYS = frozenset(
    {
        "server",
        "via",
        "cf-ray",
        "x-cache",
        "x-served-by",
        "x-amz-cf-id",
        "x-fastly-request-id",
        "age",
        "cache-status",
    },
)


def _safe_har_name(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def run_provider_dns(
    domains: list[str],
    *,
    raw_dir: Path,
    services_contacted: list[str],
    attr_cfg: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve NS for apex domains; resolve NS hostnames (glue) and optional attribution."""
    from dns import resolver as dns_resolver
    from dns.exception import DNSException
    from dns.rdatatype import RdataType

    out: dict[str, Any] = {"domains": {}, "ns_hosts": {}}
    res = dns_resolver.Resolver()
    res.timeout = 5
    res.lifetime = 10

    for domain in domains:
        domain = domain.strip().lower().rstrip(".")
        if not domain:
            continue
        services_contacted.append(f"dns:lookup:{domain}")
        entry: dict[str, Any] = {"ns": [], "a": [], "aaaa": [], "error": None}
        try:
            ans = res.resolve(domain, RdataType.NS)
            entry["ns"] = sorted({str(r.target).rstrip(".").lower() for r in ans})
        except DNSException as e:
            entry["error"] = f"NS: {e}"
        try:
            aa = res.resolve(domain, RdataType.A)
            entry["a"] = sorted({str(r) for r in aa})
        except DNSException:
            pass
        try:
            aaaa = res.resolve(domain, RdataType.AAAA)
            entry["aaaa"] = sorted({str(r) for r in aaaa})
        except DNSException:
            pass
        out["domains"][domain] = entry

    ip_attr_cache: dict[str, dict[str, Any]] = {}

    def attribution_for_ip(ip: str) -> dict[str, Any]:
        if ip in ip_attr_cache:
            return ip_attr_cache[ip]
        if not attr_cfg:
            ip_attr_cache[ip] = {}
            return ip_attr_cache[ip]
        time.sleep(0.25)
        services_contacted.append(f"attribution:ns_glue:{ip}")
        merged = merge_attribution_for_ip(ip, attr_cfg, role="provider_ns_glue")
        ip_attr_cache[ip] = merged.model_dump(mode="json")
        return ip_attr_cache[ip]

    all_ns: set[str] = set()
    for entry in out["domains"].values():
        for ns in entry.get("ns") or []:
            all_ns.add(ns)

    for host in sorted(all_ns):
        row: dict[str, Any] = {"a": [], "aaaa": [], "ip_attribution": {}, "error": None}
        services_contacted.append(f"dns:ns_glue:{host}")
        try:
            aa = res.resolve(host, RdataType.A)
            row["a"] = sorted({str(r) for r in aa})
        except DNSException as e:
            row["error"] = f"A: {e}"
        try:
            aaaa = res.resolve(host, RdataType.AAAA)
            row["aaaa"] = sorted({str(r) for r in aaaa})
        except DNSException:
            pass
        for ip in row["a"] + row["aaaa"]:
            row["ip_attribution"][ip] = attribution_for_ip(ip)
        out["ns_hosts"][host] = row

    raw_dir.mkdir(parents=True, exist_ok=True)
    p = raw_dir / "provider_dns.json"
    p.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def run_transit_probe(
    exit_ip_v4: str,
    *,
    raw_dir: Path,
    services_contacted: list[str],
) -> dict[str, Any]:
    """Best-effort traceroute from this host toward exit (through VPN tunnel)."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "target": exit_ip_v4,
        "command": None,
        "stdout": "",
        "stderr": "",
        "hops": [],
    }

    if sys.platform == "win32":
        cmd = ["tracert", "-d", "-h", "15", exit_ip_v4]
    else:
        cmd = ["traceroute", "-n", "-m", "15", "-w", "2", exit_ip_v4]

    result["command"] = cmd
    services_contacted.append("transit:local_traceroute")

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        result["stdout"] = proc.stdout[-8000:] if len(proc.stdout) > 8000 else proc.stdout
        result["stderr"] = proc.stderr[-2000:] if len(proc.stderr) > 2000 else proc.stderr
        result["returncode"] = proc.returncode
        # Parse IPv4 hops (numeric traceroute)
        for line in proc.stdout.splitlines():
            m = re.search(r"\b(\d{1,3}(?:\.\d{1,3}){3})\b", line)
            if m:
                result["hops"].append(m.group(1))
    except subprocess.TimeoutExpired:
        result["error"] = "timeout"
    except FileNotFoundError:
        result["error"] = "traceroute_not_found"

    out_path = raw_dir / "transit.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def _cdn_signals_from_headers(headers: dict[str, str]) -> dict[str, str]:
    lower = {k.lower(): v for k, v in headers.items()}
    return {k: lower[k] for k in CDN_HEADER_KEYS if k in lower}


def run_web_probes(
    urls: list[str],
    *,
    raw_dir: Path,
    services_contacted: list[str],
) -> list[dict[str, Any]]:
    """Load pages with Playwright; record HAR, response headers, script/image hosts."""
    if not urls:
        return []

    from playwright.sync_api import sync_playwright

    raw_dir.mkdir(parents=True, exist_ok=True)
    har_dir = raw_dir / "har"
    har_dir.mkdir(exist_ok=True)
    results: list[dict[str, Any]] = []

    extract_js = """
    () => {
      const scripts = [...new Set(
        [...document.querySelectorAll('script[src]')].map(s => s.src).filter(Boolean)
      )];
      const images = [...new Set(
        [...document.querySelectorAll('img[src]')].map(i => i.src).filter(Boolean)
      )];
      const captchaHints = scripts.some(u =>
        /recaptcha|turnstile|hcaptcha|challenges\\.cloudflare/i.test(u)
      );
      return { scripts, images, captcha_hints: captchaHints };
    }
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for url in urls:
                url = url.strip()
                if not url:
                    continue
                services_contacted.append(url.split("?")[0])
                har_path = har_dir / f"{_safe_har_name(url)}.har"
                entry: dict[str, Any] = {
                    "url": url,
                    "error": None,
                    "status": None,
                    "final_url": None,
                    "cdn_headers": {},
                    "scripts": [],
                    "images": [],
                    "captcha_third_party": False,
                    "har_path": str(har_path.relative_to(repo_root())),
                }
                context = browser.new_context(record_har_path=str(har_path))
                try:
                    page = context.new_page()
                    resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    if resp:
                        entry["status"] = resp.status
                        entry["final_url"] = resp.url
                        entry["cdn_headers"] = _cdn_signals_from_headers(resp.headers)
                    extracted = page.evaluate(extract_js)
                    entry["scripts"] = extracted.get("scripts") or []
                    entry["images"] = extracted.get("images") or []
                    entry["captcha_third_party"] = bool(extracted.get("captcha_hints"))
                except Exception as e:
                    entry["error"] = str(e)[:500]
                finally:
                    context.close()
                results.append(entry)
        finally:
            browser.close()

    (raw_dir / "web_probes.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


def run_portal_probes(
    hosts: list[str],
    *,
    raw_dir: Path,
    services_contacted: list[str],
) -> list[dict[str, Any]]:
    """DNS A/AAAA + HTTPS GET headers for portal/account hostnames."""
    from dns import resolver as dns_resolver
    from dns.exception import DNSException
    from dns.rdatatype import RdataType

    res = dns_resolver.Resolver()
    res.timeout = 5
    res.lifetime = 10
    out: list[dict[str, Any]] = []

    for host in hosts:
        host = host.strip().lower().rstrip(".")
        if not host:
            continue
        row: dict[str, Any] = {
            "host": host,
            "a": [],
            "aaaa": [],
            "https_status": None,
            "https_cdn_headers": {},
            "error": None,
        }
        try:
            aa = res.resolve(host, RdataType.A)
            row["a"] = sorted({str(r) for r in aa})
        except DNSException:
            pass
        try:
            aaaa = res.resolve(host, RdataType.AAAA)
            row["aaaa"] = sorted({str(r) for r in aaaa})
        except DNSException:
            pass

        url = f"https://{host}/"
        services_contacted.append(url)
        try:
            with httpx.Client(timeout=20.0, follow_redirects=True) as client:
                r = client.get(url)
                row["https_status"] = r.status_code
                row["https_cdn_headers"] = _cdn_signals_from_headers(dict(r.headers))
        except Exception as e:
            row["error"] = str(e)[:400]

        out.append(row)

    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "portal_probes.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def run_stray_json_probes(
    origins: list[str],
    paths: list[str],
    *,
    raw_dir: Path,
    services_contacted: list[str],
) -> list[dict[str, Any]]:
    """Low-rate GET of common stray JSON paths on competitor origins."""
    out: list[dict[str, Any]] = []
    paths = paths or ["/data.json", "/config.json"]

    with httpx.Client(timeout=12.0, follow_redirects=False) as client:
        for origin in origins:
            origin = origin.rstrip("/")
            if not origin:
                continue
            for path in paths:
                path = path if path.startswith("/") else f"/{path}"
                full = urljoin(origin + "/", path.lstrip("/"))
                if not full.startswith("http"):
                    full = "https://" + full
                services_contacted.append(full)
                row: dict[str, Any] = {
                    "url": full,
                    "status": None,
                    "content_type": None,
                    "body_excerpt": None,
                }
                try:
                    r = client.get(full)
                    row["status"] = r.status_code
                    row["content_type"] = r.headers.get("content-type")
                    txt = r.text[:800] if r.text else ""
                    row["body_excerpt"] = txt
                except Exception as e:
                    row["error"] = str(e)[:300]
                out.append(row)

    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "stray_json.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def run_competitor_probes(
    vpn_config: dict[str, Any],
    *,
    raw_base: Path,
    exit_ip_v4: str | None,
    services_contacted: list[str],
    attr_cfg: dict[str, Any] | None = None,
    skip_dns: bool = False,
    skip_web: bool = False,
    skip_portal: bool = False,
    skip_transit: bool = False,
    skip_stray_json: bool = False,
) -> CompetitorSurfaceSnapshot | None:
    """
    Run configured competitor-surface phases. Returns None if `competitor_probe` is absent/empty.
    """
    cfg = vpn_config.get("competitor_probe")
    if not isinstance(cfg, dict) or not cfg:
        return None

    domains = [str(x) for x in (cfg.get("provider_domains") or []) if x]
    urls = [str(x) for x in (cfg.get("probe_urls") or []) if x]
    portal_hosts = [str(x) for x in (cfg.get("portal_hosts") or []) if x]
    stray = cfg.get("stray_json") or {}
    stray_origins = [str(x) for x in (stray.get("origins") or []) if x]
    stray_paths = [str(x) for x in (stray.get("paths") or []) if x]

    has_lists = bool(domains or urls or portal_hosts or stray_origins)
    wants_transit = bool(exit_ip_v4) and not skip_transit
    if not has_lists and not wants_transit:
        return None

    probe_root = raw_base / "competitor_probe"
    probe_root.mkdir(parents=True, exist_ok=True)
    services_contacted.append("competitor_probe:enabled")

    snap = CompetitorSurfaceSnapshot()

    try:
        if not skip_dns and domains:
            snap.provider_dns = run_provider_dns(
                domains,
                raw_dir=probe_root,
                services_contacted=services_contacted,
                attr_cfg=attr_cfg,
            )

        if not skip_transit and exit_ip_v4:
            snap.transit = run_transit_probe(
                exit_ip_v4, raw_dir=probe_root, services_contacted=services_contacted
            )
        elif not skip_transit and not exit_ip_v4:
            snap.errors.append("transit: skipped (no exit IPv4)")

        if not skip_web and urls:
            snap.web_probes = run_web_probes(
                urls,
                raw_dir=probe_root,
                services_contacted=services_contacted,
            )

        if not skip_portal and portal_hosts:
            snap.portal_probes = run_portal_probes(
                portal_hosts, raw_dir=probe_root, services_contacted=services_contacted
            )

        if not skip_stray_json and stray_origins:
            snap.stray_json = run_stray_json_probes(
                stray_origins,
                stray_paths,
                raw_dir=probe_root,
                services_contacted=services_contacted,
            )
    except Exception as e:
        snap.errors.append(f"competitor_probe: {e}")

    return snap
