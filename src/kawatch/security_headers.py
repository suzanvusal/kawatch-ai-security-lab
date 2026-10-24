"""Analyze HTTP security headers without making network requests."""

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityHeaderFinding:
    """Describe a potential security-header weakness."""

    header: str
    severity: str
    message: str
    recommendation: str


def analyze_security_headers(
    headers: Mapping[str, str],
    *,
    is_https: bool,
) -> list[SecurityHeaderFinding]:
    """Report selected security headers that are missing.

    This function analyzes supplied headers only. It does not make
    network requests or verify the effectiveness of existing policies.
    """
    normalized = {
        name.strip().lower(): value.strip()
        for name, value in headers.items()
    }

    findings: list[SecurityHeaderFinding] = []

    checks = [
        (
            "content-security-policy",
            "Medium",
            "Content Security Policy is missing.",
            "Define a Content Security Policy suited to the application.",
        ),
        (
            "x-content-type-options",
            "Low",
            "X-Content-Type-Options is missing.",
            "Consider setting X-Content-Type-Options to nosniff.",
        ),
        (
            "referrer-policy",
            "Low",
            "Referrer-Policy is missing.",
            "Set a Referrer-Policy appropriate for the application.",
        ),
    ]

    for header, severity, message, recommendation in checks:
        if not normalized.get(header):
            findings.append(
                SecurityHeaderFinding(
                    header=header,
                    severity=severity,
                    message=message,
                    recommendation=recommendation,
                )
            )

    # Clickjacking protection can be provided by either of these policies.
    csp = normalized.get("content-security-policy", "").lower()
    has_frame_ancestors = "frame-ancestors" in csp
    has_frame_options = bool(normalized.get("x-frame-options"))

    if not has_frame_ancestors and not has_frame_options:
        findings.append(
            SecurityHeaderFinding(
                header="x-frame-options",
                severity="Medium",
                message="No recognized frame-protection header was found.",
                recommendation=(
                    "Configure CSP frame-ancestors or X-Frame-Options "
                    "to suit the application's framing requirements."
                ),
            )
        )

    # HSTS is relevant to HTTPS, so do not flag HTTP responses for it.
    if is_https and not normalized.get("strict-transport-security"):
        findings.append(
            SecurityHeaderFinding(
                header="strict-transport-security",
                severity="Medium",
                message="Strict-Transport-Security is missing on HTTPS.",
                recommendation=(
                    "Evaluate an appropriate HSTS policy after confirming "
                    "HTTPS is correctly configured for the domain."
                ),
            )
        )

    return findings