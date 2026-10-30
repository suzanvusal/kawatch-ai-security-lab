"""Read and display Kawatch project development progress."""

import json
from pathlib import Path
from typing import Any


def load_progress(path: Path) -> dict[str, Any]:
    """Load project progress and identify the current and next tasks."""
    data = json.loads(path.read_text(encoding="utf-8"))

    required = {"project", "completed_days", "current_day", "tasks"}
    if not required.issubset(data):
        raise ValueError("Project task file is missing required fields.")

    if not isinstance(data["completed_days"], list):
        raise ValueError("completed_days must be a list.")

    if not isinstance(data["tasks"], list):
        raise ValueError("tasks must be a list.")

    current_day = data["current_day"]

    current_task = next(
        (task for task in data["tasks"] if task["day"] == current_day),
        None,
    )

    if current_task is None:
        raise ValueError("No task found for the current development day.")

    next_task = next(
        (
            task
            for task in sorted(data["tasks"], key=lambda item: item["day"])
            if task["day"] > current_day and task["status"] == "planned"
        ),
        None,
    )

    return {
        "project": data["project"],
        "completed_days": sorted(data["completed_days"]),
        "current_day": current_day,
        "current_task": current_task,
        "next_task": next_task,
    }


def main() -> None:
    """Print the current Kawatch development progress."""
    progress = load_progress(Path("project_tasks.json"))

    print(progress["project"])
    print("-" * 40)
    print(f"Completed days: {progress['completed_days']}")
    print(f"Current day: {progress['current_day']}")
    print(f"Current task: {progress['current_task']['title']}")

    next_task = progress["next_task"]

    if next_task:
        print(f"Next task: Day {next_task['day']} - {next_task['title']}")
    else:
        print("Next task: No planned task found.")


if __name__ == "__main__":
    main()
