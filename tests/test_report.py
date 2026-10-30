"""Tests for JSON security assessment reports."""

import json

from kawatch.report import save_assessment_report
from kawatch.security_headers import SecurityHeaderFinding


def test_save_assessment_report(tmp_path):
    """The latest and historical reports should contain assessment details."""

    findings = [
        SecurityHeaderFinding(
            header="content-security-policy",
            severity="Medium",
            message="Content Security Policy is missing.",
            recommendation="Define a suitable Content Security Policy.",
        ),
        SecurityHeaderFinding(
            header="referrer-policy",
            severity="Low",
            message="Referrer-Policy is missing.",
            recommendation="Set an appropriate Referrer-Policy.",
        ),
    ]

    output_path = tmp_path / "reports" / "latest-assessment.json"

    saved_path = save_assessment_report(
        url="http://127.0.0.1:8765",
        status_code=200,
        findings=findings,
        output_path=output_path,
    )

    assert saved_path.exists()

    latest_report = json.loads(
        saved_path.read_text(encoding="utf-8")
    )

    assert latest_report["target"] == "http://127.0.0.1:8765"
    assert latest_report["http_status"] == 200
    assert latest_report["summary"]["total_findings"] == 2
    assert latest_report["summary"]["medium"] == 1
    assert latest_report["summary"]["low"] == 1
    assert len(latest_report["findings"]) == 2

    history_dir = tmp_path / "reports" / "history"
    history_files = list(history_dir.glob("assessment-*.json"))

    assert len(history_files) == 1

    historical_report = json.loads(
        history_files[0].read_text(encoding="utf-8")
    )

    assert historical_report == latest_report
