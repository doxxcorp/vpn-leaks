"""IPv6 checks: curl-style fetch + external page."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import httpx


async def run_ipv6_checks(
    *,
    raw_dir: Path,
    leak_cfg: dict[str, Any],
    exit_ip_v6: str | None,
    services_contacted: list[str],
) -> tuple[str | None, bool | None, str | None]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    ipv6_cfg = leak_cfg.get("ipv6") or {}

    v6_from_curl: str | None = None
    for url in ipv6_cfg.get("curl_v6_urls") or []:
        services_contacted.append(url)
        try:
            proc = subprocess.run(
                ["curl", "-6", "-sS", "--max-time", "15", url],
                capture_output=True,
                text=True,
                timeout=20,
                check=False,
            )
            (raw_dir / "curl_v6.txt").write_text(proc.stdout + proc.stderr, encoding="utf-8")
            out = proc.stdout.strip()
            if out and ":" in out:
                v6_from_curl = out.splitlines()[0][:128]
                break
        except FileNotFoundError:
            (raw_dir / "curl_v6.txt").write_text("curl not found\n", encoding="utf-8")
            break
        except Exception as e:
            (raw_dir / "curl_v6_error.txt").write_text(str(e), encoding="utf-8")

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        for page in ipv6_cfg.get("external_pages") or []:
            url = page.get("url")
            if not url:
                continue
            name = page.get("name") or "ipv6_external"
            services_contacted.append(url)
            try:
                r = await client.get(url, timeout=float(page.get("timeout_seconds") or 45))
                (raw_dir / f"{name}.html").write_text(r.text, encoding="utf-8", errors="replace")
            except Exception as e:
                (raw_dir / f"{name}_error.txt").write_text(str(e), encoding="utf-8")

    status, leak_flag, notes = _classify_ipv6(v6_from_curl, exit_ip_v6)
    summary = {
        "v6_from_curl": v6_from_curl,
        "exit_ip_v6": exit_ip_v6,
        "ipv6_status": status,
        "ipv6_leak_flag": leak_flag,
        "notes": notes,
    }
    (raw_dir / "ipv6_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return status, leak_flag, notes


def _classify_ipv6(
    v6_curl: str | None,
    exit_v6: str | None,
) -> tuple[str | None, bool | None, str | None]:
    if not v6_curl and not exit_v6:
        return "unsupported_or_no_ipv6", False, "No IPv6 observed via curl or IP endpoints"
    if v6_curl:
        return "observed", False, "IPv6 egress observed (compare to tunnel expectations manually)"
    if exit_v6:
        return "observed_via_ip_endpoint", False, "IPv6 from IP endpoint only"
    return "unknown", None, "Ambiguous IPv6 state"


def run_ipv6_checks_sync(*args: Any, **kwargs: Any) -> tuple[str | None, bool | None, str | None]:
    import asyncio

    return asyncio.run(run_ipv6_checks(*args, **kwargs))
