"""A local demonstration server for Kawatch development."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class DemoRequestHandler(BaseHTTPRequestHandler):
    """Serve a simple page with intentionally incomplete security headers."""

    def do_GET(self) -> None:
        body = (
            "<!doctype html>"
            "<html><head><title>Kawatch Demo</title></head>"
            "<body><h1>Kawatch Local Security Demo</h1></body></html>"
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        """Keep routine demo requests quiet in the terminal."""


def main() -> None:
    """Start the demonstration server on the loopback interface."""
    server = ThreadingHTTPServer(("127.0.0.1", 8765), DemoRequestHandler)

    print("Kawatch demo server: http://127.0.0.1:8765")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Kawatch demo server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()