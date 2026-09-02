#!/usr/bin/env python3
"""Flatten the site navigation to SMAG's five entries and drop search.

Header (desktop main-nav and the mobile drawer) becomes:

    Products (dropdown, six families) | Industries | Guides | About Us | Contact Us

Removed:
  - the Services menu (SMAG has no separate services pages; decided 2 Sep 2026)
  - the Company and Resources one-item dropdowns (their single pages move up)
  - Bespoke Magnet Design from the Products dropdown and the footer column
  - the search icon, search panel and mobile-drawer search (the site is
    static; /site-search/ was never fetched and has no backend)
  - the sticky call-to-action bar (quote, brochures, appointment) that sat
    over the page bottom; Saahil asked for it to go on 2 Sep 2026

The page trees themselves (services/, the bespoke family) are deleted by
drop_services_bespoke.py; this script only rewrites shared chrome.

Menus are replaced wholesale between exact markers rather than edited item
by item, so every page ends up with identical chrome. Depth-aware removal is
used for the search panel, which nests divs (see README lessons).

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

FAMILIES = [
    ("/products/filtration-systems/", "Magnetic Filtration"),
    ("/products/magnetic-separation-and-metal-detection/", "Magnetic Separation"),
    ("/products/magnetic-tools-and-standard-magnets/", "Stock Magnets &amp; Tools"),
    ("/products/workholding-systems/", "Workholding Systems"),
    ("/products/lifting-and-handling/", "Lifting &amp; Handling"),
    ("/products/oil-and-gas-pipeline-filtration/", "Pipeline Filtration"),
]


def family_items() -> str:
    return "".join(
        f'<li><a href={href} data-text="{name}"> <span>{name}</span> </a>'
        for href, name in FAMILIES
    )


MENU = (
    "<li class=parent><a href=# class=child-expander>\nProducts</a>"
    f"<div class=children><ul>{family_items()}</ul></div>"
    "<li><a href=/industries/>\nIndustries</a>"
    "<li><a href=/resources/guides/>\nGuides</a>"
    "<li><a href=/company/about-us/>\nAbout Us</a>"
    "<li><a href=/contact-us/>\nContact Us</a>"
)

MAIN_NAV_OPEN = "<nav class=main-nav><ul class=top-level-nav>"
DRAWER_OPEN = "<ul class=mobile-drawer__primary>"
OTHER_NAV_SEARCH = (
    '<nav class=other-nav><ul><li class=search-wrapper><a href=# class=expand-search>'
    ' <i class="fas fa-search fa-fw"></i> <span>Search</span> </a></ul>'
)
DRAWER_SEARCH = (
    '<ul class=mobile-drawer__secondary><li class=search-wrapper>'
    '<a href=# class=expand-search> <i class="fas fa-search fa-fw"></i>'
    " <span>Search</span> </a></ul>"
)
FOOTER_BESPOKE = (
    "<li><a href=/products/magnetic-materials-and-assemblies/>"
    "Bespoke Magnet Design</a>"
)


def replace_list(text: str, opener: str, closer: str, body: str) -> tuple[str, bool]:
    """Replace everything between `opener` and the next `closer` with body."""
    i = text.find(opener)
    if i < 0:
        return text, False
    j = text.find(closer, i + len(opener))
    if j < 0:
        return text, False
    return text[: i + len(opener)] + body + text[j:], True


def flatten(text: str) -> tuple[str, dict[str, int]]:
    hits = dict.fromkeys(["main", "drawer", "search", "panel", "footer", "sticky"], 0)
    # desktop: <nav class=main-nav><ul class=top-level-nav> ... </ul></nav>
    text, ok = replace_list(text, MAIN_NAV_OPEN, "</ul></nav>", MENU)
    hits["main"] += ok
    # mobile drawer primary list, closed by the secondary list or </div>
    i = text.find(DRAWER_OPEN)
    if i >= 0:
        end = find_element_end(text, i)
        if end:
            text = text[:i] + DRAWER_OPEN + MENU + "</ul>" + text[end:]
            hits["drawer"] += 1
    # search trigger in other-nav (keep the burger that follows it)
    if OTHER_NAV_SEARCH in text:
        text = text.replace(OTHER_NAV_SEARCH, "<nav class=other-nav>")
        hits["search"] += 1
    if DRAWER_SEARCH in text:
        text = text.replace(DRAWER_SEARCH, "")
        hits["search"] += 1
    # search panel: <div class=search> ... nested typeahead divs ... </div>
    m = re.search(r"<div class=search>", text)
    if m:
        end = find_element_end(text, m.start())
        if end:
            text = text[: m.start()] + text[end:]
            hits["panel"] += 1
    m = re.search(r"<div class=sticky-ctas>", text)
    if m:
        end = find_element_end(text, m.start())
        if end:
            text = text[: m.start()] + text[end:]
            hits["sticky"] += 1
    if FOOTER_BESPOKE in text:
        text = text.replace(FOOTER_BESPOKE, "")
        hits["footer"] += 1
    return text, hits


CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
# With search gone the other-nav holds only the (mobile) burger. The theme
# gives logo, main-nav and other-nav one flex share each, so the menu sat
# in the middle third with its items left-aligned. Let the menu shrink to
# its content and the equal outer shares centre it.
CSS_FIX = "\n/* smag: centre the flattened menu */header .main-nav{flex-grow:0}\n"


def main() -> None:
    dry = "--dry-run" in sys.argv
    if CSS.exists() and CSS_FIX.strip() not in CSS.read_text(encoding="utf-8"):
        if not dry:
            CSS.write_text(CSS.read_text(encoding="utf-8") + CSS_FIX, encoding="utf-8")
        print("css: menu centring rule appended")
    totals = dict.fromkeys(["main", "drawer", "search", "panel", "footer", "sticky"], 0)
    files = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        new, hits = flatten(text)
        if new == text:
            continue
        files += 1
        for k, v in hits.items():
            totals[k] += v
        if not dry:
            page.write_text(new, encoding="utf-8")
    print(f"{'DRY RUN: ' if dry else ''}{files} files changed")
    for k, v in totals.items():
        print(f"  {v:>4}  {k}")
    left = sum(
        1 for p in SITE.rglob("*.html")
        if "expand-search" in p.read_text(encoding="utf-8", errors="replace")
        or "/services/" in p.read_text(encoding="utf-8", errors="replace")[
            : p.read_text(encoding="utf-8", errors="replace").find("<main")]
    )
    print(f"pages still carrying search or services in chrome: {left}")


if __name__ == "__main__":
    main()
