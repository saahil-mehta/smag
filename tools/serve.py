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
import re
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


RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)$")


class Handler(http.server.SimpleHTTPRequestHandler):
    """Adds two more things GitHub Pages does and http.server does not.

    Byte ranges: Safari fetches <video> in ranges and needs a 206 reply to seek,
    so without them the hero video plays once and cannot loop back to 0.

    Revalidation: with no Cache-Control the browser caches pages heuristically
    from Last-Modified and shows stale copies after an edit. "no-cache" makes
    it ask every time; unchanged files still come back as a cheap 304.
    """

    _remaining: int | None = None

    def guess_type(self, path):
        ctype = super().guess_type(path)
        base = ctype.split(";", 1)[0].strip()
        if base in CHARSET_TYPES and "charset=" not in ctype:
            return f"{base}; charset=utf-8"
        return ctype

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def send_head(self):
        self._remaining = None
        m = RANGE_RE.match(self.headers.get("Range", "").strip())
        path = Path(self.translate_path(self.path))
        if not m or not path.is_file() or m.groups() == ("", ""):
            return super().send_head()

        size = path.stat().st_size
        first, last = m.groups()
        if first:
            start, end = int(first), min(int(last) if last else size - 1, size - 1)
        else:  # suffix range: the final N bytes
            start, end = max(size - int(last), 0), size - 1
        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        f = path.open("rb")
        f.seek(start)
        self._remaining = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(self._remaining))
        self.send_header("Last-Modified", self.date_time_string(int(path.stat().st_mtime)))
        self.end_headers()
        return f

    def copyfile(self, source, outputfile):
        if self._remaining is None:
            return super().copyfile(source, outputfile)
        left = self._remaining
        while left > 0:
            chunk = source.read(min(64 * 1024, left))
            if not chunk:
                break
            outputfile.write(chunk)
            left -= len(chunk)

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
