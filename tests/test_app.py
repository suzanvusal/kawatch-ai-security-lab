"""Tests for the Kawatch application foundation."""

from kawatch.app import get_health_status


def test_health_status_contains_expected_fields() -> None:
    result = get_health_status()

    assert result["status"] == "ok"
    assert result["service"] == "kawatch-ai-security-lab"
    assert result["stage"] == "foundation"
