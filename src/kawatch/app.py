"""Core application health checks for Kawatch."""


def get_health_status() -> dict[str, str]:
    """Return the application's basic health status."""
    return {
        "status": "ok",
        "service": "kawatch-ai-security-lab",
        "stage": "foundation",
    }
