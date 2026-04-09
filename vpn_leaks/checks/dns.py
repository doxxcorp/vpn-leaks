"""DNS observations: local resolver snapshot + external page fetch."""

from __future__ import annotations

import json
import re
import socket
from pathlib import Path
from typing import Any

import httpx

from vpn_leaks.models import DnsObservation


def _read_resolv_conf() -> list[str]:
    path = Path("/etc/resolv.conf")
    servers: list[str] = []
    if not path.is_file():
        return servers
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line.startswith("nameserver"):
            parts = line.split()
            if len(parts) >= 2:
                servers.append(parts[1])
    return servers


def _local_dns_snapshot() -> DnsObservation:
    servers = _read_resolv_conf()
    return DnsObservation(
        tier="local",
        detail="resolv.conf nameserver lines (Unix)",
        servers=servers,
    )


def _extract_ipv4s(text: str) -> list[str]:
    pat = re.compile(
        r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
        r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b",
    )
    return list(dict.fromkeys(pat.findall(text)))


async def run_dns_checks(
    *,
    raw_dir: Path,
    leak_cfg: dict[str, Any],
    exit_ip_v4: str | None,
    services_contacted: list[str],
) -> tuple[list[DnsObservation], bool | None, str | None]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    obs: list[DnsObservation] = []

    dns_cfg = leak_cfg.get("dns") or {}
    if dns_cfg.get("local_resolv_conf", True):
        obs.append(_local_dns_snapshot())

    hostname = dns_cfg.get("test_hostname") or "example.com"
    try:
        infos = socket.getaddrinfo(hostname, None)
        gai = sorted({x[4][0] for x in infos})
        obs.append(
            DnsObservation(
                tier="local",
                detail=f"getaddrinfo({hostname!r})",
                servers=gai,
            ),
        )
    except OSError as e:
        obs.append(DnsObservation(tier="local", detail=f"getaddrinfo failed: {e}", servers=[]))

    external_pages = dns_cfg.get("external_pages") or []
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        for page in external_pages:
            url = page.get("url")
            if not url:
                continue
            name = page.get("name") or "external"
            timeout = float(page.get("timeout_seconds") or 45)
            services_contacted.append(url)
            try:
                r = await client.get(url, timeout=timeout)
                text = r.text
                (raw_dir / f"{name}.html").write_text(text, encoding="utf-8", errors="replace")
                ips = _extract_ipv4s(text)
                obs.append(
                    DnsObservation(
                        tier="external",
                        detail=name,
                        servers=ips[:64],
                    ),
                )
            except Exception as e:
                obs.append(
                    DnsObservation(
                        tier="external",
                        detail=f"{name} error: {e}",
                        servers=[],
                    ),
                )

    summary_path = raw_dir / "dns_summary.json"
    summary_path.write_text(
        json.dumps([o.model_dump(mode="json") for o in obs], indent=2),
        encoding="utf-8",
    )

    leak_flag, notes = _infer_dns_leak(obs, exit_ip_v4)
    return obs, leak_flag, notes


def _infer_dns_leak(
    obs: list[DnsObservation],
    exit_ip_v4: str | None,
) -> tuple[bool | None, str | None]:
    """Heuristic: external page lists resolver IPs; flag if many public resolvers and ambiguous."""
    ext = [o for o in obs if o.tier == "external" and o.servers]
    if not ext:
        return None, "No external DNS test results; cannot infer leak flag automatically"
    all_ips: list[str] = []
    for o in ext:
        all_ips.extend(o.servers)
    if not all_ips:
        return False, "External test returned no IPv4-like strings (parse may need tuning)"

    # If exit IP appears as only "identity" that's expected; resolvers listed are the signal.
    # Conservative: flag if public DNS (e.g. 8.8.8.8, 1.1.1.1) appear as resolver candidates.
    public = {"8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1"}
    hit = public.intersection(set(all_ips))
    if hit:
        return True, f"Observed public resolver IPs in external test content: {sorted(hit)}"
    return False, "Heuristic: no obvious public resolver IPs parsed from external page"


def run_dns_checks_sync(
    *args: Any,
    **kwargs: Any,
) -> tuple[list[DnsObservation], bool | None, str | None]:
    import asyncio

    return asyncio.run(run_dns_checks(*args, **kwargs))
