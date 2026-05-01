"""Tests for VPN HTML report generation (markdown + embedded graph JSON)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from vpn_leaks.reporting.generate_reports import (
    _json_for_html_script,
    markdown_to_html_body,
)


def test_markdown_to_html_table_and_fence() -> None:
    md = """## T

| A | B |
|---|---|
| 1 | 2 |

```json
{"x": 1}
```
"""
    html = markdown_to_html_body(md)
    assert "<table>" in html
    assert "<pre>" in html or "<code>" in html


def test_json_for_html_script_escapes_lt() -> None:
    obj = {"u": "http://x", "t": "<tag>"}
    s = _json_for_html_script(obj)
    assert "</script>" not in s
    assert json.loads(s) == obj


def test_generate_vpn_report_writes_html(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from vpn_leaks.reporting import generate_reports
    from vpn_leaks.reporting import web_exposure

    def fake_root() -> Path:
        return tmp_path

    monkeypatch.setattr("vpn_leaks.config_loader.repo_root", fake_root)
    monkeypatch.setattr("vpn_leaks.reporting.generate_reports.repo_root", fake_root)
    monkeypatch.setattr("vpn_leaks.reporting.exposure_graph.repo_root", fake_root)
    monkeypatch.setattr(
        web_exposure,
        "pcap_host_intelligence",
        lambda data: {
            "has_inventory": True,
            "rows": [
                {
                    "host": "8.8.8.8",
                    "source": "pcap_peer_ip",
                    "ips_text": "8.8.8.8",
                    "reverse_dns": "dns.google",
                    "asn": "AS15169",
                    "owner": "Google LLC",
                    "whois_summary": "OrgName: Google LLC",
                    "dig_summary": "PTR=dns.google",
                    "bytes_observed": 1234,
                    "flow_count": 2,
                    "lookup_errors_text": "—",
                },
            ],
            "errors": [],
            "notes": ["Scope test note."],
        },
    )

    loc = tmp_path / "runs" / "r1" / "locations" / "loc1"
    loc.mkdir(parents=True)
    norm = {
        "vpn_provider": "acme",
        "vpn_location_id": "loc1",
        "vpn_location_label": "L1",
        "schema_version": "1.2",
        "exit_ip_v4": "1.2.3.4",
        "exit_ip_sources": [],
        "dns_servers_observed": [],
        "webrtc_candidates": [],
        "attribution": {"asn": 64496, "holder": "Test"},
        "policies": [],
        "services_contacted": [],
        "artifacts": {},
        "competitor_surface": {
            "har_summary": {
                "merged_unique_hosts": ["a.example.com", "b.example.com"],
                "merged_tracker_candidates": ["stats.example.net"],
                "merged_cdn_candidates": ["cdn.example.org"],
            },
            "provider_dns": {
                "domains": {
                    "acmevpn.example": {
                        "ns": ["ns1.cf.example"],
                        "a": ["1.2.3.4"],
                        "aaaa": [],
                        "mx": ["10 mx.google.example"],
                        "txt": ["v=spf1 -all"],
                    },
                },
                "ns_hosts": {},
            },
            "web_probes": [],
            "portal_probes": [],
        },
        "extra": {
            "surface_probe": {
                "probes": [
                    {
                        "page_type": "home",
                        "url": "https://acmevpn.example/",
                        "status": 200,
                        "error": None,
                    },
                ],
                "har_summary": {
                    "merged_tracker_candidates": ["stats.example.net"],
                    "merged_unique_hosts": ["acmevpn.example"],
                },
            },
        },
        "framework": {
            "risk_scores": {"overall_severity": "LOW"},
            "question_coverage": [
                {
                    "question_id": "DNS-001",
                    "answer_status": "answered",
                    "answer_summary": "resolvers seen",
                    "notes": "",
                },
                {
                    "question_id": "IP-001",
                    "answer_status": "unanswered",
                    "answer_summary": "",
                    "notes": "needs check",
                },
            ],
            "findings": [],
        },
        "pcap_derived": {"top_inet_pairs_sample": [{"src": "8.8.8.8", "dst": "1.2.3.4", "bytes": 9}]},
    }
    (loc / "normalized.json").write_text(json.dumps(norm), encoding="utf-8")

    md_path = generate_reports.generate_vpn_report("acme", vpn_name="Acme")
    html_path = md_path.with_suffix(".html")
    assert md_path.is_file()
    assert html_path.is_file()
    md_text = md_path.read_text(encoding="utf-8")
    assert "## SPEC question coverage (full table)" in md_text
    assert "one row per SPEC ID" in md_text
    assert "## Website and DNS surface (third-party exposure)" in md_text
    assert "website-exposure-methodology.md" in md_text
    assert "acmevpn.example" in md_text
    assert "#### Website & DNS surface (summary)" in md_text
    assert "#### PCAP host intelligence" in md_text
    assert "Scope test note." in md_text
    assert "dns.google" in md_text
    html = html_path.read_text(encoding="utf-8")
    assert "Coverage and graph" in html
    assert "strictest" in html
    assert "SPEC framework coverage" in html
    assert "Exposure graph" in html
    assert "How to read" in html
    assert "nodeThreeObjectExtend" in html
    assert "graph_schema" in html
    assert "stacked-bar" in html
    assert "report-appendix" in html
    assert "Full narrative export" in html
    assert "Benchmark locations" in html
    assert "loc-section-hint" in html
    assert "Exit IPv6" in html
    assert "loc-grid" in html
    assert 'class="loc-title"' in html
    assert 'title="L1"' in html
    assert "spec-q" in html
    assert "resolvers seen" in html
    assert "../style/icons/" in html
    assert "spec-cat-count" in html
    assert "Website and DNS surface" in html
    assert "web-exposure-table" in html
    assert "Surface URL matrix" in html


def test_generate_vpn_report_progress_callback(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from vpn_leaks.reporting import generate_reports

    def fake_root() -> Path:
        return tmp_path

    monkeypatch.setattr("vpn_leaks.config_loader.repo_root", fake_root)
    monkeypatch.setattr("vpn_leaks.reporting.generate_reports.repo_root", fake_root)
    monkeypatch.setattr("vpn_leaks.reporting.exposure_graph.repo_root", fake_root)

    loc = tmp_path / "runs" / "r1" / "locations" / "loc1"
    loc.mkdir(parents=True)
    norm = {
        "vpn_provider": "acme",
        "vpn_location_id": "loc1",
        "vpn_location_label": "L1",
        "schema_version": "1.2",
        "exit_ip_v4": "1.2.3.4",
        "exit_ip_sources": [],
        "dns_servers_observed": [],
        "webrtc_candidates": [],
        "attribution": {"asn": 64496, "holder": "Test"},
        "policies": [],
        "services_contacted": [],
        "artifacts": {},
        "extra": {},
    }
    (loc / "normalized.json").write_text(json.dumps(norm), encoding="utf-8")

    calls: list[str] = []
    out = generate_reports.generate_vpn_report("acme", progress_step=calls.append)
    assert out.is_file()
    assert calls == [
        "Report: collect normalized runs",
        "Report: build location matrix",
        "Report: build detailed sections",
        "Report: framework rollup",
        "Report: web exposure rollup",
        "Report: render markdown",
        "Report: write markdown",
        "Report: build exposure graph",
        "Report: build HTML dashboard",
        "Report: render HTML",
        "Report: write HTML",
    ]
