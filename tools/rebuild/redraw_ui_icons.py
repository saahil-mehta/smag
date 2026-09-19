#!/usr/bin/env python3
"""Redraw the seventeen UI icon SVGs that came from the Eclipse mirror.

They are Sketch exports, still carrying Eclipse's artboard UUIDs in their
<title> elements, and they are referenced from CSS background-image,
list-style-image and a handful of <img src>. The shapes themselves are
primitives: chevrons, long arrows, a triangle bullet, a tick and a play mark.

Each is redrawn from scratch at the same width, height, viewBox and colour, so
every existing reference keeps working and nothing shifts visually. Colours are
left as they are; the theme palette is a separate job.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
OUT = REPO / "site/site/assets/images/svg"
DRY = "--dry-run" in sys.argv

RED = "#E20026"
DEEP = "#CF2C31"
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY = "#9A9A9A"


def svg(w: str, h: str, vb: str, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="{vb}" fill="none">{body}</svg>\n')


def chevron(points: str, colour: str, sw: float) -> str:
    return (f'<polyline points="{points}" stroke="{colour}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def long_arrow(w: float, colour: str, sw: float, left: bool) -> str:
    y = w and 0
    return ""


ICONS: dict[str, str] = {}

# chevrons, 9x6, pointing down
for name, colour in (("icon-angle-black-down", BLACK), ("icon-angle-white-down", WHITE)):
    ICONS[name] = svg("9px", "6px", "0 0 9 6", chevron("1,1.4 4.5,4.6 8,1.4", colour, 1.6))

# same chevron, letterboxed in a wider box (the mirror used this for padding)
ICONS["icon-angle-black-down-padded"] = svg(
    "29px", "6px", "10 0 9 6", chevron("11,1.4 14.5,4.6 18,1.4", BLACK, 1.6))

# chevrons, 10x14, left and right
for name, colour, pts in (
    ("icon-angle-left", RED, "7,1.5 2.2,7 7,12.5"),
    ("icon-angle-right", RED, "3,1.5 7.8,7 3,12.5"),
    ("icon-angle-white-left", WHITE, "7,1.5 2.2,7 7,12.5"),
    ("icon-angle-white-right", WHITE, "3,1.5 7.8,7 3,12.5"),
):
    ICONS[name] = svg("10px", "14px", "0 0 10 14", chevron(pts, colour, 2))

# white chevron used on buttons, 8x14
ICONS["icon-button"] = svg("8px", "14px", "0 0 8 14",
                           chevron("2,1.5 6.2,7 2,12.5", WHITE, 2))

# long arrows, 42x24
for name, colour, flip in (("icon-arrow-right", RED, False), ("icon-arrow-left", RED, True)):
    if flip:
        shaft, head = 'M40 12H3', "6.5,6 1.5,12 6.5,18"
    else:
        shaft, head = 'M2 12H39', "35.5,6 40.5,12 35.5,18"
    ICONS[name] = svg("42px", "24px", "0 0 42 24",
                      f'<path d="{shaft}" stroke="{colour}" stroke-width="2" stroke-linecap="round"/>'
                      + chevron(head, colour, 2))

# short white long-arrow, 21x13
ICONS["icon-arrow-white-right"] = svg(
    "21px", "13px", "0 0 21 13",
    f'<path d="M1.5 6.5H18.5" stroke="{WHITE}" stroke-width="1.8" stroke-linecap="round"/>'
    + chevron("14.5,2 19,6.5 14.5,11", WHITE, 1.8))

# triangle list bullet, 5x7
ICONS["icon-bullet"] = svg("5px", "7px", "0 0 5 7",
                           f'<polygon points="0,0 5,3.5 0,7" fill="{RED}"/>')

# tick list bullet, 14x11
ICONS["icon-bullet-check"] = svg("14", "11", "0 0 14 11",
                                 chevron("1,5 5,9 13,1", DEEP, 2.5))

# small grey tick, 8x9
ICONS["icon-filter-checked"] = svg("8px", "9px", "0 0 8 9",
                                   chevron("0.9,4.6 3.1,6.9 7.1,1.9", GREY, 1.6))

# download arrow over a baseline, 15x19
for name, colour in (("icon-download-arrow", BLACK), ("icon-download-arrow-red", DEEP)):
    ICONS[name] = svg("15", "19", "0 0 15 19",
                      f'<path d="M7.5 1V14.6" stroke="{colour}" stroke-width="1.5" stroke-linecap="round"/>'
                      + chevron("2.8,10.2 7.5,15 12.2,10.2", colour, 1.5)
                      + f'<path d="M1 18H14" stroke="{colour}" stroke-width="1.5" stroke-linecap="round"/>')

# play triangle, 22x22
ICONS["icon-play"] = svg("22px", "22px", "0 0 22 22",
                         f'<polygon points="5,2.5 19,11 5,19.5" fill="{WHITE}"/>')


def main() -> int:
    existing = {f.stem for f in OUT.glob("icon-*.svg")}
    drawn = set(ICONS)
    if existing != drawn:
        raise SystemExit(
            f"icon set mismatch.\n  only on disk: {sorted(existing - drawn)}\n"
            f"  only in script: {sorted(drawn - existing)}")

    for name, content in sorted(ICONS.items()):
        f = OUT / f"{name}.svg"
        before = f.stat().st_size
        print(f"  {name+'.svg':36s} {before:6d} -> {len(content):4d} bytes")
        if not DRY:
            f.write_text(content, encoding="utf-8")
    print(f"{'would redraw' if DRY else 'redrew'} {len(ICONS)} icons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
