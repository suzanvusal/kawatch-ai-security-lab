"""Tests for historical assessment summaries."""

import json

from kawatch.history import summarize_history


def create_report(directory, filename, generated_at, total, high, medium, low):
    """Create a sample historical assessment report."""
    report = {
        "generated_at": generated_at,
        "summary": {
            "total_findings": total,
            "high": high,
            "medium": medium,
            "low": low,
        },
    }

    (directory / filename).write_text(
        json.dumps(report),
        encoding="utf-8",
    )


def test_empty_history_returns_zero_summary(tmp_path):
    """An empty history directory should return zero counts."""
    summary = summarize_history(tmp_path)

    assert summary["total_assessments"] == 0
    assert summary["total_findings"] == 0
    assert summary["severity"] == {
        "high": 0,
        "medium": 0,
        "low": 0,
    }
    assert summary["latest_assessment"] is None
    assert summary["finding_change"] is None


def test_history_summarizes_multiple_assessments(tmp_path):
    """The summary should combine reports and compare the latest two."""
    create_report(
        tmp_path,
        "assessment-20261029-100000-000000.json",
        "2026-10-29T10:00:00+00:00",
        4, 1, 2, 1,
    )
    create_report(
        tmp_path,
        "assessment-20261029-110000-000000.json",
        "2026-10-29T11:00:00+00:00",
        2, 0, 1, 1,
    )
    create_report(
        tmp_path,
        "assessment-20261029-120000-000000.json",
        "2026-10-29T12:00:00+00:00",
        3, 1, 1, 1,
    )

    summary = summarize_history(tmp_path)

    assert summary["total_assessments"] == 3
    assert summary["total_findings"] == 9
    assert summary["severity"] == {
        "high": 2,
        "medium": 4,
        "low": 3,
    }
    assert summary["latest_assessment"] == "2026-10-29T12:00:00+00:00"
    assert summary["finding_change"] == 1


def test_single_assessment_has_no_comparison(tmp_path):
    """One report is not enough to calculate a change."""
    create_report(
        tmp_path,
        "assessment-20261029-100000-000000.json",
        "2026-10-29T10:00:00+00:00",
        2, 0, 1, 1,
    )

    summary = summarize_history(tmp_path)

    assert summary["total_assessments"] == 1
    assert summary["finding_change"] is None
