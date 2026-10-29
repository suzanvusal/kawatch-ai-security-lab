"""Tests for JSON security assessment reports."""

import json

from kawatch.report import save_assessment_report
from kawatch.security_headers import SecurityHeaderFinding


def test_save_assessment_report(tmp_path):
    """The report should contain assessment details and findings."""

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

    output_path = tmp_path / "reports" / "assessment.json"

    saved_path = save_assessment_report(
        url="http://127.0.0.1:8765",
        status_code=200,
        findings=findings,
        output_path=output_path,
    )

    assert saved_path.exists()

    report = json.loads(saved_path.read_text(encoding="utf-8"))

    assert report["target"] == "http://127.0.0.1:8765"
    assert report["http_status"] == 200
    assert report["summary"]["total_findings"] == 2
    assert report["summary"]["medium"] == 1
    assert report["summary"]["low"] == 1
    assert len(report["findings"]) == 2
