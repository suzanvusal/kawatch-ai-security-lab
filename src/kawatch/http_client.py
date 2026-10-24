"""Collect HTTP response headers from a local demonstration server."""

import http.client
from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True)
class HttpResponseData:
    """Represent the parts of an HTTP response needed by Kawatch."""

    status_code: int
    headers: dict[str, str]
    is_https: bool


def fetch_local_headers(
    url: str,
    *,
    timeout: float = 2.0,
) -> HttpResponseData:
    """Fetch response headers from an HTTP server on 127.0.0.1 only."""
    parsed = urlsplit(url)

    if parsed.scheme != "http":
        raise ValueError("Only local HTTP URLs are allowed.")

    if parsed.hostname != "127.0.0.1":
        raise ValueError("Only the local address 127.0.0.1 is allowed.")

    if parsed.username is not None or parsed.password is not None:
        raise ValueError("URLs containing credentials are not allowed.")

    if parsed.port is None:
        raise ValueError("Specify the local server port in the URL.")

    if parsed.fragment:
        raise ValueError("URL fragments are not supported.")

    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    path = parsed.path or "/"

    if parsed.query:
        path = f"{path}?{parsed.query}"

    connection = http.client.HTTPConnection(
        "127.0.0.1",
        parsed.port,
        timeout=timeout,
    )

    try:
        connection.request("GET", path)
        response = connection.getresponse()

        return HttpResponseData(
            status_code=response.status,
            headers=dict(response.getheaders()),
            is_https=False,
        )
    finally:
        connection.close()