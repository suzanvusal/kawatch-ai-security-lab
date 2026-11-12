"""Load and validate structured AI agent task definitions."""

import json
from pathlib import Path
from typing import Any

ALLOWED_CHECKS = {"ruff", "pytest", "diff_check"}

REQUIRED_FIELDS = {
    "task_id",
    "title",
    "objective",
    "status",
    "allowed_files",
    "acceptance_criteria",
    "checks",
    "constraints",
    "requires_human_review",
}


def validate_task_definition(task: Any) -> list[str]:
    """Return validation errors for an AI agent task."""
    if not isinstance(task, dict):
        return ["Task definition must be a JSON object."]

    errors = []

    missing_fields = REQUIRED_FIELDS - task.keys()

    for field in sorted(missing_fields):
        errors.append(f"Missing required field: {field}")

    if missing_fields:
        return errors

    for field in ("task_id", "title", "objective"):
        if not isinstance(task[field], str) or not task[field].strip():
            errors.append(f"{field} must be a non-empty string.")

    if task["status"] not in ("planned", "in_progress", "completed"):
        errors.append("status must be planned, in_progress, or completed.")

    for field in ("allowed_files", "acceptance_criteria", "constraints"):
        value = task[field]

        if (
            not isinstance(value, list)
            or not value
            or any(
                not isinstance(item, str) or not item.strip()
                for item in value
            )
        ):
            errors.append(f"{field} must be a non-empty list of strings.")

    allowed_files = task["allowed_files"]

    if isinstance(allowed_files, list):
        for filename in allowed_files:
            if not isinstance(filename, str):
                continue

            file_path = Path(filename)

            if (
                file_path.is_absolute()
                or ".." in file_path.parts
                or "\\" in filename
            ):
                errors.append(
                    f"Invalid allowed file path: {filename}"
                )

    checks = task["checks"]

    if (
        not isinstance(checks, list)
        or not checks
        or any(check not in ALLOWED_CHECKS for check in checks)
    ):
        errors.append(
            "checks must contain only approved checks: "
            "ruff, pytest, diff_check."
        )

    if task["requires_human_review"] is not True:
        errors.append("Human review must be required.")

    return errors


def load_task_definition(path: Path) -> dict[str, Any]:
    """Load a JSON task definition and reject invalid instructions."""
    try:
        task = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Could not load task definition: {error}") from error

    errors = validate_task_definition(task)

    if errors:
        raise ValueError("; ".join(errors))

    return task


def main() -> None:
    """Display a validated task definition."""
    task_path = Path("agent_tasks/day-012-history-csv-export.json")
    task = load_task_definition(task_path)

    print("Kawatch AI Agent Task")
    print("-" * 40)
    print(f"Task ID: {task['task_id']}")
    print(f"Title: {task['title']}")
    print(f"Status: {task['status']}")
    print(f"Objective: {task['objective']}")

    print("\nAllowed files:")
    for filename in task["allowed_files"]:
        print(f"  - {filename}")

    print("\nAcceptance criteria:")
    for criterion in task["acceptance_criteria"]:
        print(f"  - {criterion}")

    print("\nHuman review required: Yes")


if __name__ == "__main__":
    main()
