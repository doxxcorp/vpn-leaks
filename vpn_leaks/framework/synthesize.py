"""Build FrameworkResult for embedding in NormalizedRun."""

from __future__ import annotations

from vpn_leaks.framework.coverage import build_question_coverage
from vpn_leaks.framework.endpoints import collect_observed_endpoints
from vpn_leaks.framework.findings import build_findings
from vpn_leaks.framework.load import load_classification_rules, load_question_bank, load_test_matrix
from vpn_leaks.framework.scoring import score_risk
from vpn_leaks.models import FrameworkResult, NormalizedRun


def synthesize_framework_result(run: NormalizedRun) -> FrameworkResult:
    qb_ver, questions = load_question_bank()
    mx_ver, _ = load_test_matrix()
    rules = load_classification_rules()

    findings = build_findings(run)
    coverage = build_question_coverage(run, questions)
    endpoints = collect_observed_endpoints(run, rules)
    risk = score_risk(run, findings)

    return FrameworkResult(
        question_bank_version=qb_ver,
        test_matrix_version=mx_ver,
        findings=findings,
        question_coverage=coverage,
        risk_scores=risk,
        observed_endpoints=endpoints,
    )


def apply_framework(run: NormalizedRun) -> NormalizedRun:
    """Return a copy of run with framework populated."""
    fw = synthesize_framework_result(run)
    return run.model_copy(update={"framework": fw, "schema_version": "1.4"})
