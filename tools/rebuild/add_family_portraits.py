#!/usr/bin/env python3
"""Show the whole Ingle family in the About page team block.

The supplied photo.pdf carries six portraits, one per page, in this order:
Sushil, Rahul, Deepak, Vijay, Santosh, Mandar. Rahul and Sushil were already
on the page as half-size renders of pages 2 and 1, so their files are kept;
the other four are rendered the same way, 543 x 724. Pages 4 and 6 are 4:5
rather than 3:4 and are centre-cropped to width first. The PDF images are
tagged sRGB, so the pixels need no colour conversion.

Masters go to assets/source/supplied/team/ as high-quality JPEGs.

The block moves from a two-column inline style to a grid--team rule: three
across from 768px, two across on phones, so six portraits sit as two full rows.
Roles are only shown where they are known. Vijay is shown as retired.

Usage:
    add_family_portraits.py --pdf ~/Downloads/photo.pdf [--dry-run]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pypdf
from PIL import Image

REPO = Path("/Users/saahil/Documents/GitHub/smag")
PAGE = REPO / "site/company/about-us/index.html"
CSS = REPO / "site/site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
IMG_DIR = REPO / "site/site/assets/images"
MASTERS = REPO / "assets/source/supplied/team"
SIZE = (543, 724)

# (name, role or None, pdf page index), in the order supplied.
FAMILY = [
    ("Sushil Ingle", "COO", 0),
    ("Rahul Ingle", "CEO", 1),
    ("Deepak Ingle", None, 2),
    ("Vijay Ingle", "Retired", 3),
    ("Santosh Ingle", None, 4),
    ("Mandar Ingle", None, 5),
]
KEEP = {"Sushil Ingle", "Rahul Ingle"}

MARKER = "/* smag: team grid */"
RULES = (
    f"\n{MARKER}\n"
    ".grid--team{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 14px;max-width:1000px}\n"
    "@media (min-width:768px){.grid--team{grid-template-columns:repeat(3,minmax(0,1fr));gap:40px 28px}}\n"
    "@media (max-width:549px){.grid--team .team__image h3{font-size:1em;padding:.6em .9em 0 0}}\n"
)

DRY = "--dry-run" in sys.argv
PDF = Path(sys.argv[sys.argv.index("--pdf") + 1]).expanduser() if "--pdf" in sys.argv else None


def slug(name: str) -> str:
    return "team-" + name.lower().replace(" ", "-") + ".jpg"


def to_3x4(im: Image.Image) -> Image.Image:
    w, h = im.size
    target_w = round(h * 3 / 4)
    if target_w < w:
        left = (w - target_w) // 2
        im = im.crop((left, 0, left + target_w, h))
    return im.resize(SIZE, Image.LANCZOS)


def card(name: str, role: str | None) -> str:
    return ("<div class=grid__item><div class=team__item><div class=team__image>"
            f'<img src=/site/assets/images/{slug(name)} width=543 height=724 '
            f'style="height:auto" alt="{name}" loading=lazy decoding=async />'
            f"<h3>{name}</h3></div>"
            + (f"<h6 class=bordered-header>{role}</h6>" if role else "")
            + "</div></div>")


def main() -> int:
    if PDF is None or not PDF.is_file():
        raise SystemExit("pass --pdf <photo.pdf>")
    pages = pypdf.PdfReader(PDF).pages
    if len(pages) != len(FAMILY):
        raise SystemExit(f"expected {len(FAMILY)} pages, found {len(pages)}")

    for name, _, idx in FAMILY:
        im = pages[idx].images[0].image.convert("RGB")
        master = MASTERS / slug(name)
        out = IMG_DIR / slug(name)
        action = "kept" if name in KEEP else "written"
        if not DRY:
            MASTERS.mkdir(parents=True, exist_ok=True)
            im.save(master, quality=95, subsampling=0)
            if name not in KEEP:
                to_3x4(im).save(out, quality=82, optimize=True, progressive=True)
        print(f"  {name:14s} page {idx + 1}  {im.size[0]}x{im.size[1]}  {out.name} {action}")

    s = PAGE.read_text(encoding="utf-8")
    m = re.search(r'<div class="grid grid--about"[^>]*>(?:<div class=grid__item>.*?</h6></div></div>)+</div>', s)
    if not m:
        if "grid--team" in s:
            print("team grid already in place")
            return 0
        raise SystemExit("team grid not found")
    grid = ('<div class="grid grid--team">'
            + "".join(card(n, r) for n, r, _ in FAMILY) + "</div>")
    if not DRY:
        PAGE.write_text(s[:m.start()] + grid + s[m.end():], encoding="utf-8")
    print(f"team grid rebuilt with {len(FAMILY)} people")

    css = CSS.read_text(encoding="utf-8")
    if MARKER not in css and not DRY:
        CSS.write_text(css + RULES, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
