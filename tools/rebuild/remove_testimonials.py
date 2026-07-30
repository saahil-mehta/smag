#!/usr/bin/env python3
"""Remove the Eclipse testimonial carousels from site/.

Nine quotes attributed to named individuals at AB MAURI, Roquette, Vallourec,
the Nuclear AMRC, Simpsons Malt and others, all endorsing Eclipse. On this site
they would present other firms' endorsements as SMAG's.

Careful with the string "testimonial": 180 pages contain it, but most are the
layout class `content-wrapper--no-testimonials`, which must survive. Only
`<div class="row testimonials">` elements are removed.

Removal is depth-aware. The carousel nests divs several levels deep, so a
regex cannot match it: `.*?</div>` stops at the first inner close, and an
unbounded `.*` runs to the end of the document.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

TAG_RE = re.compile(r"<(/?)(\w+)([^>]*)>")
VOID = {
    "img", "br", "hr", "input", "meta", "link", "source", "area", "base",
    "col", "embed", "param", "track", "wbr",
}
OPEN_RE = re.compile(r'<div class="row testimonials"[^>]*>')


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
        elif not t.group(3).rstrip().endswith("/"):
            depth += 1
    return None


def main() -> None:
    dry = "--dry-run" in sys.argv
    rows = files = 0
    unbalanced = []

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        original = text

        while True:
            m = OPEN_RE.search(text)
            if not m:
                break
            end = find_element_end(text, m.start())
            if not end:
                print(f"  UNTERMINATED in {page.relative_to(SITE)}")
                break
            text = text[: m.start()] + text[end:]
            rows += 1

        if text != original:
            files += 1
            main_m = re.search(r"<main>.*</main>", text, re.DOTALL)
            if main_m:
                seg = main_m.group(0)
                o, c = len(re.findall(r"<div\b", seg)), len(re.findall(r"</div>", seg))
                if o != c:
                    unbalanced.append((str(page.relative_to(SITE)), o, c))
            if not dry:
                page.write_text(text, encoding="utf-8")

    print(f"{'DRY RUN: ' if dry else ''}{rows} testimonial rows removed "
          f"from {files} files")
    print(f"pages left unbalanced: {len(unbalanced)}")
    for u in unbalanced[:5]:
        print(f"  {u[0]}: {u[1]}/{u[2]}")

    slides = quotes = keeps = 0
    for p in SITE.rglob("*.html"):
        t = p.read_text(encoding="utf-8", errors="replace")
        slides += len(re.findall(r'class="swiper-slide testimonial"', t))
        quotes += len(re.findall(r"testimonial__author", t))
        keeps += len(re.findall(r"content-wrapper--no-testimonials", t))
    print(f"\nremaining testimonial slides: {slides}   author lines: {quotes}")
    print(f"'--no-testimonials' layout classes preserved: {keeps}")


if __name__ == "__main__":
    main()
