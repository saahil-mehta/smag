#!/usr/bin/env python3
"""Fill each industry page's "Products used in ..." grid from its own copy.

prune_catalogue.py emptied the cards that pointed at dropped Eclipse
products, which left oil and gas with three blank cards, sugar with one, and
the rest showing one or two products that did not match the page's own
"Where the equipment goes" list. Each grid is now rebuilt from that list.

Cards are copied from the family index pages, so image, blurb and markup
match the catalogue exactly. The drawer housings named in the food, chemical,
pharmaceutical and plastics lists have no product page yet and are left out.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
DRY = "--dry-run" in sys.argv

SEP = "magnetic-separation-and-metal-detection"
WH = "workholding-systems"
TOOLS = "magnetic-tools-and-standard-magnets"

INDUSTRIES = {
    "aerospace": [f"{WH}/rectangular-premier-chuck", f"{WH}/circular-premier-chuck",
                  "filtration-systems/magnetic-coolant-filter", f"{WH}/table-top-demagnetiser",
                  "lifting-and-handling/permanent-magnetic-lifter", f"{TOOLS}/neodymium-block-magnets"],
    "chemical-processing": [f"{SEP}/magnetic-separation-grids", f"{SEP}/housed-easy-clean-grid-magnet-separator",
                            f"{SEP}/high-intensity-liquid-filter-separator"],
    "food-processing": [f"{SEP}/magnetic-separation-grids", f"{SEP}/magnetic-grids-for-sieves",
                        f"{SEP}/housed-easy-clean-grid-magnet-separator", f"{SEP}/housed-bullet-magnet",
                        f"{SEP}/high-intensity-liquid-filter-separator", f"{SEP}/magnetic-sampling-probe"],
    "oil-and-gas": ["oil-and-gas-pipeline-filtration/inline-magnetic-pipeline-filter",
                    "oil-and-gas-pipeline-filtration/modular-high-pressure-pipeline-filter"],
    "pharmaceutical": [f"{SEP}/magnetic-separation-grids", f"{SEP}/housed-easy-clean-grid-magnet-separator",
                       f"{SEP}/high-intensity-liquid-filter-separator"],
    "steel": ["lifting-and-handling/permanent-magnetic-lifter", f"{WH}/rectangular-premier-chuck",
              f"{WH}/circular-premier-chuck", "filtration-systems/magnetic-coolant-filter",
              f"{TOOLS}/magnetic-sweeper", f"{SEP}/deep-field-magnetic-plate-separator"],
    "sugar-processing": [f"{SEP}/deep-field-magnetic-plate-separator", f"{SEP}/chute-separator",
                         f"{SEP}/housed-easy-clean-grid-magnet-separator", f"{SEP}/magnetic-separation-grids",
                         f"{SEP}/high-intensity-liquid-filter-separator", f"{SEP}/magnetic-sampling-probe"],
    "virgin-recycled-plastic-processing": [f"{SEP}/deep-field-magnetic-plate-separator", f"{SEP}/chute-separator",
                                           f"{SEP}/magnetic-separation-grids", f"{SEP}/housed-bullet-magnet",
                                           f"{SEP}/housed-easy-clean-grid-magnet-separator",
                                           f"{SEP}/magnetic-sampling-probe"],
}

GRID_OPEN = '<div class="grid grid--product-category">'


def grid_span(s: str, start: int) -> tuple[int, int]:
    """Return the span of the div opening at start, found by depth walk."""
    depth = 0
    for m in re.compile(r"<div\b|</div>").finditer(s, start):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return start, m.end()
    raise SystemExit("unbalanced grid")


def catalogue_cards() -> dict[str, str]:
    cards = {}
    for f in (SITE / "products").glob("*/index.html"):
        s = f.read_text(encoding="utf-8")
        g = s.find(GRID_OPEN)
        if g < 0:
            continue
        a, b = grid_span(s, g)
        inner = s[a + len(GRID_OPEN):b - len("</div>")]
        pos = 0
        while (i := inner.find("<div class=grid__item>", pos)) >= 0:
            _, j = grid_span(inner, i)
            item = inner[i:j]
            m = re.search(r"<a href=/products/([^ >]+?)/ ", item)
            if m:
                cards[m.group(1)] = item
            pos = j
    return cards


def main() -> int:
    cards = catalogue_cards()
    for slug, products in INDUSTRIES.items():
        f = SITE / "industries" / slug / "index.html"
        s = f.read_text(encoding="utf-8")
        g = s.find(GRID_OPEN)
        if g < 0:
            raise SystemExit(f"no product grid on {slug}")
        missing = [p for p in products if p not in cards]
        if missing:
            raise SystemExit(f"{slug}: no catalogue card for {missing}")
        a, b = grid_span(s, g)
        new = GRID_OPEN + "".join(cards[p] for p in products) + "</div>"
        print(f"  {slug:36s} {len(products)} cards" + ("" if s[a:b] != new else " (unchanged)"))
        if not DRY and s[a:b] != new:
            f.write_text(s[:a] + new + s[b:], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
