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
    """Save assessment results as a structured JSON report."""

    report = {
        "project": "Kawatch AI Security Lab",
        "generated_at": datetime.now(timezone.utc).isoformat(),
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    return output_path
