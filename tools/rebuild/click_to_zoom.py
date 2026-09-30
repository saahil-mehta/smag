#!/usr/bin/env python3
"""Relabel the product gallery zoom tip and give the image a zoom cursor.

javascript.js now opens a gallery image's large rendition in the lity
lightbox on click, in place of the jQuery Zoom hover magnifier, which panned
the photo under the pointer. The tip under each image and the cursor follow.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
DRY = "--dry-run" in sys.argv
OLD, NEW = "</i> Hover to zoom</div>", "</i> Click to zoom</div>"
MARKER = "/* smag: click to zoom */"
RULES = f"\n{MARKER}\n.product-zoom{{cursor:zoom-in}}\n"


def main() -> int:
    pages = tips = 0
    for f in sorted(SITE.rglob("*.html")):
        s = f.read_text(encoding="utf-8")
        n = s.count(OLD)
        if n:
            pages += 1
            tips += n
            if not DRY:
                f.write_text(s.replace(OLD, NEW), encoding="utf-8")
    print(f"  {tips} tips relabelled on {pages} pages")
    css = CSS.read_text(encoding="utf-8")
    if MARKER not in css:
        print("  zoom cursor rule appended")
        if not DRY:
            CSS.write_text(css + RULES, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
