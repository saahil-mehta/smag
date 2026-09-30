#!/usr/bin/env python3
"""Place an animated line drawing of the working cycle on product pages.

Each drawing in assets/source/animations/ is an SVG in the guide diagram
style whose parts carry `an-*` classes; smag.css moves them on one shared
loop and javascript.js pauses a drawing while it is off screen, or when the
reader presses Pause. The numbered steps sit above the drawing as an HTML
list on the same loop, so they stay readable on a phone, a screen reader
hears every step, and they translate with the rest of the copy.

The figure goes straight after the Overview heading. Re-running replaces
it, so the page follows the source. Run after rewrite_copy.py.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site/products"
SRC = REPO / "assets/source/animations"
DRY = "--dry-run" in sys.argv

SEP = "magnetic-separation-and-metal-detection"
PAGES = [
    (f"{SEP}/easy-clean-magnetic-grid-separator", "easy-clean-grid",
     "Cleaning an easy clean grid. The cores slide out of the tubes and the iron falls off."),
    ("lifting-and-handling/permanent-magnetic-lifter", "lifter",
     "A Maxx lifter at work. One turn of the handle holds the load, and turning it back releases it."),
    ("magnetic-tools-and-standard-magnets/magnetic-sweeper", "sweeper",
     "The sweeper picks up nails and swarf as it rolls, and drops them in a bin when the lever is pulled."),
    (f"{SEP}/high-intensity-liquid-filter-separator", "liquid-filter",
     "Iron in the liquid holds to the rods. To clean, lift the rod cluster out and wipe it."),
    ("filtration-systems/magnetic-coolant-filter", "liquid-filter",
     "Iron in the coolant holds to the rods. To clean, lift the rods out, wipe them and refit them."),
]
STEPS = {
    "easy-clean-grid": ("ec", ["Iron holds to the tubes", "Draw out the cores",
                               "The iron falls off", "Refit the cores"]),
    "lifter": ("lf", ["Set the lifter on the load", "Turn the handle on",
                      "Lift and set down", "Turn it back to release"]),
    "sweeper": ("sw", ["Push it over the floor", "Hold it over a bin",
                       "Pull the lever and the load drops off"]),
    "liquid-filter": ("lt", ["Iron holds to the rods", "Lift the rods out",
                             "Wipe them clean", "Refit and run"]),
}
OLD = re.compile(r'<figure class="guide-figure guide-figure--diagram product-anim".*?</figure>', re.S)


def figure(name: str, caption: str) -> str:
    svg = (SRC / f"{name}.svg").read_text(encoding="utf-8").strip()
    svg = re.sub(r"<svg\b", f'<svg role=img aria-label="{html.escape(caption, quote=True)}"', svg, count=1)
    key, steps = STEPS[name]
    items = "".join(
        f'<li class="an an-{key}-s{i}" style="--k:{i - 1}">'
        f"<span class=product-anim__n>{i}</span>{html.escape(t)}</li>"
        for i, t in enumerate(steps, 1))
    ticks = "<i></i>" * len(steps)
    head = (f"<div class=product-anim__head><ol class=product-anim__steps>{items}</ol>"
            f"<div class=product-anim__ticks aria-hidden=true>{ticks}</div></div>")
    return ('<figure class="guide-figure guide-figure--diagram product-anim">' + head + svg +
            f"<figcaption>{html.escape(caption)}"
            '<button class=product-anim__toggle type=button data-play=Play data-pause=Pause>Pause</button>'
            "</figcaption></figure>")


def main() -> int:
    for rel, name, caption in PAGES:
        page = SITE / rel / "index.html"
        s = OLD.sub("", page.read_text(encoding="utf-8"))
        at = s.find("id=overview")
        end = s.find("</h2>", at)
        if at < 0 or end < 0:
            raise SystemExit(f"no overview heading on {page}")
        end += len("</h2>")
        s = s[:end] + figure(name, caption) + s[end:]
        print(f"  {rel:60s} {name}")
        if not DRY:
            page.write_text(s, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
