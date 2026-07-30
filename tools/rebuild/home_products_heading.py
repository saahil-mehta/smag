#!/usr/bin/env python3
"""Remove the Industry Focus section and give the product grid a heading.

The 12 Industry Focus tiles are Eclipse's sectors (aerospace, pharmaceutical,
speaker magnets, oil and gas) and every tile links into /industries/, which is
13 pages of Eclipse content. Keeping the section would commit us to rewriting
all 13 to make the links honest.

The product grid above it had no heading at all: the first heading inside it
was a category name, so the tiles read as orphaned. It gains a "Product
Families" intro in the same row, matching how the rest of the site pairs a
row__intro with its content.

Removal is depth-aware. The section nests grid items several levels deep, so a
regex cannot bound it.
"""
from __future__ import annotations

import re
from pathlib import Path

PAGE = Path("/Users/saahil/Documents/GitHub/smag/site/index.html")

TAG_RE = re.compile(r"<(/?)(\w+)([^>]*)>")
VOID = {
    "img", "br", "hr", "input", "meta", "link", "source", "area", "base",
    "col", "embed", "param", "track", "wbr",
}

HEADING = (
    '<div class="row__inner row__intro">'
    "<h3 class=bordered-header>Product Families</h3>"
    '<p class="intro capped">Separation, filtration, lifting and workholding '
    "equipment, designed and machined at our own works in Mumbai. Tell us the "
    "application and we will point you at the right unit."
    "</div>"
)


def find_element_end(text: str, start: int) -> int | None:
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
    text = PAGE.read_text(encoding="utf-8")
    before = len(text)

    # 1. Remove the row that contains the Industry Focus heading.
    needle = ">Industry Focus<"
    i = text.find(needle)
    if i < 0:
        print("Industry Focus already removed")
    else:
        best = None
        for m in re.finditer(r'<div class="row\b[^"]*"', text):
            if m.start() > i:
                break
            end = find_element_end(text, m.start())
            if end and m.start() < i < end:
                span = end - m.start()
                if best is None or span < best[2]:
                    best = (m.start(), end, span)
        if not best:
            print("could not bound the Industry Focus row")
            return
        removed = text[best[0]:best[1]]
        text = text[: best[0]] + text[best[1]:]
        print(f"Industry Focus removed: {len(removed)} bytes, "
              f"{len(re.findall(r'<img|<source', removed))} img/source tags, "
              f"{len(re.findall(r'href=/industries/', removed))} sector links")

    # 2. Give the product grid a heading, inside its own row.
    if "Product Families" in text:
        print("heading already present")
    else:
        anchor = '<div class="row__inner home-categories">'
        assert anchor in text, "product grid not found"
        text = text.replace(anchor, HEADING + anchor, 1)
        print("Product Families heading added above the product grid")

    PAGE.write_text(text, encoding="utf-8")

    m = re.search(r"<main>.*</main>", text, re.DOTALL)
    seg = m.group(0)
    o, c = len(re.findall(r"<div\b", seg)), len(re.findall(r"</div>", seg))
    print(f"\n{before} -> {len(text)} bytes   div {o}/{c} "
          f"{'OK' if o == c else 'MISMATCH'}")
    print(f"/industries/ links left on the home page: "
          f"{len(re.findall(r'href=/industries/', seg))}")
    print("section order now:")
    for d in re.finditer(r'<div class="(row[^"]*)"', seg):
        nxt = seg[d.end():d.end() + 1200]
        h = re.search(r"<h[1-4][^>]*>(.*?)</h[1-4]>", nxt, re.DOTALL)
        label = re.sub(r"<[^>]+>", "", h.group(1)).strip()[:44] if h else ""
        print(f"  {d.group(1):26s} {label}")


if __name__ == "__main__":
    main()
