#!/usr/bin/env python3
"""Apply the Works Catalogue design layer (30 Sep 2026).

The look now lives in site/site/assets/css/smag.css, loaded after the
inherited theme stylesheet on every page. This script makes the
markup changes the layer needs; copy is untouched.

1. Link smag.css after fonts.css on every page.
2. The thumb-index: a strip naming the six families at the top of every
   family and product page, marking the one you are in.
3. The closing action band gains call and WhatsApp buttons beside its
   existing line, so every page ends at the two routes a visit should end in.
4. A down-arrow at the foot of the home hero, linking to the product families.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
DRY = "--dry-run" in sys.argv

FONTS_LINK = "<link rel=stylesheet href=/site/assets/fonts/fonts.css>"
SMAG_LINK = "<link rel=stylesheet href=/site/assets/css/smag.css>"

FAMILIES = [
    ("filtration-systems", "Magnetic Filtration"),
    ("magnetic-separation-and-metal-detection", "Magnetic Separation"),
    ("magnetic-tools-and-standard-magnets", "Stock Magnets &amp; Tools"),
    ("workholding-systems", "Workholding Systems"),
    ("lifting-and-handling", "Lifting &amp; Handling"),
    ("oil-and-gas-pipeline-filtration", "Pipeline Filtration"),
]

ACTION_CONTACT = (
    "<div class=action-contact>"
    '<a class=ac-call href="tel:+919920143922"><i class="fas fa-phone" aria-hidden=true></i>+91 99201 43922</a>'
    '<a class=ac-wa href=https://wa.me/919920143922 target=_blank rel="noopener noreferrer">'
    '<i class="fab fa-whatsapp" aria-hidden=true></i>WhatsApp</a>'
    "</div>"
)


HERO_CUE = (
    '<a class=hero-cue href=#product-families aria-label="Scroll to the product families">'
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden=true><path d="M6 9.5l6 6 6-6" '
    'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
)
HERO_ANCHOR = '<div class=home-banner__container>'


def thumb_index(current: str, on_family_page: bool) -> str:
    links = []
    for slug, label in FAMILIES:
        mark = ""
        if slug == current:
            mark = " aria-current=page" if on_family_page else " aria-current=true"
        links.append(f"<a href=/products/{slug}/{mark}>{label}</a>")
    return ('<nav class=thumb-index aria-label="Product families"><div class=row__inner>'
            + "".join(links) + "</div></nav>")


def main() -> int:
    counts = dict(link=0, index=0, action=0)
    for f in sorted(SITE.rglob("*.html")):
        s = orig = f.read_text(encoding="utf-8")
        if SMAG_LINK not in s and FONTS_LINK in s:
            s = s.replace(FONTS_LINK, FONTS_LINK + "\n" + SMAG_LINK, 1)
            counts["link"] += 1

        parts = f.relative_to(SITE).parts
        if len(parts) >= 3 and parts[0] == "products" and "class=thumb-index" not in s:
            family = parts[1]
            if family in dict(FAMILIES):
                s = s.replace("<main id=main>", "<main id=main>" + thumb_index(family, len(parts) == 3), 1)
                counts["index"] += 1

        if f == SITE / "index.html" and "class=hero-cue" not in s and HERO_ANCHOR in s:
            s = s.replace(HERO_ANCHOR, HERO_ANCHOR + HERO_CUE, 1)
            counts["cue"] = counts.get("cue", 0) + 1

        a = s.find('<div class="row row--action">')
        if a >= 0 and "class=action-contact" not in s:
            h = s.find("</h3>", a)
            s = s[:h + 5] + ACTION_CONTACT + s[h + 5:]
            counts["action"] += 1

        if s != orig and not DRY:
            f.write_text(s, encoding="utf-8")
    for k, v in counts.items():
        print(f"  {k:6s} {v} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
