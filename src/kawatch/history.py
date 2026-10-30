"""Summarize historical Kawatch security assessment reports."""

import json
from pathlib import Path
from typing import Any


def summarize_history(history_dir: Path) -> dict[str, Any]:
    """Summarize saved assessment reports in chronological order."""
    report_files = sorted(history_dir.glob("assessment-*.json"))

    reports = []

    for report_file in report_files:
        report = json.loads(report_file.read_text(encoding="utf-8"))
        reports.append(report)

    if not reports:
        return {
            "total_assessments": 0,
            "total_findings": 0,
            "severity": {"high": 0, "medium": 0, "low": 0},
            "latest_assessment": None,
            "finding_change": None,
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
    }


def main() -> None:
    """Print a summary of historical assessments."""
    history_dir = Path("reports/history")
    summary = summarize_history(history_dir)

    print("Kawatch Assessment History")
    print("-" * 40)
    print(f"Total assessments: {summary['total_assessments']}")
    print(f"Total findings: {summary['total_findings']}")

    print("Severity breakdown:")
    for level, count in summary["severity"].items():
        print(f"  {level.title()}: {count}")

    print(f"Latest assessment: {summary['latest_assessment']}")

    change = summary["finding_change"]

    if change is None:
        print("Finding change: Not enough assessments to compare.")
    elif change > 0:
        print(f"Finding change: Increased by {change}")
    elif change < 0:
        print(f"Finding change: Decreased by {abs(change)}")
    else:
        print("Finding change: No change")


if __name__ == "__main__":
    main()
