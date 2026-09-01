#!/usr/bin/env python3
"""Reduce site/ to a single English site with the unwanted sections removed.

Deletes:
  - the locale trees cn/ de/ fr/ en-us/ en-gb/  (Eclipse's own translations)
  - case-studies/ news/ partner-login/
  - company/net-zero/ company/become-a-distributor/

Then removes what pointed at them: nav items, dropdown entries, sitemap rows,
carousel cards, "related case studies" sections, hreflang alternates and the
country selector.

Container removal is depth-aware, not regex-bounded. A regex cannot match a
<div> containing nested <div>s, and bounding one with a negative lookahead is
how an earlier sweep here destroyed a footer across 318 pages.
find_element_end walks the tag stack, so a removal cannot extend past the
element it started in.

Section headings are matched as exact full strings for the same reason: an
earlier draft listed a bare "Case Studies", which matched unintended headings
and took their enclosing rows with them.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

LOCALE_DIRS = ["cn", "de", "fr", "en-us", "en-gb"]
SECTION_DIRS = [
    "case-studies",
    "news",
    "partner-login",
    "company/net-zero",
    "company/become-a-distributor",
]
DROP_DIRS = LOCALE_DIRS + SECTION_DIRS

# URL paths belonging to anything removed.
SLUG_RE = re.compile(
    r"/(?:cn|de|fr|en-us|en-gb|case-studies|news|partner-login|"
    r"company/net-zero|company/become-a-distributor)(?:/|\b)"
)

# Exact section headings whose whole enclosing row goes.
SECTION_HEADINGS = [
    "<h3 class=bordered-header>Recent News &amp; Case Studies</h3>",
    "<h3 class=bordered-header>Related case studies</h3>",
    '<h3 class="configurable-header bordered-header">Related case studies</h3>',
]

TAG_RE = re.compile(r"<(/?)(\w+)([^>]*)>")
VOID = {
    "img", "br", "hr", "input", "meta", "link", "source", "area", "base",
    "col", "embed", "param", "track", "wbr",
}


def find_element_end(text: str, start: int) -> int | None:
    """Index just past the element opening at `start`, tracking nesting."""
    m = TAG_RE.match(text, start)
    if not m or m.group(1):
        return None
    name = m.group(2).lower()
    if name in VOID or m.group(3).rstrip().endswith("/"):
        return m.end()

    depth = 0
    for t in TAG_RE.finditer(text, start):
        if t.group(2).lower() != name:
            continue
        if t.group(1):
            depth -= 1
            if depth == 0:
                return t.end()
        else:
            if not t.group(3).rstrip().endswith("/"):
                depth += 1
    return None


def remove_enclosing_row(text: str, needle: str) -> tuple[str, int]:
    """Remove the innermost <div class="row..."> containing each `needle`."""
    removed = 0
    while True:
        i = text.find(needle)
        if i < 0:
            return text, removed
        best = None
        for m in re.finditer(r'<div class="?row\b', text):
            if m.start() > i:
                break
            end = find_element_end(text, m.start())
            if end and m.start() < i < end:
                span = end - m.start()
                if best is None or span < best[2]:
                    best = (m.start(), end, span)
        if best:
            text = text[: best[0]] + text[best[1] :]
        else:
            text = text.replace(needle, "", 1)
        removed += 1


def remove_dead_cards(text: str) -> tuple[str, int]:
    """Remove cards whose every link points at something removed."""
    removed = 0
    for cls in (
        r'<div class="swiper-slide[^"]*"',
        r"<div class=swiper-slide\b",
        r'<div class="grid__item[^"]*"',
    ):
        while True:
            hit = None
            for m in re.finditer(cls, text):
                end = find_element_end(text, m.start())
                if not end:
                    continue
                inner = text[m.start() : end]
                links = re.findall(r'href=["\']?([^"\' >]+)', inner)
                if links and all(SLUG_RE.search(h) for h in links):
                    hit = (m.start(), end)
                    break
            if not hit:
                break
            text = text[: hit[0]] + text[hit[1] :]
            removed += 1
    return text, removed


SLUGS = (
    r"cn|de|fr|en-us|en-gb|case-studies|news|partner-login|"
    r"net-zero|become-a-distributor"
)
# Each of these keeps [^<]* for the label, so a match stays inside one anchor.
LI_RE = re.compile(
    rf"<li[^>]*>(?:\s|&raquo;|&nbsp;)*"
    rf"<a [^>]*href=[\"']?/(?:{SLUGS})[^\"' >]*[\"']?[^>]*>[^<]*</a>[^<]*"
)
LINK_RE = re.compile(
    rf"<a [^>]*href=[\"']?/(?:{SLUGS})[^\"' >]*[\"']?[^>]*>[^<]*</a>\s*(?:\|\s*)?"
)
HREFLANG_RE = re.compile(r"<link rel=alternate[^>]*hreflang=[^>]*>")
VIEWMORE_RE = re.compile(
    rf"<p class=view-more>\s*<a [^>]*href=[\"']?/(?:{SLUGS})[^>]*>[^<]*</a>\s*"
)


def main() -> None:
    dry = "--dry-run" in sys.argv
    drop_prefixes = [str(SITE / d) for d in DROP_DIRS]
    stats = dict.fromkeys(
        ["sections", "cards", "li", "links", "hreflang", "viewmore", "selectors"], 0
    )
    files = 0

    for page in sorted(SITE.rglob("*.html")):
        s = str(page)
        if any(s.startswith(p + "/") for p in drop_prefixes):
            continue
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        original = text

        for h in SECTION_HEADINGS:
            if h in text:
                text, n = remove_enclosing_row(text, h)
                stats["sections"] += n

        text, n = remove_dead_cards(text)
        stats["cards"] += n

        text, n = HREFLANG_RE.subn("", text)
        stats["hreflang"] += n

        # Country selector: <li class="parent locale-wrapper"> holding an <a>
        # and a nested <div class="children country-list">. The <li> has no
        # closing tag, so bound the removal by that div's depth-aware end.
        while True:
            m = re.search(r'<li class="parent locale-wrapper">', text)
            if not m:
                break
            d = re.compile(r'<div class="children country-list"').search(text, m.end())
            if not d:
                break
            end = find_element_end(text, d.start())
            if not end:
                break
            text = text[: m.start()] + text[end:]
            stats["selectors"] += 1

        text, n = VIEWMORE_RE.subn("", text)
        stats["viewmore"] += n
        text, n = LI_RE.subn("", text)
        stats["li"] += n
        text, n = LINK_RE.subn("", text)
        stats["links"] += n

        if text != original:
            files += 1
            if not dry:
                page.write_text(text, encoding="utf-8")

    print(f"{'DRY RUN: ' if dry else ''}{files} files changed")
    for k, v in stats.items():
        print(f"  {v:>6}  {k}")

    if not dry:
        for d in DROP_DIRS:
            p = SITE / d
            if p.exists():
                n = len(list(p.rglob("*.html")))
                shutil.rmtree(p)
                print(f"  deleted {d}/  ({n} pages)")

    left = sum(
        len(SLUG_RE.findall(p.read_text(encoding="utf-8", errors="replace")))
        for p in SITE.rglob("*.html")
    )
    print(f"\nresidual references: {left}")
    print(f"pages remaining: {len(list(SITE.rglob('*.html')))}")


if __name__ == "__main__":
    main()


def li_element_end(text: str, start: int) -> int | None:
    """End of a minified <li> that has no closing tag.

    The site's HTML relies on implicit </li>, so find_element_end cannot
    bound a list item. A leaf <li> ends at the next sibling <li> or the
    parent's </ul>/</ol>. If a nested <ul> opens first, the item is a
    parent (nav dropdowns) and None is returned so callers fall back.
    """
    m = TAG_RE.match(text, start)
    if not m or m.group(2).lower() != "li":
        return None
    nxt = re.search(r"<li\b|</li>|</ul>|</ol>|<ul\b|<ol\b", text[m.end():])
    if not nxt:
        return None
    if nxt.group(0).startswith(("<ul", "<ol")):
        return None
    if nxt.group(0) == "</li>":
        return m.end() + nxt.end()
    return m.end() + nxt.start()
