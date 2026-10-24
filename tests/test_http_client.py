"""Tests for the local HTTP response collector."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

import pytest

from kawatch.http_client import fetch_local_headers


class DemoHandler(BaseHTTPRequestHandler):
    """Return predictable headers for collector tests."""

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(b"Kawatch test response")

    def log_message(self, format: str, *args: object) -> None:
        """Suppress routine test-server logs."""


@pytest.fixture
def local_server():
    """Start a temporary HTTP server on an available local port."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_collects_headers_from_local_server(local_server) -> None:
    port = local_server.server_address[1]

    result = fetch_local_headers(f"http://127.0.0.1:{port}/")

    assert result.status_code == 200
    assert result.is_https is False
    assert result.headers["X-Content-Type-Options"] == "nosniff"


def test_rejects_external_host() -> None:
    with pytest.raises(ValueError, match="127.0.0.1"):
        fetch_local_headers("http://example.com/")


def test_rejects_https_for_this_development_collector() -> None:
    with pytest.raises(ValueError, match="HTTP"):
        fetch_local_headers("https://127.0.0.1:8765/")


def test_rejects_missing_port() -> None:
    with pytest.raises(ValueError, match="port"):
        fetch_local_headers("http://127.0.0.1/")


def test_rejects_non_positive_timeout() -> None:
    with pytest.raises(ValueError, match="Timeout"):
        fetch_local_headers("http://127.0.0.1:8765/", timeout=0)