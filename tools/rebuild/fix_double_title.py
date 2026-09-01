#!/usr/bin/env python3
"""Collapse doubled "| Santosh Magnetic Works" title suffixes.

An earlier brand sweep appended the works' name to titles that already
carried it, so some pages show "... | Santosh Magnetic Works | Santosh
Magnetic Works" in the tab. One suffix stays.
"""
from __future__ import annotations

from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
DOUBLE = "| Santosh Magnetic Works | Santosh Magnetic Works"
SINGLE = "| Santosh Magnetic Works"


def main() -> None:
    n = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        if DOUBLE not in text:
            continue
        page.write_text(text.replace(DOUBLE, SINGLE), encoding="utf-8")
        n += 1
        print(f"fixed {page.relative_to(SITE)}")
    print(f"pages fixed: {n}")


if __name__ == "__main__":
    main()
