#!/usr/bin/env python3
"""Repair the seven Stock Magnets & Tools product pages and give them the
product header every other product page has.

What went wrong: scrub_image_branding.py asked replace_gallery() to swap
the gallery on these pages, but the tools pages never had one. Their
<main> opens with the sub-nav and goes straight into the tabbed details;
there is no product__top row, no gallery and no <h1>. find() returned -1,
find_element_end() returned None, and text[:-1] + gallery + text[None:]
wrote each page as: the page, the new gallery, then the whole page again.
Browsers rendered the second copy as visible junk below the footer.

Repair: keep the second copy (it is the clean pre-gallery page), then
insert a product__top row after the sub-nav, composed of the site's own
classes exactly as build_smag_product_pages.py does: breadcrumbs, the
SMAG gallery from the GALLERIES specs, an <h1> taken from the page title,
and the Get a quote button. No tagline or bullets are invented.

Also removes the "Our Global Distributors" sub-nav item that an earlier
dead-link unwrap left as bare text on nine family pages.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_smag_product_pages as build  # noqa: E402
from scrub_image_branding import GALLERIES, pseudo_img  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
FAM = "magnetic-tools-and-standard-magnets"
FAM_NAME = "Stock Magnets &amp; Tools"
DETAILS_OPEN = '<div class=row><div class="row__inner product__details">'
DISTRIBUTORS = re.compile(r"<li>\s*Our Global Distributors\s*</a>")


def product_top(name: str, slides: str) -> str:
    return (
        '<div class="row row--alt row--x-small-padding">'
        '<div class="row__inner product__top"><div class=product__top-left>'
        "<div class=breadcrumbs><div class=row__inner>"
        "<span>&nbsp;/&nbsp;</span>\n"
        f"<a href=/products/{FAM}/>{FAM_NAME}</a>"
        f"<span>&nbsp;/&nbsp;</span>{name} </div></div>"
        '<div class="product__gallery swiper-container '
        'gallery-swiper-container">'
        f'<div class="product__images swiper-wrapper">{slides}</div>'
        "<button class=prev></button><button class=next></button></div></div>"
        '<div class="product__intro content">'
        f"<h1 class=bordered-header>{name}</h1>"
        '<div class=c2a><a href=/contact-us/ class="button button--large '
        'button--full button--with-arrow">Get a quote</a></div>'
        "</div></div></div>"
    )


def repair(text: str, specs: list[tuple[str, str]]) -> str:
    docs = [m.start() for m in re.finditer(r"<!DOCTYPE", text)]
    if len(docs) == 2:
        text = text[docs[1]:]
    elif len(docs) != 1:
        raise ValueError(f"unexpected document count {len(docs)}")
    if "gallery-swiper-container" in text:
        raise ValueError("page already carries a gallery")
    name = re.search(r"<title>([^|<]*)\|", text).group(1).strip()
    imgs = [pseudo_img(s) if s.startswith("/") else build.renditions(s)
            for s, _ in specs]
    slides = "".join(build.slide(im, alt) for im, (_, alt) in zip(imgs, specs))
    i = text.find(DETAILS_OPEN)
    if i < 0:
        raise ValueError("no product details row to anchor on")
    return text[:i] + product_top(name, slides) + text[i:]


def main() -> None:
    dry = "--dry-run" in sys.argv
    for rel, specs in GALLERIES.items():
        if not rel.startswith(f"products/{FAM}/"):
            continue
        page = SITE / rel / "index.html"
        text = page.read_text(encoding="utf-8")
        new = repair(text, specs)
        print(f"repaired {rel}: {len(text)} -> {len(new)} chars, "
              f"{len(specs)} slides, h1 set")
        if not dry:
            page.write_text(new, encoding="utf-8")

    n = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        new, k = DISTRIBUTORS.subn("", text)
        if k:
            n += 1
            if not dry:
                page.write_text(new, encoding="utf-8")
    print(f"distributor sub-nav leftovers removed from {n} pages")

    dup = [p for p in SITE.rglob("*.html")
           if p.read_text(encoding="utf-8").count("<body") > 1]
    print(f"pages with more than one <body>: {len(dup)}")


if __name__ == "__main__":
    main()
