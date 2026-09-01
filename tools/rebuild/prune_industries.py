#!/usr/bin/env python3
"""Trim the industries section to the eight sectors SMAG actually serves.

Keeps: virgin/recycled plastic, oil and gas, steel, food, chemical, sugar,
aerospace, pharmaceutical.

Deletes: automotive-manufacturing, bearing-manufacture, engineering,
speaker-magnets, then removes every tile, card or list row that pointed at
them (industries index grid, sector-expertise cards, guide links, sitemap
rows).

Container removal is depth-aware via remove_sections.find_element_end; slug
alternations are terminated with `/` so `/engineering` cannot match a longer
path (see the lessons in README.md).

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

DROP = [
    "automotive-manufacturing",
    "bearing-manufacture",
    "engineering",
    "speaker-magnets",
]

SLUG_RE = re.compile(
    r"/industries/(?:" + "|".join(re.escape(s) for s in DROP) + r")/"
)

# Containers that may wrap a link to a dropped industry, innermost first.
CONTAINER_RES = [
    re.compile(r'<div class="?grid__item\b[^>]*>'),
    re.compile(r'<div class="?swiper-slide\b[^>]*>'),
    re.compile(r"<li\b[^>]*>"),
]


def scrub(text: str) -> tuple[str, int]:
    removed = 0
    while True:
        m = SLUG_RE.search(text)
        if m is None:
            return text, removed
        # innermost matching container that encloses the hit
        best = None
        for cre in CONTAINER_RES:
            for c in cre.finditer(text, 0, m.start()):
                end = find_element_end(text, c.start())
                if end and c.start() < m.start() < end:
                    span = end - c.start()
                    if best is None or span < best[2]:
                        best = (c.start(), end, span)
        if best:
            text = text[: best[0]] + text[best[1]:]
        else:
            # last resort: neutralise the link target so nothing 404s
            a = text.rfind("<a ", 0, m.start())
            e = text.find("</a>", m.start())
            if a >= 0 and e >= 0:
                text = text[:a] + text[e + 4:]
            else:
                text = text[: m.start()] + "/industries/" + text[m.end():]
        removed += 1


def main() -> None:
    dry = "--dry-run" in sys.argv

    for slug in DROP:
        d = SITE / "industries" / slug
        if d.exists():
            print(f"delete dir  industries/{slug}/")
            if not dry:
                shutil.rmtree(d)

    total = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        if not SLUG_RE.search(text):
            continue
        new, n = scrub(text)
        total += n
        print(f"{n:3d} removals  {page.relative_to(SITE)}")
        if not dry:
            page.write_text(new, encoding="utf-8")

    left = [
        p.relative_to(SITE)
        for p in SITE.rglob("*.html")
        if SLUG_RE.search(p.read_text(encoding="utf-8"))
    ]
    print(f"\ncontainers removed: {total}; pages still referencing: {left or 'none'}")


if __name__ == "__main__":
    main()
