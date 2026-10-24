"""Tests for the security-header analyzer."""

from kawatch.security_headers import analyze_security_headers


def test_reports_missing_security_headers() -> None:
    findings = analyze_security_headers({}, is_https=True)

    reported_headers = {finding.header for finding in findings}

    assert "content-security-policy" in reported_headers
    assert "x-content-type-options" in reported_headers
    assert "referrer-policy" in reported_headers
    assert "x-frame-options" in reported_headers
    assert "strict-transport-security" in reported_headers


def test_accepts_headers_case_insensitively() -> None:
    headers = {
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Strict-Transport-Security": "max-age=31536000",
    }

    findings = analyze_security_headers(headers, is_https=True)

    assert findings == []


def test_does_not_report_hsts_missing_for_http() -> None:
    findings = analyze_security_headers({}, is_https=False)

    reported_headers = {finding.header for finding in findings}

    assert "strict-transport-security" not in reported_headers


def test_csp_frame_ancestors_counts_as_frame_protection() -> None:
    headers = {
        "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
    }

    findings = analyze_security_headers(headers, is_https=False)

    assert all(finding.header != "x-frame-options" for finding in findings)