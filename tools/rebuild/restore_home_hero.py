#!/usr/bin/env python3
"""Reinstate the SMAG hero slide on the home page.

The first pass of scrub_dead_links.py ran its dead-link sweep before the
home CTA rewrite, so the hero's "See the range" button (which pointed at
/products/, a page that has never existed) took the whole first hero slide
with it, video and all. The video and poster assets survived at
/site/assets/images/hero-lifter.{mp4,jpg}; this script rebuilds the slide in
front of the remaining banner slides, with the CTA pointing at the Product
Families grid.

Idempotent: does nothing if the slide is already present.
"""
from __future__ import annotations

from pathlib import Path

PAGE = Path("/Users/saahil/Documents/GitHub/smag/site/index.html")

WRAPPER = ('<div class="swiper-container pagination-swiper-manual-container">'
           "<div class=swiper-wrapper>")

SLIDE = (
    "<div class=swiper-slide><div class=row__inner><div class=banner__text>"
    "<h1 class=regular>Magnetic equipment built and tested in our own works"
    "</h1><div class=c2a><a href=#product-families class=button>\n"
    "See the range </a></div></div></div>"
    "<video width=1224 height=720 class=responsive-video autoplay "
    "playsinline loop muted poster=/site/assets/images/hero-lifter-poster.jpg>"
    "<source src=/site/assets/images/hero-lifter.mp4 type=video/mp4>"
    "</video></div>"
)


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    if "hero-lifter.mp4" in text:
        print("hero slide already present, nothing to do")
        return
    i = text.find(WRAPPER)
    if i < 0:
        raise SystemExit("hero swiper wrapper not found")
    j = i + len(WRAPPER)
    PAGE.write_text(text[:j] + SLIDE + text[j:], encoding="utf-8")
    print("hero slide reinstated as slide 1")


if __name__ == "__main__":
    main()
