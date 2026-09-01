#!/usr/bin/env python3
"""Remove every internal link that points at a page that does not exist.

The mirror was a partial crawl, so the site has always carried links to
pages that were never fetched (the sitemap page alone listed over a hundred),
and the range pruning added more. This sweep runs after the new SMAG pages
are built, so anything still dead has nothing to point at.

For each dead href the innermost enclosing tile, card or list row is removed
(depth-aware, per the README lessons); a dead link in running prose is
unwrapped so the text stays.

Also repoints the home hero CTA, which linked to /products/ (a page that has
never existed) at the Product Families grid on the same page.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end, li_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

CONTAINER_RES = [
    re.compile(r'<div class="?grid__item\b[^>]*>'),
    re.compile(r'<div class="?swiper-slide\b[^>]*>'),
    re.compile(r"<li\b[^>]*>"),
]

HREF_RE = re.compile(r'<a\s[^>]*?href=(?:"([^"]+)"|([^\s>]+))[^>]*>')

# dead paths whose product now lives at another URL: rewrite, do not remove
REWRITES = {
    "/products/magnetic-tools-and-standard-magnets/table-top-demagnetiser/":
        "/products/workholding-systems/table-top-demagnetiser/",
    "/products/magnetic-tools-and-standard-magnets/rectangular-premier-chuck/":
        "/products/workholding-systems/rectangular-premier-chuck/",
    "/products/magnetic-tools-and-standard-magnets/circular-premier-chuck/":
        "/products/workholding-systems/circular-premier-chuck/",
    "/products/magnetic-tools-and-standard-magnets/gauss-meter/":
        "/products/magnetic-separation-and-metal-detection/gauss-meter/",
}


def exists(path: str) -> bool:
    path = unquote(path.split("#", 1)[0].split("?", 1)[0])
    if not path or path == "/":
        return True
    p = SITE / path.lstrip("/")
    if path.endswith("/"):
        return (p / "index.html").exists()
    return p.exists() or (p / "index.html").exists() or \
        Path(str(p) + ".html").exists()


def scrub(text: str) -> tuple[str, int, set[str]]:
    removed = 0
    dead: set[str] = set()
    while True:
        hit = None
        for m in HREF_RE.finditer(text):
            href = m.group(1) or m.group(2)
            if not href.startswith("/"):
                continue
            if exists(href):
                continue
            hit = (m, href)
            break
        if hit is None:
            return text, removed, dead
        m, href = hit
        dead.add(href)
        best = None
        for cre in CONTAINER_RES:
            for c in cre.finditer(text, 0, m.start()):
                # minified <li> has no closing tag; bound it by its sibling
                end = find_element_end(text, c.start())
                if end is None and text[c.start():c.start() + 3] == "<li":
                    end = li_element_end(text, c.start())
                if end and c.start() < m.start() < end:
                    span = end - c.start()
                    if best is None or span < best[2]:
                        best = (c.start(), end, span)
        if best:
            text = text[: best[0]] + text[best[1]:]
        else:
            # unwrap: keep the anchor's inner text in place
            a_end = find_element_end(text, m.start())
            if a_end:
                inner = text[m.end():a_end - len("</a>")]
                text = text[: m.start()] + inner + text[a_end:]
            else:
                text = text[: m.start()] + text[m.end():]
        removed += 1


HOME_CTA_OLD = "<a href=/products/ class=button>"
HOME_CTA_NEW = "<a href=#product-families class=button>"
HOME_HEADING_OLD = "<h3 class=bordered-header>Product Families"
HOME_HEADING_NEW = ('<h3 class=bordered-header id=product-families>'
                    "Product Families")


def main() -> None:
    dry = "--dry-run" in sys.argv
    total = 0
    all_dead: dict[str, int] = {}
    for page in sorted(SITE.rglob("*.html")):
        orig = text = page.read_text(encoding="utf-8")
        # orphan bullets: an earlier pass unwrapped dead anchors inside
        # unclosed <li> rows (sitemap), leaving bare "&raquo; Name" text
        text = re.sub(
            r"<li class=no-child>&raquo;(?:(?!<li\b|</ul>|<a\s)[\s\S])*"
            r"(?=<li\b|</ul>)", "", text)
        text = text.replace("<ul></ul>", "")
        for old, new_url in REWRITES.items():
            text = text.replace(old, new_url)
        # rewrites must run BEFORE the scrub: the first pass of this script
        # ran them after, so the scrub saw the hero CTA's dead /products/
        # link and removed the enclosing hero slide (restore_home_hero.py
        # is the repair). Keep this order.
        if page == SITE / "index.html":
            text = text.replace(HOME_CTA_OLD, HOME_CTA_NEW)
            if HOME_HEADING_NEW not in text:
                text = text.replace(HOME_HEADING_OLD, HOME_HEADING_NEW)
        new, n, dead = scrub(text)
        if new == orig:
            continue
        for d in dead:
            all_dead[d] = all_dead.get(d, 0) + 1
        total += n
        print(f"{n:3d} dead-link removals  {page.relative_to(SITE)}")
        if not dry:
            page.write_text(new, encoding="utf-8")
    print(f"\ntotal removals: {total}")
    for d in sorted(all_dead):
        print(f"  {all_dead[d]:3d}x {d}")


if __name__ == "__main__":
    main()
