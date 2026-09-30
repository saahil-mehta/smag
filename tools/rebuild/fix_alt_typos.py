#!/usr/bin/env python3
"""Correct typos in image alt text carried over from the mirror.

Each fix is an exact alt value and its replacement. Re-running changes
nothing once the pages are fixed.
"""
from __future__ import annotations

from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
LANGS = {"hi", "mr", "gu", "kn", "te", "ml", "ta"}
FIXES = {'alt="Neodymium Discs Magnets"': 'alt="Neodymium Disc Magnets"'}


def main() -> int:
    n = 0
    for p in SITE.rglob("*.html"):
        if p.relative_to(SITE).parts[0] in LANGS:
            continue
        s = t = p.read_text(encoding="utf-8")
        for old, new in FIXES.items():
            t = t.replace(old, new)
        if t != s:
            p.write_text(t, encoding="utf-8")
            n += 1
    print(f"  {n} pages fixed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
