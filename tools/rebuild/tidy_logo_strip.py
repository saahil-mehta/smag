#!/usr/bin/env python3
"""Lay the client logo strip out as a grid instead of a wrapping flex row.

flex-wrap left whatever remainder fell out on the last line: at desktop width
that was a single logo sitting next to the label, which reads as a mistake.

There are 30 logos, and 30 divides evenly by 6, 5, 3 and 2, so a grid with
those column counts gives completely full rows at every breakpoint. The
"+ many more" label moves below the grid: as a 31st cell it would break that.

Rules go in a small scoped <style> block rather than inline attributes, so the
column count can respond to width. Idempotent: re-running replaces the strip.
"""
from __future__ import annotations

import re
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
PAGES = ["index.html", "company/about-us/index.html"]

STYLE_ID = "smag-clients-css"
STYLE = (
    f'<style id={STYLE_ID}>'
    ".clients-strip{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));"
    "gap:36px 40px;align-items:center;justify-items:center}"
    ".clients-strip img{height:60px;width:auto;max-width:100%;"
    "object-fit:contain}"
    ".clients-more{text-align:center;margin:34px 0 0;font-weight:600;"
    "color:#6b6770}"
    "@media(max-width:1180px){.clients-strip"
    "{grid-template-columns:repeat(5,minmax(0,1fr))}}"
    "@media(max-width:880px){.clients-strip"
    "{grid-template-columns:repeat(3,minmax(0,1fr))}}"
    "@media(max-width:540px){.clients-strip"
    "{grid-template-columns:repeat(2,minmax(0,1fr));gap:26px 20px}}"
    "</style>"
)

# The strip holds only <img> and one <span>, no nested divs, so </div> ends it.
# Include any trailing label in the match, otherwise re-running appends a
# second one instead of replacing the first.
STRIP_RE = re.compile(
    r'<div class=clients-strip[^>]*>((?:(?!</div>)[\s\S])*)</div>'
    r'(?:\s*<p class=clients-more>[^<]*</p>)*'
)
IMG_RE = re.compile(r"<img [^>]*?/site/assets/images/clients/[^>]*>")


def main() -> None:
    for rel in PAGES:
        page = SITE / rel
        text = page.read_text(encoding="utf-8")

        m = STRIP_RE.search(text)
        if not m:
            print(f"  {rel}: NO strip found")
            continue

        # Reuse the existing <img> tags, stripped of their inline sizing.
        imgs = IMG_RE.findall(m.group(1))
        cleaned = [
            re.sub(r'\s*style="[^"]*"', "", i).replace(" height=60", "")
            for i in imgs
        ]
        new_strip = (
            "<div class=clients-strip>" + "".join(cleaned) + "</div>"
            '<p class=clients-more>+ many more</p>'
        )
        text = text[: m.start()] + new_strip + text[m.end():]

        # These pages are minified and omit </head> (an optional end tag), so
        # the style block goes immediately before <body.
        added = False
        if STYLE_ID not in text:
            text, n = re.subn(r"(?=<body\b)", STYLE, text, count=1)
            added = bool(n)

        page.write_text(text, encoding="utf-8")
        print(f"  {rel}: {len(cleaned)} logos re-laid as a grid, style block "
              f"{'added' if added else 'already present'}")


if __name__ == "__main__":
    main()
