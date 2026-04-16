"""Tests for compact benchmark location labels."""

from __future__ import annotations

from vpn_leaks.reporting.benchmark_location import format_benchmark_location_display
from vpn_leaks.reporting.coverage_rollup import compute_next_steps
from vpn_leaks.reporting.html_dashboard import _spec_list_preview


def test_format_from_exit_geo_us() -> None:
    data = {
        "vpn_location_label": "ignored if geo present",
        "extra": {
            "exit_geo": {
                "city": "San Francisco",
                "region": "California",
                "country_code": "US",
            },
        },
    }
    assert format_benchmark_location_display(data) == "San Francisco, CA, USA"


def test_format_from_label_three_part_us() -> None:
    data = {
        "vpn_location_label": "San Francisco, California, United States",
    }
    assert format_benchmark_location_display(data) == "San Francisco, CA, USA"


def test_format_from_label_two_part() -> None:
    data = {"vpn_location_label": "London, United Kingdom"}
    assert format_benchmark_location_display(data) == "London, GB, GBR"


def test_spec_list_preview_answered() -> None:
    assert (
        _spec_list_preview(
            {
                "answer_status": "answered",
                "answer_summary": "Done.",
                "next_steps": "—",
            },
        )
        == "Done."
    )


def test_spec_list_preview_unanswered_uses_next_steps() -> None:
    assert (
        _spec_list_preview(
            {
                "answer_status": "unanswered",
                "answer_summary": "",
                "next_steps": "Run the harness again.",
            },
        )
        == "Run the harness again."
    )


def test_spec_list_preview_partial_combines() -> None:
    s = _spec_list_preview(
        {
            "answer_status": "partially_answered",
            "answer_summary": "Partial evidence.",
            "next_steps": "Collect more HAR.",
        },
    )
    assert "Partial evidence." in s
    assert "Collect more HAR." in s


def test_compute_next_steps_gap_fallback() -> None:
    s = compute_next_steps(
        {
            "question_id": "X-001",
            "answer_status": "unanswered",
            "notes": "",
            "testability": "DYNAMIC_FULL",
        },
        {},
    )
    assert "research-questions-and-evidence.md" in s
    assert "RUN-STEPS.md" in s
    assert "X-001" in s
