#!/usr/bin/env python3
"""Restore a readable body weight after the variable-font swap.

The theme sets body{font-weight:200}. The Effra kit only ever shipped 400,
500 and 700, so CSS font matching snapped that 200 up to 400 and the site
rendered at regular weight. Noto Sans is a single variable file carrying the
whole 100 to 900 axis, so 200 is now honoured literally and the body copy
came out thin.

Set it to 400, which is what the page actually rendered at before.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

CSS = Path("/Users/saahil/Documents/GitHub/smag/site/site/assets/pwpc/"
           "pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css")
DRY = "--dry-run" in sys.argv
NEW_WEIGHT = sys.argv[sys.argv.index("--weight") + 1] if "--weight" in sys.argv else "400"


def main() -> int:
    s = CSS.read_text(encoding="utf-8")
    m = re.search(r"(?<![\w-])body\{([^}]*)\}", s)
    if not m:
        raise SystemExit("no body{} rule found")
    body = m.group(1)
    wm = re.search(r"font-weight:(\d+)", body)
    if not wm:
        raise SystemExit("body rule carries no font-weight")
    old = wm.group(1)
    new_body = body[:wm.start(1)] + NEW_WEIGHT + body[wm.end(1):]
    print(f"body font-weight {old} -> {NEW_WEIGHT}")
    if not DRY:
        CSS.write_text(s[:m.start(1)] + new_body + s[m.end(1):], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
