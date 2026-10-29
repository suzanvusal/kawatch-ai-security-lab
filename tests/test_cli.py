"""Tests for the Kawatch command-line assessment."""

from kawatch import cli
from kawatch.http_client import HttpResponseData


def test_assess_url_returns_status_and_findings(monkeypatch):
    """Collected response headers should be passed to the analyzer."""

    def fake_fetch(url: str) -> HttpResponseData:
        assert url == "http://127.0.0.1:8765"

        return HttpResponseData(
            status_code=200,
            headers={
                "Content-Type": "text/html",
                "X-Content-Type-Options": "nosniff",
            },
            is_https=False,
        )

    monkeypatch.setattr(cli, "fetch_local_headers", fake_fetch)

    status_code, findings = cli.assess_url(
        "http://127.0.0.1:8765"
    )

    assert status_code == 200

    finding_headers = {finding.header for finding in findings}

    assert "content-security-policy" in finding_headers
    assert "referrer-policy" in finding_headers
