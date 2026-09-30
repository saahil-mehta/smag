#!/usr/bin/env python3
"""Link each product family to its guides.

Run after build_guides.py. A guide belongs to a family when its `product`
front matter points inside /products/<family>/. Each family page gets a
ruled Guides row just above the closing action band, one line per guide:
its title and its description, both taken from the guide's source. A family
with no guide gets no row. Re-running replaces the row, so it follows the
sources.

The sitemap page's Guides list also gains any guide it does not yet name;
build_guides.py only renames rows that already exist.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_guides import SRC, load  # noqa: E402
from remove_sections import find_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
SITEMAP = SITE / "sitemap/index.html"
DRY = "--dry-run" in sys.argv
OPEN = '<div class="row family-guides">'
ACTION = '<div class="row row--action">'
SITEMAP_GUIDES = "<li>&raquo; <a href=/resources/guides/>Guides</a><ul>"


def row(guides: list[dict]) -> str:
    items = "".join(
        f'<li><a href=/resources/guides/{g["slug"]}/>'
        f'<span class=family-guides__title>{html.escape(g["title"])}</span>'
        f'<span class=family-guides__text>{html.escape(g["description"])}</span></a>'
        for g in guides)
    return (OPEN + '<div class="row__inner row__intro"><h3 class=bordered-header>Guides</h3></div>'
            f"<div class=row__inner><ul class=family-guides__list>{items}</ul></div></div>")


def main() -> int:
    guides = sorted((load(p) for p in SRC.glob("*.md")), key=lambda g: g["title"])
    for fam in sorted((SITE / "products").iterdir()):
        page = fam / "index.html"
        if not page.exists():
            continue
        mine = [g for g in guides if g["product"].startswith(f"/products/{fam.name}/")]
        s = page.read_text(encoding="utf-8")
        start = s.find(OPEN)
        if start >= 0:
            s = s[:start] + s[find_element_end(s, start):]
        if mine:
            a = s.find(ACTION)
            if a < 0:
                raise SystemExit(f"no action band on {page}")
            s = s[:a] + row(mine) + s[a:]
        print(f"  {fam.name:42s} {len(mine)} guides")
        if not DRY:
            page.write_text(s, encoding="utf-8")

    sm = SITEMAP.read_text(encoding="utf-8")
    at = sm.find(SITEMAP_GUIDES)
    if at < 0:
        raise SystemExit("sitemap guides list not found")
    add = "".join(
        f'<li class=no-child>&raquo; <a href=/resources/guides/{g["slug"]}/>{html.escape(g["title"])}</a>'
        for g in guides if f'/resources/guides/{g["slug"]}/' not in sm)
    print(f"  sitemap: {add.count('<li')} guides added")
    if add and not DRY:
        cut = at + len(SITEMAP_GUIDES)
        SITEMAP.write_text(sm[:cut] + add + sm[cut:], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
