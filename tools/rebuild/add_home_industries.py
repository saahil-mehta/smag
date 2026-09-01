#!/usr/bin/env python3
"""Put the Industry Focus section back on the home page.

home_products_heading.py removed Eclipse's Industry Focus row when the
Product Families grid went in, which left the home page with no industries
entry point beyond the nav. This restores the mirror's own compact layout
(grid--home-industries: small thumbnail, name, chevron, three columns),
filtered to the eight sectors SMAG serves and with the intro copy rewritten.

A first version of this script used the /industries/ page's large card
tiles instead; the mirror's compact list is the design the layout expects
on the home page, so the mirror markup is now the source.

Idempotent: replaces its own row when re-run.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
HOME = SITE / "index.html"
MIRROR_HOME = REPO / "reference-mirror/www.eclipsemagnetics.com/index.html"

ROW_ID = "industries-we-serve"
KEEP = [
    "virgin-recycled-plastic-processing", "oil-and-gas", "steel",
    "food-processing", "chemical-processing", "sugar-processing",
    "aerospace", "pharmaceutical",
]
INTRO = ("Our separators, filters, lifters and chucks run in plants across "
         "these sectors, each unit sized and certified for its duty.")


def main() -> None:
    dry = "--dry-run" in sys.argv
    src = MIRROR_HOME.read_text(encoding="utf-8")
    m = re.search(r'<div class="grid grid--home-industries">', src)
    end = find_element_end(src, m.start())
    items = {}
    for it in re.finditer(r"<div class=grid__item>", src[m.start():end]):
        seg = src[m.start():end]
        iend = find_element_end(seg, it.start())
        tile = seg[it.start():iend]
        slug = re.search(r"href=/industries/([a-z-]+)/", tile).group(1)
        items[slug] = tile
    kept = [items[s] for s in KEEP if s in items]
    if len(kept) != len(KEEP):
        raise SystemExit(f"missing tiles: {[s for s in KEEP if s not in items]}")

    row = (f'<div class="row row--alt" id={ROW_ID}>'
           '<div class="row__inner row__intro">'
           "<h3 class=bordered-header>Industry Focus</h3>"
           f'<p class="intro capped">{INTRO}'
           "<div class=c2a><a href=/industries/>View All Sectors</a></div>"
           "</div><div class=row__inner>"
           '<div class="grid grid--home-industries">'
           + "".join(kept) + "</div></div></div>")

    text = HOME.read_text(encoding="utf-8")
    old = re.search(rf'<div class="row row--alt" id={ROW_ID}>', text)
    if old:
        oend = find_element_end(text, old.start())
        text = text[:old.start()] + row + text[oend:]
        print(f"replaced existing row ({len(kept)} items, compact layout)")
    else:
        k = text.find('class="row__inner home-categories"')
        gend = find_element_end(text, text.rfind("<div", 0, k))
        rend = text.find("</div>", gend) + len("</div>")
        text = text[:rend] + row + text[rend:]
        print(f"inserted after Product Families ({len(kept)} items)")
    if not dry:
        HOME.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
