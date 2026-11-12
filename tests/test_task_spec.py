"""Tests for AI agent task definitions."""

import json

import pytest

from kawatch.task_spec import (
    load_task_definition,
    validate_task_definition,
)


def valid_task():
    """Return a valid sample agent task."""
    return {
        "task_id": "day-012-history-csv-export",
        "title": "Add CSV export",
        "objective": "Export assessment history as CSV.",
        "status": "planned",
        "allowed_files": [
            "src/kawatch/history.py",
            "tests/test_history.py",
        ],
        "acceptance_criteria": [
            "Generate a CSV file.",
            "Add automated tests.",
        ],
        "checks": ["ruff", "pytest", "diff_check"],
        "constraints": [
            "Do not modify main directly.",
            "Require human approval.",
        ],
        "requires_human_review": True,
    }


def test_valid_task_definition_passes():
    """A complete task definition should pass validation."""
    assert validate_task_definition(valid_task()) == []


def test_task_definition_rejects_missing_fields():
    """Required task fields cannot be omitted."""
    errors = validate_task_definition({"task_id": "day-012"})

    assert "Missing required field: title" in errors
    assert "Missing required field: allowed_files" in errors


def test_task_definition_rejects_unapproved_checks():
    """Only approved check names should be accepted."""
    task = valid_task()
    task["checks"] = ["ruff", "delete-project"]

    errors = validate_task_definition(task)

    assert any("approved checks" in error for error in errors)


def test_task_definition_rejects_paths_outside_project():
    """Task file permissions must not include parent directories."""
    task = valid_task()
    task["allowed_files"] = ["../../outside-project/file.py"]

    errors = validate_task_definition(task)

    assert any("Invalid allowed file path" in error for error in errors)


def test_task_definition_requires_human_review():
    """A task cannot disable the human review requirement."""
    task = valid_task()
    task["requires_human_review"] = False

    errors = validate_task_definition(task)

    assert "Human review must be required." in errors


def test_load_task_definition_from_json(tmp_path):
    """The loader should read a valid task from a JSON file."""
    task = valid_task()
    task_file = tmp_path / "task.json"
    task_file.write_text(json.dumps(task), encoding="utf-8")

    loaded_task = load_task_definition(task_file)

    assert loaded_task["task_id"] == "day-012-history-csv-export"
    assert loaded_task["requires_human_review"] is True


def test_load_task_definition_rejects_invalid_json(tmp_path):
    """The loader should reject malformed JSON."""
    task_file = tmp_path / "task.json"
    task_file.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Could not load task definition"):
        load_task_definition(task_file)
