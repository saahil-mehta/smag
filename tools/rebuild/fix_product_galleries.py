#!/usr/bin/env python3
"""Make every product gallery behave the same way.

- One image: no arrows and no thumbnail strip. There is nothing to move to.
- Two or more images: arrows plus a "2 / 3" counter. javascript.js runs the
  gallery without looping, so the arrow at either end greys out.
- The lifter's second photo is the first photo recropped; it is dropped and
  the thumbnails renumbered.

Works on the English product pages; make i18n carries the change into the
language copies.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
DRY = "--dry-run" in sys.argv

ARROWS = "<button class=prev></button><button class=next></button>"
COUNT = "<div class=gallery-count></div>"
SLIDE = re.compile(r'<div class="product__image swiper-slide">.*?<p class=zoom-tip>.*?</div>', re.S)
THUMBS = re.compile(r"<div class=product__thumbnails>(?:<a href=# data-img=\d+><div [^>]*></div></a>)*</div>")
DROP = {"products/lifting-and-handling/permanent-magnetic-lifter": "permanent-magnetic-lifter-02"}


def renumber(thumbs: str) -> str:
    n = iter(range(1, 100))
    return re.sub(r"data-img=\d+", lambda _: f"data-img={next(n)}", thumbs)


def fix(rel: str, s: str) -> str:
    stem = DROP.get(rel)
    if stem:
        s = SLIDE.sub(lambda m: "" if f"/{stem}.hero." in m.group(0) else m.group(0), s)
        s = re.sub(rf"<a href=# data-img=\d+><div [^>]*/{stem}\.thumb\.jpg[^>]*></div></a>", "", s)
        s = THUMBS.sub(lambda m: renumber(m.group(0)), s)
    start = s.index('<div class="product__gallery')
    end = s.index('<div class="product__intro', start)
    gallery = s[start:end]
    slides = len(SLIDE.findall(gallery))
    gallery = gallery.replace(ARROWS + COUNT, ARROWS)
    if slides < 2:
        gallery = gallery.replace(ARROWS, "")
        gallery = THUMBS.sub("", gallery)
    elif ARROWS in gallery:
        gallery = gallery.replace(ARROWS, ARROWS + COUNT)
    else:
        raise ValueError(f"{rel}: {slides} slides and no arrows")
    return s[:start] + gallery + s[end:]


def main() -> None:
    for page in sorted(SITE.glob("products/*/*/index.html")):
        rel = str(page.parent.relative_to(SITE))
        s = page.read_text(encoding="utf-8")
        new = fix(rel, s)
        if new != s:
            print(f"{'would fix' if DRY else 'fixed'} {rel}")
            if not DRY:
                page.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    main()
