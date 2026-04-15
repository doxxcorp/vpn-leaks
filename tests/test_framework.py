"""Tests for SPEC framework synthesis."""

from __future__ import annotations

from vpn_leaks.framework.coverage import build_question_coverage
from vpn_leaks.framework.findings import build_findings
from vpn_leaks.framework.load import load_question_bank
from vpn_leaks.framework.scoring import score_risk
from vpn_leaks.framework.synthesize import apply_framework, synthesize_framework_result
from vpn_leaks.models import ArtifactIndex, CompetitorSurfaceSnapshot, ExitIpSource, NormalizedRun


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


def test_coverage_web004_portal_probes_count() -> None:
    """WEB-004 should succeed when only portal_probes are present (not only web_probes)."""
    _, qs = load_question_bank()
    cs = CompetitorSurfaceSnapshot(
        web_probes=[],
        portal_probes=[{"host": "portal.example.com", "status": 200}],
    )
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        competitor_surface=cs,
    )
    cov = build_question_coverage(run, qs)
    row = next(c for c in cov if c.question_id == "WEB-004")
    assert row.answer_status == "partially_answered"
    assert "portal" in row.answer_summary.lower()


def test_coverage_fp001_browserleaks_without_fingerprint_dict() -> None:
    _, qs = load_question_bank()
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        fingerprint_snapshot={},
        browserleaks_snapshot={"pages": [{"url": "https://browserleaks.com/ip"}]},
    )
    cov = build_question_coverage(run, qs)
    row = next(c for c in cov if c.question_id == "FP-001")
    assert row.answer_status == "partially_answered"
    assert "browserleaks" in row.answer_summary.lower()


def test_coverage_ip014_agreement_summary() -> None:
    _, qs = load_question_bank()
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        exit_ip_sources=[
            ExitIpSource(url="https://a.example", ipv4="198.51.100.1"),
            ExitIpSource(url="https://b.example", ipv4="198.51.100.1"),
        ],
    )
    cov = build_question_coverage(run, qs)
    row = next(c for c in cov if c.question_id == "IP-014")
    assert "agree" in row.answer_summary.lower()


def test_coverage_exit005_geo_matches_label() -> None:
    _, qs = load_question_bank()
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="us-nm-1",
        vpn_location_label="Albuquerque, New Mexico, United States",
        extra={
            "exit_geo": {
                "location_label": "Albuquerque, New Mexico, United States",
                "city": "Albuquerque",
                "region": "New Mexico",
                "country_code": "US",
            },
        },
    )
    cov = build_question_coverage(run, qs)
    row = next(c for c in cov if c.question_id == "EXIT-005")
    assert "consistent" in row.answer_summary.lower()


def test_coverage_exit004_reads_exit_dns_json() -> None:
    _, qs = load_question_bank()
    run = NormalizedRun(
        run_id="r1",
        vpn_provider="example",
        vpn_location_id="loc1",
        artifacts=ArtifactIndex(exit_dns_json="tests/fixtures/exit_dns_no_ptr.json"),
    )
    cov = build_question_coverage(run, qs)
    row = next(c for c in cov if c.question_id == "EXIT-004")
    assert row.answer_status == "partially_answered"
    assert "no reverse dns" in row.answer_summary.lower() or "PTR lookup completed" in row.answer_summary


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
                {
                    "question_id": "DNS-001",
                    "answer_status": "answered",
                    "answer_summary": "resolvers seen",
                    "notes": None,
                },
                {
                    "question_id": "IP-001",
                    "answer_status": "partially_answered",
                    "answer_summary": "exit v4",
                    "notes": None,
                },
            ],
            "findings": [{"severity": "HIGH", "title": "t"}],
        },
    }
    r = build_framework_rollup([("run1", p, data)])
    assert r["has_framework"] is True
    assert r["merged_question_count"] == 42
    assert r["coverage_counts"]["answered"] == 1
    assert r["coverage_counts"]["partially_answered"] == 1
    assert r["coverage_counts"]["unanswered"] == 40
    total = sum(r["coverage_counts"].values())
    assert total == 42
    dns_merged = next(x for x in r["merged_coverage"] if x["question_id"] == "DNS-001")
    assert dns_merged["answer_status"] == "answered"


def test_build_framework_rollup_merge_worst_status() -> None:
    """Across two locations, unanswered for a question beats answered."""
    from vpn_leaks.reporting.generate_reports import build_framework_rollup

    p = __import__("pathlib").Path("x/loc/normalized.json")
    qc_a = {
        "question_id": "WEB-001",
        "answer_status": "answered",
        "answer_summary": "from loc a",
        "notes": "",
    }
    qc_b = {
        "question_id": "WEB-001",
        "answer_status": "unanswered",
        "answer_summary": "",
        "notes": "Configure competitor_probe.provider_domains.",
    }
    fw = {"risk_scores": {"overall_severity": "LOW"}, "question_coverage": [qc_a], "findings": []}
    fw2 = dict(fw)
    fw2["question_coverage"] = [qc_b]
    r = build_framework_rollup([("run1", p, {"framework": fw}), ("run2", p, {"framework": fw2})])
    web = next(x for x in r["merged_coverage"] if x["question_id"] == "WEB-001")
    assert web["answer_status"] == "unanswered"
