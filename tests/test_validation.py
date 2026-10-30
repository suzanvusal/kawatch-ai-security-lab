"""Tests for Kawatch assessment report validation."""

from kawatch.validation import validate_report


def valid_report():
    """Return a valid sample assessment report."""
    return {
        "project": "Kawatch AI Security Lab",
        "generated_at": "2026-10-30T12:00:00+00:00",
        "target": "http://127.0.0.1:8765",
        "http_status": 200,
        "summary": {
            "total_findings": 1,
            "high": 0,
            "medium": 1,
            "low": 0,
        },
        "findings": [
            {
                "header": "content-security-policy",
                "severity": "Medium",
                "message": "Content Security Policy is missing.",
                "recommendation": "Define a suitable policy.",
            }
        ],
    }


def test_valid_report_has_no_errors():
    """A correctly structured report should pass validation."""
    assert validate_report(valid_report()) == []


def test_report_rejects_inconsistent_severity_counts():
    """Severity counts must add up to the total findings."""
    report = valid_report()
    report["summary"]["medium"] = 0

    errors = validate_report(report)

    assert "Severity counts must equal total_findings." in errors


def test_report_rejects_invalid_finding_severity():
    """Findings must use a supported severity."""
    report = valid_report()
    report["findings"][0]["severity"] = "Critical"

    errors = validate_report(report)

    assert "Finding 0 has an unsupported severity." in errors


def test_report_rejects_missing_required_fields():
    """A report missing required fields should fail validation."""
    errors = validate_report({"project": "Kawatch"})

    assert "Missing required field: generated_at" in errors
    assert "Missing required field: findings" in errors


def test_report_rejects_non_object_input():
    """The validator should handle non-object input safely."""
    assert validate_report([]) == ["Report must be a JSON object."]


def test_report_rejects_finding_count_mismatch():
    """The number of finding records must match the summary."""
    report = valid_report()
    report["findings"] = []

    errors = validate_report(report)

    assert "The number of findings must equal total_findings." in errors
