#!/usr/bin/env python3
"""Delete the Services pages, the Bespoke Magnet Design family and the
Eclipse guides SMAG is not keeping, then tidy the sitemap.

Decided 2 Sep 2026: SMAG has no separate services pages (site survey,
installation, servicing, training were Eclipse offerings); custom work is
already covered by the Custom Solutions pages inside the families that
remain; and the guides section is cut to twelve topics that map onto the
SMAG range, each rewritten by build_guides.py.

Also removed: the guides pagination stubs (page2..page6.html, which the
partial crawl fetched as flat files) and what-is-a-pot-magnet.html, an
unlinked crawl leftover.

Sitemap: the Services group and the Bespoke sub-tree are removed as whole
blocks here, because scrub_dead_links.py would otherwise leave their
headings behind with empty lists. Every other reference to a deleted page
(index cards, related-guide tiles, in-copy links) is left to
scrub_dead_links.py, which runs next in the order.

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

DROP_GUIDES = [
    "5-hidden-costs-of-traditional-steel-lifting",
    "how-can-i-keep-machine-coolant-cleaner-for-longer",
    "how-magnetic-filtration-can-help-eliminate-typical-edm-problems",
    "how-will-a-magnetic-filter-save-money",
    "improve-your-sustainability-with-magnetic-separation-and-metal-detection",
    "industrial-filtration-solutions-driving-efficiency-and-precision",
    "safe-fluids-handling-guide",
    "types-of-filtration-for-cnc-machines",
    "what-does-a-coolant-filter-do",
    "why-magnetic-filters-for-cnc-machines-are-saving-businesses-1-000s-a-year",
]
DROP_DIRS = ["services", "products/magnetic-materials-and-assemblies"] + [
    f"resources/guides/{g}" for g in DROP_GUIDES
]
DROP_FILES = [f"resources/guides/page{n}.html" for n in range(2, 7)] + [
    "resources/guides/what-is-a-pot-magnet.html"
]

# sitemap blocks: an <li> whose label is followed by a <ul> of children
SITEMAP_BLOCKS = [
    "<li>&raquo; <span>Services</span><ul>",
    "<li>&raquo; <a href=/products/magnetic-materials-and-assemblies/>"
    "Bespoke Magnet Design</a><ul>",
]


def drop_sitemap_blocks(text: str) -> tuple[str, int]:
    n = 0
    for opener in SITEMAP_BLOCKS:
        i = text.find(opener)
        if i < 0:
            continue
        ul = i + len(opener) - len("<ul>")
        end = find_element_end(text, ul)
        if end is None:
            print(f"  !! could not bound sitemap block {opener[:40]}")
            continue
        text = text[:i] + text[end:]
        n += 1
    return text, n


def main() -> None:
    dry = "--dry-run" in sys.argv
    smap = SITE / "sitemap/index.html"
    text = smap.read_text(encoding="utf-8")
    new, n = drop_sitemap_blocks(text)
    print(f"sitemap: {n} blocks removed")
    if not dry and new != text:
        smap.write_text(new, encoding="utf-8")

    pages = 0
    for d in DROP_DIRS:
        p = SITE / d
        if not p.exists():
            print(f"  missing {d}/")
            continue
        k = len(list(p.rglob("*.html")))
        pages += k
        print(f"  {'would delete' if dry else 'deleted'} {d}/  ({k} pages)")
        if not dry:
            shutil.rmtree(p)
    for f in DROP_FILES:
        p = SITE / f
        if p.exists():
            pages += 1
            print(f"  {'would delete' if dry else 'deleted'} {f}")
            if not dry:
                p.unlink()
    print(f"\n{pages} pages removed; {len(list(SITE.rglob('*.html')))} remain")


if __name__ == "__main__":
    main()
