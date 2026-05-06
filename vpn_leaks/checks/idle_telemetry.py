"""Capture network traffic while a VPN app is running but the tunnel is OFF.

Operator workflow:
    1. Launch the VPN app (do NOT click connect).
    2. Run ``sudo vpn-leaks capture idle --provider <slug> --duration 120``.
    3. The harness captures raw-IP traffic for ``duration`` seconds, summarizes
       the resulting PCAP, attributes every contact via WHOIS / BGP / role
       classification (TASK-03), and writes ``idle_telemetry.json``.

Any contact that is NOT owned by the provider represents data exposure that
happens before the user has decided to connect (TASK-10).
"""

from __future__ import annotations

import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vpn_leaks.capture import session as capture_session
from vpn_leaks.checks.pcap_summarize import write_pcap_summary_json
from vpn_leaks.config_loader import repo_root
from vpn_leaks.reporting.web_exposure import (
    classify_contact_role,
    pcap_host_intelligence,
)


def _summarize_contacts(
    rows: list[dict[str, Any]],
    *,
    provider_name: str,
) -> dict[str, int]:
    total = 0
    provider_owned = 0
    third_party = 0
    dns_resolvers = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        total += 1
        role = row.get("role") or classify_contact_role(
            owner=row.get("owner", "") or "",
            canonical_company=row.get("owner", "") or "",
            provider_name=provider_name,
            sources=row.get("source", "") or "",
        )
        if role == "vpn-control" or role == "vpn-data":
            provider_owned += 1
        elif role == "dns-resolver":
            dns_resolvers += 1
        else:
            third_party += 1
    return {
        "total_contacts": total,
        "provider_owned": provider_owned,
        "third_party": third_party,
        "dns_resolvers": dns_resolvers,
    }


def run_idle_capture(
    provider: str,
    *,
    duration: int = 120,
    interface: str = "en0",
    output: str | None = None,
    bpf: str | None = None,
) -> dict[str, Any]:
    """Capture, summarize, attribute, and persist idle-window telemetry.

    Returns the structured result and writes it to ``output`` (default:
    ``runs/idle_telemetry/<provider>-<timestamp>.json``). Requires sudo for
    tcpdump on most systems.
    """
    if duration < 1:
        raise ValueError("duration must be at least 1 second")

    desc, err = capture_session.start(interface=interface, bpf=bpf)
    if err or desc is None:
        raise RuntimeError(f"capture start failed: {err or 'unknown'}")

    start_at = datetime.now(UTC).isoformat()
    print(
        f"[idle] tcpdump started session={desc.session_id} pid={desc.pid} iface={interface}",
        flush=True,
    )
    print(f"[idle] capturing for {duration}s — keep VPN app open but DISCONNECTED", flush=True)
    try:
        time.sleep(duration)
    finally:
        ok, msg = capture_session.abort(discard_pcap=False)
        if not ok:
            raise RuntimeError(f"capture abort failed: {msg}")

    pcap_path = Path(desc.pcap_path)
    if not pcap_path.is_file():
        raise FileNotFoundError(f"expected pcap missing: {pcap_path}")

    pcap_summary_path = pcap_path.with_suffix(".pcap.summary.json")
    pcap_summary = write_pcap_summary_json(pcap_path, pcap_summary_path)

    intel = pcap_host_intelligence({"pcap_derived": pcap_summary})
    rows = intel.get("rows") or []
    contacts: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        canonical_owner = row.get("owner", "") or ""
        role = classify_contact_role(
            owner=canonical_owner,
            canonical_company=canonical_owner,
            provider_name=provider,
            sources=row.get("source", "") or "",
        )
        contacts.append({
            "ip": row.get("ip", ""),
            "host": row.get("host", ""),
            "asn": row.get("asn", ""),
            "owner": canonical_owner,
            "bytes": int(row.get("bytes_observed") or 0),
            "flows": int(row.get("flow_count") or 0),
            "reverse_dns": row.get("reverse_dns", ""),
            "upstream_asn": row.get("upstream_asn"),
            "as_path": row.get("as_path"),
            "sources": row.get("source", ""),
            "role": role,
        })

    result: dict[str, Any] = {
        "provider": provider,
        "duration_seconds": duration,
        "captured_at": start_at,
        "interface": interface,
        "pcap_path": str(pcap_path),
        "pcap_summary_path": str(pcap_summary_path),
        "contacts": contacts,
        "summary": _summarize_contacts(contacts, provider_name=provider),
    }

    if output:
        out_path = Path(output).resolve()
    else:
        out_dir = repo_root() / "runs" / "idle_telemetry"
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        out_path = out_dir / f"{provider}-{ts}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    result["output_path"] = str(out_path)
    print(f"[idle] wrote {out_path}", flush=True)
    return result
