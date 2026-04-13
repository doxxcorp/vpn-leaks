"""Load framework question bank, test matrix, and classification rules."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from vpn_leaks.config_loader import load_yaml, repo_root


@dataclass(frozen=True)
class QuestionDef:
    id: str
    category: str
    text: str
    testability: str


@dataclass(frozen=True)
class TestMatrixRow:
    question_id: str
    test_method: str
    automation_level: str
    tools: list[str]
    expected_evidence: list[str]
    outcomes: dict[str, str]
    repetition_strategy: str
    environment_dependencies: list[str]


def _questions_path() -> Path:
    return repo_root() / "configs" / "framework" / "questions.yaml"


def _matrix_path() -> Path:
    return repo_root() / "configs" / "framework" / "test_matrix.yaml"


def _classification_path() -> Path:
    return repo_root() / "configs" / "framework" / "classification_rules.yaml"


def load_question_bank() -> tuple[str, list[QuestionDef]]:
    path = _questions_path()
    data = load_yaml(path) if path.is_file() else {}
    version = str(data.get("version") or "0")
    raw = data.get("questions") or []
    out: list[QuestionDef] = []
    for row in raw:
        if not isinstance(row, dict):
            continue
        qid = str(row.get("id") or "").strip()
        if not qid:
            continue
        out.append(
            QuestionDef(
                id=qid,
                category=str(row.get("category") or "unknown"),
                text=str(row.get("text") or ""),
                testability=str(row.get("testability") or "DYNAMIC_PARTIAL"),
            ),
        )
    return version, out


def load_test_matrix() -> tuple[str, dict[str, TestMatrixRow]]:
    path = _matrix_path()
    data = load_yaml(path) if path.is_file() else {}
    version = str(data.get("version") or "0")
    raw = data.get("matrix") or []
    by_id: dict[str, TestMatrixRow] = {}
    for row in raw:
        if not isinstance(row, dict):
            continue
        qid = str(row.get("question_id") or "").strip()
        if not qid:
            continue
        tools = row.get("tools") or []
        ev = row.get("expected_evidence") or []
        oc = row.get("outcomes") or {}
        env = row.get("environment_dependencies") or []
        by_id[qid] = TestMatrixRow(
            question_id=qid,
            test_method=str(row.get("test_method") or ""),
            automation_level=str(row.get("automation_level") or ""),
            tools=[str(x) for x in tools] if isinstance(tools, list) else [],
            expected_evidence=[str(x) for x in ev] if isinstance(ev, list) else [],
            outcomes=dict(oc) if isinstance(oc, dict) else {},
            repetition_strategy=str(row.get("repetition_strategy") or ""),
            environment_dependencies=[str(x) for x in env] if isinstance(env, list) else [],
        )
    return version, by_id


def load_classification_rules() -> dict[str, Any]:
    path = _classification_path()
    return load_yaml(path) if path.is_file() else {}
