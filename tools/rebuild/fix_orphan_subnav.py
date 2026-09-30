#!/usr/bin/env python3
"""Remove subnav items whose link was taken out but whose label was left.

drop_family_subpages.py removed the links to the dropped Eclipse sub-pages
("Service & Maintenance", "Sector Expertise") but left on the lifting family
page an <li> holding only the label and a stray </a>. Such an item is dead
text in the page's tab row. Re-running changes nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
LANGS = {"hi", "mr", "gu", "kn", "te", "ml", "ta"}
SUBNAV = re.compile(r'<div class="row subnav">.*?</ul>', re.S)
ORPHAN = re.compile(r"<li>\s*[^<]*</a>")


def main() -> int:
    n = 0
    for p in SITE.rglob("index.html"):
        if p.relative_to(SITE).parts[0] in LANGS:
            continue
        s = p.read_text(encoding="utf-8")
        t = SUBNAV.sub(lambda m: ORPHAN.sub("", m.group(0)), s)
        if t != s:
            p.write_text(t, encoding="utf-8")
            n += 1
            print(f"  {p.relative_to(SITE)}")
    print(f"  {n} pages fixed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
