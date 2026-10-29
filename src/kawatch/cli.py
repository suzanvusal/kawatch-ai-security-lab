"""Command-line interface for the local Kawatch demo."""

import http.client
from pathlib import Path

from kawatch.http_client import fetch_local_headers
from kawatch.report import save_assessment_report
from kawatch.security_headers import (
    SecurityHeaderFinding,
    analyze_security_headers,
)

DEMO_URL = "http://127.0.0.1:8765"
REPORT_PATH = Path("reports/latest-assessment.json")


def assess_url(
    url: str,
) -> tuple[int, list[SecurityHeaderFinding]]:
    """Collect and analyze headers from an allowed local HTTP server."""
    response = fetch_local_headers(url)

    findings = analyze_security_headers(
        response.headers,
        is_https=response.is_https,
    )

    return response.status_code, findings


def main() -> None:
    """Run and save a local security assessment."""
    print("Kawatch AI Security Lab")
    print(f"Assessing local demo: {DEMO_URL}")
    print("-" * 40)

    try:
        status_code, findings = assess_url(DEMO_URL)

        saved_path = save_assessment_report(
            url=DEMO_URL,
            status_code=status_code,
            findings=findings,
            output_path=REPORT_PATH,
        )

    except (OSError, http.client.HTTPException, ValueError) as error:
        print(f"Assessment failed: {error}")
        print("Make sure the local demo server is running.")
        return

    print(f"HTTP status: {status_code}")
    print(f"Findings: {len(findings)}")
    print(f"Report saved to: {saved_path}")
    print()

    if not findings:
        print("No missing security headers were detected.")
        return

    for finding in findings:
        print(f"[{finding.severity}] {finding.header}")
        print(f"  Finding: {finding.message}")
        print(f"  Recommendation: {finding.recommendation}")
        print()


if __name__ == "__main__":
    main()
