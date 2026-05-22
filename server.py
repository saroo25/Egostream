#!/usr/bin/env python3
"""
Minimal static server for the EGOSTREAM teaser website.

Run locally:
    python server.py

Optional:
    PORT=8080 python server.py
    HOST=0.0.0.0 PORT=8080 python server.py
"""

from __future__ import annotations

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))


class TeaserHandler(SimpleHTTPRequestHandler):
    """Static-file handler with clean index fallback and no directory listings."""

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def list_directory(self, path):  # type: ignore[override]
        self.send_error(403, "Directory listing disabled")
        return None

    def do_GET(self) -> None:
        # Let / route serve index.html.
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()


def main() -> int:
    handler = partial(TeaserHandler, directory=str(ROOT))
    server = ThreadingHTTPServer((HOST, PORT), handler)
    url_host = "localhost" if HOST in {"127.0.0.1", "0.0.0.0"} else HOST
    print(f"Serving EGOSTREAM teaser from: {ROOT}")
    print(f"Open: http://{url_host}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
