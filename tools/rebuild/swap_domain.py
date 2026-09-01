#!/usr/bin/env python3
"""Point every absolute eclipsemagnetics.com URL at santoshmagneticworks.com.

Covers canonical links, JSON-LD breadcrumb schemas, og:url/og:image tags and
in-copy absolute links. Links that end up pointing at pages this site does
not carry are removed afterwards by scrub_dead_links.py; og:image tags whose
file does not exist locally are handled by debrand_copy.py.
"""
from __future__ import annotations

from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

SWAPS = [
    ("https://www.eclipsemagnetics.com", "https://santoshmagneticworks.com"),
    ("http://www.eclipsemagnetics.com", "https://santoshmagneticworks.com"),
    ("www.eclipsemagnetics.com", "santoshmagneticworks.com"),
    ("eclipsemagnetics.com", "santoshmagneticworks.com"),  # bare-domain links
]


def main() -> None:
    pages = swaps = 0
    for page in sorted(SITE.rglob("*.html")):
        text = orig = page.read_text(encoding="utf-8")
        for old, new in SWAPS:
            swaps += text.count(old)
            text = text.replace(old, new)
        if text != orig:
            pages += 1
            page.write_text(text, encoding="utf-8")
    print(f"{swaps} URLs swapped across {pages} pages")


if __name__ == "__main__":
    main()
