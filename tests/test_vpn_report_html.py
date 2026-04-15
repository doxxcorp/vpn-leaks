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
        "framework": {
            "risk_scores": {"overall_severity": "LOW"},
            "question_coverage": [
                {"answer_status": "answered"},
                {"answer_status": "unanswered"},
            ],
            "findings": [],
        },
    }
    (loc / "normalized.json").write_text(json.dumps(norm), encoding="utf-8")

    md_path = generate_reports.generate_vpn_report("acme", vpn_name="Acme")
    html_path = md_path.with_suffix(".html")
    assert md_path.is_file()
    assert html_path.is_file()
    html = html_path.read_text(encoding="utf-8")
    assert "Visualizations" in html
    assert "SPEC framework coverage" in html
    assert "Exposure graph" in html
    assert "graph_schema" in html
    assert "stacked-bar" in html
    assert "<article" in html or "report-body" in html
