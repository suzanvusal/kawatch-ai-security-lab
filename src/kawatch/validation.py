"""Validate the structure and contents of Kawatch assessment reports."""

from datetime import datetime
from typing import Any

REQUIRED_REPORT_FIELDS = {
    "project",
    "generated_at",
    "target",
    "http_status",
    "summary",
    "findings",
}

REQUIRED_SUMMARY_FIELDS = {
    "total_findings",
    "high",
    "medium",
    "low",
}


def validate_report(report: Any) -> list[str]:
    """Return validation errors for an assessment report."""
    errors = []

    if not isinstance(report, dict):
        return ["Report must be a JSON object."]

    missing_fields = REQUIRED_REPORT_FIELDS - report.keys()

    if missing_fields:
        return [
            f"Missing required field: {field}"
            for field in sorted(missing_fields)
        ]

    if not isinstance(report["project"], str) or not report["project"]:
        errors.append("Project must be a non-empty string.")

    if not isinstance(report["target"], str) or not report["target"]:
        errors.append("Target must be a non-empty string.")

    try:
        datetime.fromisoformat(report["generated_at"])
    except (TypeError, ValueError):
        errors.append("generated_at must be a valid ISO 8601 timestamp.")

    if (
        not isinstance(report["http_status"], int)
        or isinstance(report["http_status"], bool)
        or not 100 <= report["http_status"] <= 599
    ):
        errors.append("http_status must be an integer between 100 and 599.")

    summary = report["summary"]

    if not isinstance(summary, dict):
        errors.append("summary must be a JSON object.")
    else:
        missing_summary_fields = REQUIRED_SUMMARY_FIELDS - summary.keys()

        for field in sorted(missing_summary_fields):
            errors.append(f"Missing summary field: {field}")

        if not missing_summary_fields:
            counts = [
                summary[field]
                for field in REQUIRED_SUMMARY_FIELDS
            ]

            if any(
                not isinstance(count, int)
                or isinstance(count, bool)
                or count < 0
                for count in counts
            ):
                errors.append("Summary counts must be non-negative integers.")
            elif (
                summary["high"]
                + summary["medium"]
                + summary["low"]
                != summary["total_findings"]
            ):
                errors.append(
                    "Severity counts must equal total_findings."
                )

    if not isinstance(report["findings"], list):
        errors.append("findings must be a JSON array.")
    else:
        if (
            isinstance(summary, dict)
            and isinstance(summary.get("total_findings"), int)
            and not isinstance(summary.get("total_findings"), bool)
            and summary["total_findings"] != len(report["findings"])
        ):
            errors.append(
                "The number of findings must equal total_findings."
            )

        for index, finding in enumerate(report["findings"]):
            if not isinstance(finding, dict):
                errors.append(f"Finding {index} must be a JSON object.")
                continue

            for field in (
                "header",
                "severity",
                "message",
                "recommendation",
            ):
                if (
                    not isinstance(finding.get(field), str)
                    or not finding[field]
                ):
                    errors.append(
                        f"Finding {index} has an invalid {field}."
                    )

            if finding.get("severity") not in ("High", "Medium", "Low"):
                errors.append(
                    f"Finding {index} has an unsupported severity."
                )

    return errors
