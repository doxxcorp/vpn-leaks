"""Merge SPEC question coverage across benchmark rows and build report narratives."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from vpn_leaks.config_loader import load_yaml, repo_root
from vpn_leaks.framework.load import QuestionDef, load_question_bank

# Strictest status wins across locations (plan: unanswered > partial > answered > not_testable_dynamically).
_STATUS_RANK: dict[str, int] = {
    "unanswered": 3,
    "partially_answered": 2,
    "answered": 1,
    "not_testable_dynamically": 0,
}


def _rank(status: str | None) -> int:
    if not status:
        return -1
    return _STATUS_RANK.get(str(status), -1)


def _report_hints_path() -> Path:
    return repo_root() / "configs" / "framework" / "report_hints.yaml"


def load_report_hints() -> dict[str, str]:
    """Return question_id -> hint string from configs/framework/report_hints.yaml."""
    path = _report_hints_path()
    data = load_yaml(path) if path.is_file() else {}
    raw = data.get("hints") or {}
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for k, v in raw.items():
        if v is None:
            continue
        out[str(k)] = str(v).strip()
    return out


def _collect_qc_by_id(rows: list[tuple[str, Path, dict[str, Any]]]) -> dict[str, list[dict[str, Any]]]:
    """question_id -> all question_coverage dicts from runs that have a framework block."""
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for _rid, _p, data in rows:
        fw = data.get("framework")
        if not fw:
            continue
        for qc in fw.get("question_coverage") or []:
            if not isinstance(qc, dict):
                continue
            qid = str(qc.get("question_id") or "").strip()
            if not qid:
                continue
            by_id[qid].append(qc)
    return by_id


def merge_question_coverage_rows(
    rows: list[tuple[str, Path, dict[str, Any]]],
    questions: list[QuestionDef],
) -> list[dict[str, Any]]:
    """One merged row per question in bank order; worst status across benchmark rows wins."""
    by_id = _collect_qc_by_id(rows)
    merged: list[dict[str, Any]] = []
    for q in questions:
        group = by_id.get(q.id) or []
        if not group:
            merged.append(
                {
                    "question_id": q.id,
                    "question_text": q.text,
                    "category": q.category,
                    "testability": q.testability,
                    "answer_status": "unanswered",
                    "answer_summary": "",
                    "notes": "No question_coverage row for this ID in any framework block.",
                },
            )
            continue
        best = group[0]
        best_r = _rank(best.get("answer_status"))
        for qc in group[1:]:
            r = _rank(qc.get("answer_status"))
            if r > best_r:
                best = qc
                best_r = r
            elif r == best_r:
                # Prefer richer summary on tie
                s0 = str(best.get("answer_summary") or "").strip()
                s1 = str(qc.get("answer_summary") or "").strip()
                if len(s1) > len(s0):
                    best = qc
        notes_parts: list[str] = []
        n0 = str(best.get("notes") or "").strip()
        if n0:
            notes_parts.append(n0)
        for qc in group:
            if _rank(qc.get("answer_status")) != best_r:
                continue
            n = str(qc.get("notes") or "").strip()
            if n and n not in notes_parts:
                notes_parts.append(n)
        merged.append(
            {
                "question_id": q.id,
                "question_text": q.text,
                "category": q.category,
                "testability": q.testability,
                "answer_status": str(best.get("answer_status") or "unanswered"),
                "answer_summary": str(best.get("answer_summary") or "").strip(),
                "notes": " ".join(notes_parts).strip(),
            },
        )
    return merged


def count_coverage_statuses(merged: list[dict[str, Any]]) -> dict[str, int]:
    out = {
        "answered": 0,
        "partially_answered": 0,
        "unanswered": 0,
        "not_testable_dynamically": 0,
    }
    for m in merged:
        st = m.get("answer_status")
        if st in out:
            out[str(st)] += 1
    return out


def compute_next_steps(
    row: dict[str, Any],
    hints: dict[str, str],
) -> str:
    qid = str(row.get("question_id") or "")
    status = str(row.get("answer_status") or "")
    notes = str(row.get("notes") or "").strip()
    hint = hints.get(qid, "").strip()
    testability = str(row.get("testability") or "unknown").strip()

    if status == "not_testable_dynamically":
        if hint:
            return hint
        return (
            "Not verifiable by this harness alone; see "
            "docs/research-questions-and-evidence.md (evidence tiers)."
        )
    if status == "answered":
        return "—"
    # partial or unanswered
    if notes and hint:
        if notes in hint or hint.startswith(notes):
            combined = hint
        elif hint in notes:
            combined = notes
        else:
            combined = f"{notes} — {hint}"
    else:
        combined = notes or hint or ""

    if combined and combined != "—":
        return combined

    return (
        f"See docs/research-questions-and-evidence.md for {qid or '?'} "
        f"(testability: {testability}); follow RUN-STEPS.md to extend the harness or add "
        "desk/document evidence (S/D)."
    )


def _sanitize_table_cell(s: str) -> str:
    """Avoid breaking Markdown tables (pipes, newlines)."""
    return " ".join(str(s).replace("|", "/").split()).strip()


def enrich_merged_with_next_steps(
    merged: list[dict[str, Any]],
    hints: dict[str, str],
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for m in merged:
        row = dict(m)
        row["next_steps"] = compute_next_steps(row, hints)
        row["answer_summary_display"] = _sanitize_table_cell(str(row.get("answer_summary") or ""))
        row["next_steps_display"] = _sanitize_table_cell(row["next_steps"])
        row["question_text_display"] = _sanitize_table_cell(str(row.get("question_text") or ""))
        out.append(row)
    return out


def build_coverage_analysis_markdown(
    merged: list[dict[str, Any]],
    rows: list[tuple[str, Path, dict[str, Any]]],
    top_findings: list[dict[str, Any]],
    max_overall_severity: str,
) -> str:
    """Deterministic narrative: scope, findings, by-category bullets, limitations."""
    lines: list[str] = [
        "### Scope",
        "",
        f"- **Benchmark rows in this report:** {len(rows)} (one row per `normalized.json` location).",
        (
            "- **Merge rule:** For each SPEC question ID, the status shown in the table is the "
            "**strictest** across rows: unanswered > partially_answered > answered > "
            "not_testable_dynamically."
        ),
        "",
        "### Risk and findings",
        "",
        f"- **Rollup severity (max across runs):** `{max_overall_severity}`",
    ]
    if top_findings:
        lines.append("- **HIGH / CRITICAL framework findings:**")
        for f in top_findings[:25]:
            title = str(f.get("title") or "")
            sev = str(f.get("severity") or "")
            cat = str(f.get("category") or "")
            lines.append(f"  - **[{sev}]** {title} ({cat})")
    else:
        lines.append("- **HIGH / CRITICAL framework findings:** none in this rollup.")
    lines.extend(["", "### By category (merged coverage)", ""])

    by_cat: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in merged:
        by_cat[str(m.get("category") or "unknown")].append(m)

    for cat in sorted(by_cat.keys()):
        lines.append(f"#### {cat}")
        lines.append("")
        for m in sorted(by_cat[cat], key=lambda x: str(x.get("question_id") or "")):
            qid = m.get("question_id")
            st = m.get("answer_status")
            summ = str(m.get("answer_summary") or "").strip()
            if st == "answered" and summ:
                lines.append(f"- **{qid}** (answered): {summ}")
            elif st == "partially_answered":
                extra = summ or str(m.get("notes") or "").strip() or "(no summary)"
                lines.append(f"- **{qid}** (partial): {extra}")
            elif st == "unanswered":
                nu = str(m.get("notes") or "").strip() or "(unanswered — see Next steps in table)"
                lines.append(f"- **{qid}** (unanswered): {nu}")
            else:
                lines.append(
                    f"- **{qid}** (`{st}`): {summ or 'see harness limits; Next steps column'}",
                )
        lines.append("")

    any_dns = any(bool(r[2].get("dns_leak_flag")) for r in rows)
    any_wrtc = any(bool(r[2].get("webrtc_leak_flag")) for r in rows)
    any_v6 = any(bool(r[2].get("ipv6_leak_flag")) for r in rows)

    lines.extend(
        [
            "### Limitations",
            "",
            (
                "- Leak flags and DNS notes are **heuristic / harness-defined**; read raw "
                "`runs/.../raw/` artifacts for full context."
            ),
            (
                f"- **Observed leak flags (any location):** DNS={any_dns}, WebRTC={any_wrtc}, "
                f"IPv6={any_v6}."
            ),
            (
                "- **App telemetry (TELEM-001, TELEM-004)** and some control-plane details are "
                "**not** proven by browser-only harness paths; use **D** (documents) or external "
                "traffic studies where applicable."
            ),
            (
                "- **Desk research (S)** (e.g. apex `dig`, glue WHOIS) is not auto-merged into "
                "this report; compare to `competitor_probe` / provider DNS when both exist."
            ),
            "",
        ],
    )
    return "\n".join(lines).rstrip() + "\n"


def build_framework_rollup_payload(
    rows: list[tuple[str, Path, dict[str, Any]]],
) -> dict[str, Any]:
    """Full framework rollup: merged 42-question coverage, counts, gaps, analysis text."""
    _, questions = load_question_bank()
    total_q = len(questions)
    top_findings: list[dict[str, Any]] = []
    order = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]

    def mx(a: str, b: str) -> str:
        try:
            return a if order.index(a) >= order.index(b) else b
        except ValueError:
            return b

    max_overall = "INFO"
    has_fw = False
    for _rid, _p, data in rows:
        fw = data.get("framework")
        if not fw:
            continue
        has_fw = True
        rs = fw.get("risk_scores") or {}
        max_overall = mx(max_overall, str(rs.get("overall_severity") or "INFO"))
        for f in fw.get("findings") or []:
            if not isinstance(f, dict):
                continue
            if f.get("severity") in ("HIGH", "CRITICAL"):
                top_findings.append(f)

    empty_counts = {
        "answered": 0,
        "partially_answered": 0,
        "unanswered": 0,
        "not_testable_dynamically": 0,
    }

    if not has_fw:
        return {
            "has_framework": False,
            "coverage_counts": empty_counts,
            "merged_question_count": 0,
            "question_bank_count": total_q,
            "max_overall_severity": max_overall,
            "top_findings": top_findings[:25],
            "merged_coverage": [],
            "gap_rows": [],
            "coverage_analysis_md": (
                "### Scope\n\n"
                "*No `framework` block on these `normalized.json` files — regenerate runs "
                "without `--no-framework` (default) or re-run `vpn-leaks run` on a current build.*\n"
            ),
        }

    merged_raw = merge_question_coverage_rows(rows, questions)
    hints = load_report_hints()
    merged = enrich_merged_with_next_steps(merged_raw, hints)
    coverage_counts = count_coverage_statuses(merged)

    gap_rows = [
        m
        for m in merged
        if m.get("answer_status") in ("unanswered", "partially_answered")
    ]

    analysis_md = build_coverage_analysis_markdown(
        merged,
        rows,
        top_findings[:25],
        max_overall,
    )

    merged_total = len(merged)

    return {
        "has_framework": True,
        "coverage_counts": coverage_counts,
        "merged_question_count": merged_total,
        "question_bank_count": total_q,
        "max_overall_severity": max_overall,
        "top_findings": top_findings[:25],
        "merged_coverage": merged,
        "gap_rows": gap_rows,
        "coverage_analysis_md": analysis_md,
    }
