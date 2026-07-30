#!/usr/bin/env python3
"""Rebuild the home product grid as SMAG's six real families.

Drops Metal Detection and Pipeline Filtration: SMAG does not make either.
Adds Magnetic Grills and Workshop Tools, which SMAG does make and Eclipse's
grid never showed.

Descriptions are reworded from the Eclipse tiles rather than lifted from SMAG's
pre-takedown pages, which were AI-written. Eclipse's phrasing was written by
people for a real magnetics manufacturer, so it is the better base. The claims
are checked against SMAG's actual range, not carried over.
"""
from __future__ import annotations

import re
from pathlib import Path

PAGE = Path("/Users/saahil/Documents/GitHub/smag/site/index.html")
IMG = "/site/assets/images/products"

# (slug, name, href, description, alt)
# Description lineage, Eclipse -> reworded for SMAG:
#   "Separation systems for food processing, chemicals & pharmaceuticals."
#     -> tramp iron wording, since SMAG's range is bulk handling
#   "Filtration systems for metalworking fluids, CNC machine tools &
#    centralised fluid tanks." -> kept close, it already fits
#   "Safely and efficiently lift ferrous loads with the power of magnetics."
#     -> drops the "power of magnetics" flourish
#   "Drive production efficiency & precision with magnetic chucks for milling
#    & grinding." -> drops "drive production efficiency"
#   "A wide range of magnets, magnetic materials, magnetic workshop tools and
#    accessories." -> split: tools tile keeps this, grills tile is new
TILES = [
    ("separators", "Magnetic Separators",
     "/products/magnetic-separation-and-metal-detection/",
     "Separators for chutes, conveyors and process lines carrying tramp iron.",
     "Magnetic separator with pull-out magnetic bars"),
    ("filters", "Magnetic Filters",
     "/products/filtration-systems/",
     "Filters for metalworking fluids, CNC machine tools and central fluid tanks.",
     "Skid-mounted magnetic filtration unit"),
    ("lifters", "Magnetic Lifters",
     "/products/lifting-and-handling/",
     "Lever-operated lifting magnets for steel plate, block and round bar.",
     "Permanent magnetic lifter holding a steel plate"),
    ("chucks", "Magnetic Chucks",
     "/products/workholding-systems/",
     "Chucks that hold work for grinding, turning, milling and inspection.",
     "Round permanent magnetic chuck"),
    ("grills", "Magnetic Grills",
     "/products/magnetic-separation-and-metal-detection/",
     "Hopper and chute grills that take fine iron out of powders and granules.",
     "Hopper magnetic grill with magnetic tubes"),
    ("tools", "Workshop Tools",
     "/products/magnetic-tools-and-standard-magnets/",
     "V-blocks, tool racks, demagnetisers and magnets across grades and shapes.",
     "Magnetic V-block, tool rack and demagnetiser"),
]


def tile(slug, name, href, desc, alt) -> str:
    srcset = ",".join(
        f"{IMG}/{slug}.{w}.jpg {w}w" for w in (200, 300)
    ) + f",{IMG}/{slug}.jpg 405w,{IMG}/{slug}.810.jpg 810w"
    return (
        "<div class=grid__item>"
        f"<a href={href} class=expandHint> "
        f"<img src={IMG}/{slug}.jpg "
        f'srcset="{srcset}" sizes="(max-width: 405px) 100vw, 405px" '
        f'width=405 height=260 alt="{alt}" loading=lazy decoding=async />'
        f"<div class=expandHint__text><h2>{name}</h2><p>{desc}"
        "<div class=expandHint__positioner>"
        '<p class="read-more expandHint__hidden">Read more</div></div></a></div>'
    )


GRID_RE = re.compile(
    r'(<div class="row__inner home-categories"><div class="grid grid--products">)'
    r"(?:(?!</div></div>)[\s\S])*"
    r"(</div></div>)"
)


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    before = len(text)

    m = GRID_RE.search(text)
    if not m:
        # Fall back to a depth-aware bound on the grid.
        i = text.find('<div class="grid grid--products">')
        if i < 0:
            print("product grid not found")
            return
        depth = 0
        end = None
        for t in re.finditer(r"<div\b[^>]*>|</div>", text[i:]):
            depth += -1 if t.group(0).startswith("</") else 1
            if depth == 0:
                end = i + t.end()
                break
        if end is None:
            print("could not bound the grid")
            return
        new = '<div class="grid grid--products">' + "".join(tile(*t) for t in TILES) + "</div>"
        text = text[:i] + new + text[end:]
    else:
        text = (
            text[: m.start()]
            + m.group(1)
            + "".join(tile(*t) for t in TILES)
            + m.group(2)
            + text[m.end():]
        )

    PAGE.write_text(text, encoding="utf-8")

    seg = re.search(r"<main>.*</main>", text, re.DOTALL).group(0)
    o, c = len(re.findall(r"<div\b", seg)), len(re.findall(r"</div>", seg))
    depth = 0
    valid = True
    for t in re.finditer(r"<div\b[^>]*>|</div>", seg):
        depth += -1 if t.group(0).startswith("</") else 1
        if depth < 0:
            valid = False
            break
    print(f"{before} -> {len(text)} bytes   div {o}/{c}   nesting valid: "
          f"{valid and depth == 0}")
    print(f"tiles: {len(re.findall(r'grid__item', seg.split(chr(34) + 'grid grid--products' + chr(34))[1][:9000]))}")
    for slug, name, href, desc, _ in TILES:
        print(f"  {name:22s} {href}")
    print("\nEclipse tiles removed: Metal Detection, Pipeline Filtration")
    print(f"old Eclipse tile images still referenced: "
          f"{len(re.findall(r'/site/assets/files/\d+/[^ ]*405x260', seg))}")


if __name__ == "__main__":
    main()
