#!/usr/bin/env python3
"""Static preview server that declares UTF-8, matching production.

python3 -m http.server sends a bare "Content-type: text/html". Browsers then
fall back to guessing the encoding, and since many mirror pages declare
<meta charset> beyond the 1024-byte prescan limit, that guess lands on
windows-1252: "©" renders as "Â©", "é" as "Ã©", and CJK text as mojibake.

An HTTP Content-Type charset takes precedence over the in-document <meta>,
so declaring it here fixes every page without touching any HTML. GitHub Pages
already sends "text/html; charset=utf-8", so this makes the local preview
match what is actually deployed.

Usage: serve.py <directory> <port> [host]
"""
from __future__ import annotations

import functools
import http.server
import socketserver
import sys
from pathlib import Path

# Text formats where a missing charset leads to a browser guess.
CHARSET_TYPES = {
    "text/html",
    "text/css",
    "text/plain",
    "text/javascript",
    "application/javascript",
    "application/json",
    "image/svg+xml",
    "application/xml",
    "text/xml",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        ctype = super().guess_type(path)
        base = ctype.split(";", 1)[0].strip()
        if base in CHARSET_TYPES and "charset=" not in ctype:
            return f"{base}; charset=utf-8"
        return ctype

    def log_message(self, fmt, *args):
        # Keep the preview quiet; errors still surface via log_error.
        pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__.strip().splitlines()[-1])

    directory = Path(sys.argv[1]).resolve()
    port = int(sys.argv[2])
    host = sys.argv[3] if len(sys.argv) > 3 else "127.0.0.1"

    if not directory.is_dir():
        sys.exit(f"not a directory: {directory}")

    handler = functools.partial(Handler, directory=str(directory))
    with Server((host, port), handler) as httpd:
        print(f"Serving {directory} on http://{host}:{port} as UTF-8  (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")


if __name__ == "__main__":
    main()
