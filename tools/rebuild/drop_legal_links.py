#!/usr/bin/env python3
"""Remove the Extranet Terms of Use and Conditions of Purchase pages from site/.

Both are Eclipse legal text with no SMAG equivalent, so the links go and the
pages go with them rather than being left orphaned but reachable by URL.

The Privacy Policy and Cookie Policy links are kept; those pages get SMAG
content.

Matching is deliberately tight. An earlier version used a negative lookahead
for "<li>" as a boundary, which is not a boundary at all in a region that
contains no <li>, and it ran on to swallow the whole footer lower bar. Both
patterns here are anchored on the anchor tag itself and cannot span it.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
SLUGS = "extranet-terms-of-use|conditions-of-purchase"

DROP_DIRS = [
    SITE / "information/extranet-terms-of-use",
    SITE / "information/conditions-of-purchase",
]

# A sitemap row: <li ...>&raquo; <a href=...slug...>text</a> with nothing else.
# [^<]* for the label means this can never cross a tag boundary.
SITEMAP_LI_RE = re.compile(
    rf"<li[^>]*>(?:\s|&raquo;|&nbsp;)*"
    rf"<a href=[^>]*(?:{SLUGS})[^>]*>[^<]*</a>[^<]*"
)

# A plain footer/inline link, plus any trailing " | " separator.
# [^<]* again keeps the match inside the single anchor.
ANCHOR_RE = re.compile(
    rf"<a href=[^>]*(?:{SLUGS})[^>]*>[^<]*</a>\s*(?:\|\s*)?"
)


def main() -> None:
    anchors = lis = files = 0

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if page.parent in DROP_DIRS:
            continue

        original = text
        text, n = SITEMAP_LI_RE.subn("", text)
        lis += n
        text, n = ANCHOR_RE.subn("", text)
        anchors += n

        if text != original:
            page.write_text(text, encoding="utf-8")
            files += 1

    print(f"{files} files rewritten: {lis} sitemap rows, {anchors} anchors removed")

    for d in DROP_DIRS:
        if d.exists():
            shutil.rmtree(d)
            print(f"removed page: {d.relative_to(SITE)}")

    left = sum(
        len(re.findall(SLUGS, p.read_text(encoding="utf-8", errors="replace")))
        for p in SITE.rglob("*.html")
    )
    print(f"\nreferences remaining: {left}")


if __name__ == "__main__":
    main()
