"""Summarize validated Kawatch security assessment reports."""

import json
from pathlib import Path
from typing import Any

from kawatch.validation import validate_report


def summarize_history(history_dir: Path) -> dict[str, Any]:
    """Summarize valid reports and identify invalid report files."""
    report_files = sorted(history_dir.glob("assessment-*.json"))

    reports = []
    invalid_reports = []

    for report_file in report_files:
        try:
            report = json.loads(report_file.read_text(encoding="utf-8"))
            errors = validate_report(report)
        except (OSError, json.JSONDecodeError) as error:
            errors = [f"Could not read JSON report: {error}"]

        if errors:
            invalid_reports.append(
                {
                    "file": report_file.name,
                    "errors": errors,
                }
            )
            continue

        reports.append(report)

    if not reports:
        return {
            "total_assessments": 0,
            "total_findings": 0,
            "severity": {"high": 0, "medium": 0, "low": 0},
            "latest_assessment": None,
            "finding_change": None,
            "invalid_reports": invalid_reports,
        }

    total_findings = 0
    severity = {"high": 0, "medium": 0, "low": 0}

    for report in reports:
        summary = report["summary"]
        total_findings += summary["total_findings"]

        for level in severity:
            severity[level] += summary[level]

    latest_assessment = reports[-1]

    finding_change = None

    if len(reports) >= 2:
        previous_count = reports[-2]["summary"]["total_findings"]
        latest_count = latest_assessment["summary"]["total_findings"]
        finding_change = latest_count - previous_count

    return {
        "total_assessments": len(reports),
        "total_findings": total_findings,
        "severity": severity,
        "latest_assessment": latest_assessment["generated_at"],
        "finding_change": finding_change,
        "invalid_reports": invalid_reports,
    }


def main() -> None:
    """Print a summary of historical assessments."""
    summary = summarize_history(Path("reports/history"))

    print("Kawatch Assessment History")
    print("-" * 40)
    print(f"Valid assessments: {summary['total_assessments']}")
    print(f"Total findings: {summary['total_findings']}")

    print("Severity breakdown:")
    for level, count in summary["severity"].items():
        print(f"  {level.title()}: {count}")

    print(f"Latest assessment: {summary['latest_assessment']}")

    change = summary["finding_change"]

    if change is None:
        print("Finding change: Not enough valid assessments to compare.")
    elif change > 0:
        print(f"Finding change: Increased by {change}")
    elif change < 0:
        print(f"Finding change: Decreased by {abs(change)}")
    else:
        print("Finding change: No change")

    invalid_reports = summary["invalid_reports"]
    print(f"Invalid reports skipped: {len(invalid_reports)}")

    for report in invalid_reports:
        print(f"\nInvalid file: {report['file']}")
        for error in report["errors"]:
            print(f"  - {error}")


if __name__ == "__main__":
    main()
