"""Tests for SPEC framework synthesis."""

from __future__ import annotations

from vpn_leaks.framework.coverage import build_question_coverage
from vpn_leaks.framework.findings import build_findings
from vpn_leaks.framework.load import load_question_bank
from vpn_leaks.framework.scoring import score_risk
from vpn_leaks.framework.synthesize import apply_framework, synthesize_framework_result
from vpn_leaks.models import NormalizedRun


def test_synthesize_framework_minimal() -> None:
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        exit_ip_v4="198.51.100.1",
        dns_leak_flag=False,
        webrtc_leak_flag=False,
        ipv6_leak_flag=False,
    )
    fw = synthesize_framework_result(run)
    assert fw.question_bank_version
    assert len(fw.question_coverage) >= 1
    assert fw.risk_scores.overall_severity in ("INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert any(f.category == "summary" for f in fw.findings)


def test_apply_framework_bumps_embed() -> None:
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        dns_leak_flag=True,
    )
    out = apply_framework(run)
    assert out.framework is not None
    assert any(f.severity == "CRITICAL" for f in out.framework.findings)


def test_coverage_dns_question() -> None:
    _, qs = load_question_bank()
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        dns_servers_observed=[],
    )
    cov = build_question_coverage(run, qs)
    dns_rows = [c for c in cov if c.question_id == "DNS-001"]
    assert len(dns_rows) == 1
    assert dns_rows[0].answer_status == "unanswered"


def test_score_risk_dns_leak() -> None:
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        dns_leak_flag=True,
    )
    findings = build_findings(run)
    rs = score_risk(run, findings)
    assert rs.leak_severity == "CRITICAL"


def test_build_framework_rollup_import() -> None:
    from vpn_leaks.reporting.generate_reports import build_framework_rollup

    p = __import__("pathlib").Path("x/loc/normalized.json")
    data = {
        "framework": {
            "risk_scores": {"overall_severity": "LOW"},
            "question_coverage": [
                {"answer_status": "answered"},
                {"answer_status": "partially_answered"},
            ],
            "findings": [{"severity": "HIGH", "title": "t"}],
        },
    }
    r = build_framework_rollup([("run1", p, data)])
    assert r["has_framework"] is True
    assert r["coverage_counts"]["answered"] == 1
