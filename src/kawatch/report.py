"""Generate JSON security assessment reports."""

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from kawatch.security_headers import SecurityHeaderFinding


def save_assessment_report(
    url: str,
    status_code: int,
    findings: list[SecurityHeaderFinding],
    output_path: Path,
) -> Path:
    """Save the latest report and preserve a historical copy."""

    generated_at = datetime.now(timezone.utc)

    report = {
        "project": "Kawatch AI Security Lab",
        "generated_at": generated_at.isoformat(),
        "target": url,
        "http_status": status_code,
        "summary": {
            "total_findings": len(findings),
            "high": sum(f.severity == "High" for f in findings),
            "medium": sum(f.severity == "Medium" for f in findings),
            "low": sum(f.severity == "Low" for f in findings),
        },
        "findings": [asdict(finding) for finding in findings],
    }

    report_json = json.dumps(report, indent=4)

    # Create a unique filename for this assessment.
    timestamp = generated_at.strftime("%Y%m%d-%H%M%S-%f")
    history_dir = output_path.parent / "history"
    history_dir.mkdir(parents=True, exist_ok=True)

    history_path = history_dir / f"assessment-{timestamp}.json"

    # Save the historical report.
    history_path.write_text(report_json, encoding="utf-8")

    # Also update the latest report.
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_json, encoding="utf-8")

    return output_path
