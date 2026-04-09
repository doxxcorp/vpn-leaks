"""Multi-source exit IP capture."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from vpn_leaks.models import ExitIpSource


async def run_ip_check(
    *,
    raw_dir: Path,
    endpoints: list[dict[str, Any]],
    services_contacted: list[str],
) -> tuple[list[ExitIpSource], str | None, str | None]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    sources: list[ExitIpSource] = []
    v4: str | None = None
    v6: str | None = None

    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        for ep in endpoints:
            url = ep["url"]
            fmt = ep.get("format", "text")
            services_contacted.append(url)
            try:
                r = await client.get(url)
                r.raise_for_status()
                text = r.text.strip()
                ipv4: str | None = None
                ipv6: str | None = None
                if fmt == "json":
                    data = r.json()
                    key = ep.get("json_ipv4_key", "ip")
                    if isinstance(data, dict) and key in data:
                        val = str(data[key])
                        if ":" in val:
                            ipv6 = val
                        else:
                            ipv4 = val
                else:
                    if ":" in text and "." not in text.split(":")[0]:
                        ipv6 = text
                    else:
                        ipv4 = text
                sources.append(
                    ExitIpSource(url=url, ipv4=ipv4, ipv6=ipv6, raw_excerpt=text[:500]),
                )
                v4 = ipv4 or v4
                v6 = ipv6 or v6
            except Exception as e:
                sources.append(
                    ExitIpSource(url=url, error=str(e)),
                )

    out_path = raw_dir / "ip-check.json"
    out_path.write_text(
        json.dumps([s.model_dump(mode="json") for s in sources], indent=2),
        encoding="utf-8",
    )
    return sources, v4, v6


def run_ip_check_sync(
    *args: Any,
    **kwargs: Any,
) -> tuple[list[ExitIpSource], str | None, str | None]:
    import asyncio

    return asyncio.run(run_ip_check(*args, **kwargs))
