"""Tests for historical assessment summaries."""

import json

from kawatch.history import summarize_history


def create_report(directory, filename, generated_at, total, high, medium, low):
    """Create a valid sample historical assessment report."""
    findings = []

    for severity, count in (
        ("High", high),
        ("Medium", medium),
        ("Low", low),
    ):
        for index in range(count):
            findings.append(
                {
                    "header": f"test-header-{severity.lower()}-{index}",
                    "severity": severity,
                    "message": "Test finding.",
                    "recommendation": "Review the relevant configuration.",
                }
            )

    report = {
        "project": "Kawatch AI Security Lab",
        "generated_at": generated_at,
        "target": "http://127.0.0.1:8765",
        "http_status": 200,
        "summary": {
            "total_findings": total,
            "high": high,
            "medium": medium,
            "low": low,
        },
        "findings": findings,
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
    assert summary["invalid_reports"] == []


def test_history_summarizes_multiple_assessments(tmp_path):
    """The summary should combine valid reports and compare recent ones."""
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
    assert summary["invalid_reports"] == []


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


def test_invalid_report_is_skipped(tmp_path):
    """Invalid reports should be excluded and reported."""
    create_report(
        tmp_path,
        "assessment-20261029-100000-000000.json",
        "2026-10-29T10:00:00+00:00",
        2, 0, 1, 1,
    )

    invalid_path = tmp_path / "assessment-20261029-110000-000000.json"
    invalid_path.write_text(
        json.dumps({"project": "Incomplete report"}),
        encoding="utf-8",
    )

    summary = summarize_history(tmp_path)

    assert summary["total_assessments"] == 1
    assert summary["total_findings"] == 2
    assert len(summary["invalid_reports"]) == 1
    assert summary["invalid_reports"][0]["file"] == invalid_path.name


def test_malformed_json_is_skipped(tmp_path):
    """Unreadable JSON should be reported without stopping the summary."""
    invalid_path = tmp_path / "assessment-20261029-100000-000000.json"
    invalid_path.write_text("{not valid JSON", encoding="utf-8")

    summary = summarize_history(tmp_path)

    assert summary["total_assessments"] == 0
    assert len(summary["invalid_reports"]) == 1
    assert "Could not read JSON report" in (
        summary["invalid_reports"][0]["errors"][0]
    )
