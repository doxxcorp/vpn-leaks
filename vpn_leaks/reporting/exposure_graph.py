"""Build a stable nodes/edges JSON from normalized benchmark runs (exposure graph)."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vpn_leaks.config_loader import repo_root
from vpn_leaks.reporting.generate_reports import collect_normalized_runs

GRAPH_SCHEMA = "1.0"


def _policy_id(url: str) -> str:
    return "policy:" + hashlib.sha256(url.encode()).hexdigest()[:16]


def build_exposure_graph(provider_slug: str | None = None) -> dict[str, Any]:
    """
    Nodes: vpn, domain, ns, ip, asn, policy_url.
    Edges: exit_ip, attributed_as, provider_apex_domain, delegates_ns, ns_glue, policy_document.
    """
    rows = collect_normalized_runs(provider_slug)
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def node(nid: str, ntype: str, label: str, **meta: Any) -> None:
        if nid not in nodes:
            entry: dict[str, Any] = {"id": nid, "type": ntype, "label": label}
            meta = {k: v for k, v in meta.items() if v is not None}
            entry.update(meta)
            nodes[nid] = entry

    def edge(src: str, tgt: str, relation: str, **prov: Any) -> None:
        row: dict[str, Any] = {"source": src, "target": tgt, "relation": relation}
        prov = {k: v for k, v in prov.items() if v is not None}
        row.update(prov)
        edges.append(row)

    root = repo_root()

    for run_id, path, data in rows:
        loc_id = data.get("vpn_location_id") or ""
        prov = {
            "run_id": run_id,
            "location_id": loc_id,
            "normalized_path": str(path.relative_to(root)),
        }
        slug = data.get("vpn_provider") or "unknown"
        vpn_id = f"vpn:{slug}"
        node(vpn_id, "vpn", slug, vpn_provider=slug)

        att = data.get("attribution") or {}
        exit_v4 = data.get("exit_ip_v4")
        if exit_v4:
            ip_id = f"ip:{exit_v4}"
            node(ip_id, "ip", exit_v4, address=exit_v4)
            edge(vpn_id, ip_id, "exit_ip", **prov)
            asn = att.get("asn")
            if isinstance(asn, int):
                asn_id = f"asn:{asn}"
                holder = att.get("holder") or ""
                node(asn_id, "asn", f"AS{asn} {holder}".strip(), asn=asn, holder=holder)
                edge(ip_id, asn_id, "attributed_as", **prov)

        for pol in data.get("policies") or []:
            url = pol.get("url")
            if not url:
                continue
            pid = _policy_id(url)
            node(pid, "policy_url", url[:120], url=url)
            edge(vpn_id, pid, "policy_document", role=pol.get("role"), **prov)

        cs = data.get("competitor_surface")
        pd: dict[str, Any] = {}
        if isinstance(cs, dict):
            pd = cs.get("provider_dns") or {}
        if not isinstance(pd, dict):
            pd = {}

        domains = pd.get("domains") or {}
        for dname, dentry in domains.items():
            dname = str(dname).lower()
            did = f"domain:{dname}"
            node(did, "domain", dname, apex=dname)
            edge(vpn_id, did, "provider_apex_domain", **prov)
            for ns in dentry.get("ns") or []:
                ns = str(ns).lower()
                nsid = f"ns:{ns}"
                node(nsid, "ns", ns, hostname=ns)
                edge(did, nsid, "delegates_ns", **prov)

        ns_hosts = pd.get("ns_hosts") or {}
        if isinstance(ns_hosts, dict):
            for host, hrow in ns_hosts.items():
                host = str(host).lower()
                nsid = f"ns:{host}"
                node(nsid, "ns", host, hostname=host)
                if not isinstance(hrow, dict):
                    continue
                for ip in (hrow.get("a") or []) + (hrow.get("aaaa") or []):
                    ip = str(ip)
                    ipid = f"ip:{ip}"
                    node(ipid, "ip", ip, address=ip)
                    edge(nsid, ipid, "ns_glue", **prov)
                    ip_att = hrow.get("ip_attribution") or {}
                    if not isinstance(ip_att, dict):
                        continue
                    attr = ip_att.get(ip) or {}
                    if not isinstance(attr, dict):
                        continue
                    asn = attr.get("asn")
                    if isinstance(asn, int):
                        holder = attr.get("holder") or ""
                        asn_id = f"asn:{asn}"
                        node(
                            asn_id,
                            "asn",
                            f"AS{asn} {holder}".strip(),
                            asn=asn,
                            holder=holder,
                            attribution_role="provider_ns_glue",
                        )
                        edge(ipid, asn_id, "attributed_as", **prov)

    return {
        "graph_schema": GRAPH_SCHEMA,
        "generated_utc": datetime.now(UTC).isoformat(),
        "filter_provider": provider_slug,
        "nodes": list(nodes.values()),
        "edges": edges,
    }


def write_exposure_graph(out_path: Path, provider_slug: str | None = None) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_exposure_graph(provider_slug)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
