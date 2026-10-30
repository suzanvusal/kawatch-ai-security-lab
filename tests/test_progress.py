"""Tests for the Kawatch project progress tracker."""

import json

import pytest

from kawatch.progress import load_progress


def test_load_progress_identifies_current_and_next_tasks(tmp_path):
    """The tracker should identify completed, current, and next tasks."""
    data = {
        "project": "Kawatch AI Security Lab",
        "completed_days": [1, 2, 3, 4, 5, 6, 7],
        "current_day": 8,
        "tasks": [
            {
                "day": 8,
                "title": "Build project progress tracker",
                "status": "in_progress",
            },
            {
                "day": 9,
                "title": "Add assessment history summary",
                "status": "planned",
            },
        ],
    }

    task_file = tmp_path / "project_tasks.json"
    task_file.write_text(json.dumps(data), encoding="utf-8")

    progress = load_progress(task_file)

    assert progress["completed_days"] == [1, 2, 3, 4, 5, 6, 7]
    assert progress["current_day"] == 8
    assert progress["current_task"]["title"] == (
        "Build project progress tracker"
    )
    assert progress["next_task"]["day"] == 9


def test_load_progress_rejects_missing_current_task(tmp_path):
    """The tracker should reject a current day with no matching task."""
    data = {
        "project": "Kawatch AI Security Lab",
        "completed_days": [1, 2, 3],
        "current_day": 4,
        "tasks": [],
    }

    task_file = tmp_path / "project_tasks.json"
    task_file.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="No task found"):
        load_progress(task_file)


def test_load_progress_rejects_missing_required_fields(tmp_path):
    """The tracker should reject incomplete project task files."""
    task_file = tmp_path / "project_tasks.json"
    task_file.write_text('{"project": "Kawatch"}', encoding="utf-8")

    with pytest.raises(ValueError, match="missing required fields"):
        load_progress(task_file)
