#!/usr/bin/env python3
"""Set the "Leaders In Magnetic Engineering" line under the header logo.

The line is HTML text inside the logo link, so it can be translated with the
rest of the copy, and it inherits the white link colour the theme already
gives the home header over the video.

The face is Noto Serif Italic, the serif partner of the site's Noto Sans,
pinned to weight 700 to match the supplied artwork and subset to Basic Latin.
Its @font-face sits with the tagline rule in the theme CSS appendix, because
build_noto_webfonts.py owns fonts.css and rewrites it whole.

Usage:
    add_logo_tagline.py --src NotoSerif-Italic[wdth,wght].ttf [--dry-run]
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
FONT_OUT = SITE / "site/assets/fonts/notoserif-bolditalic-basic.woff2"
TAGLINE = "Leaders In Magnetic Engineering"

OLD = ('<div class=logo><a href=/> <img src=/site/assets/images/logo.svg '
       'alt="Santosh Magnetic Works"> </a></div>')
NEW = ('<div class=logo><a href=/> <img src=/site/assets/images/logo.svg '
       f'alt="Santosh Magnetic Works"> <span class=logo__tagline>{TAGLINE}</span> </a></div>')

MARKER = "/* smag: logo tagline */"
RULES = (
    f"\n{MARKER}\n"
    "@font-face{font-family:'Noto Serif';font-style:italic;font-weight:700;font-display:swap;"
    "src:url(/site/assets/fonts/notoserif-bolditalic-basic.woff2) format('woff2');"
    "unicode-range:U+0020-007E}\n"
    "header .logo a{display:flex;flex-direction:column;align-items:flex-start}\n"
    # The 5px and 6px indents line the text up with the pill's visible left
    # edge; logo.svg has side padding, 19.5 of 560 viewBox units.
    ".logo__tagline{display:block;margin:5px 0 0 5px;text-indent:0;white-space:nowrap;"
    "font-family:'Noto Serif',Georgia,serif;font-style:italic;font-weight:700;"
    "font-size:11px;line-height:1.1;letter-spacing:0;color:#2a2a2a}\n"
    ".home header .logo__tagline{color:inherit;text-shadow:0 1px 3px rgba(0,0,0,.45)}\n"
    "@media (min-width:1024px){.logo__tagline{margin-left:6px;font-size:12px}}\n"
)

DRY = "--dry-run" in sys.argv
SRC = Path(sys.argv[sys.argv.index("--src") + 1]).expanduser() if "--src" in sys.argv else None


def build_font(src: Path) -> int:
    font = instancer.instantiateVariableFont(TTFont(src), {"wght": 700, "wdth": 100})
    # Same save/reload round trip as build_noto_webfonts.py: instancing leaves
    # tables out of step with the glyph order and the subsetter trips on it.
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    font = TTFont(buf)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.hinting = False
    opts.notdef_outline = True
    s = subset.Subsetter(options=opts)
    s.populate(unicodes=range(0x20, 0x7F))
    s.subset(font)
    if DRY:
        return -1
    font.save(FONT_OUT)
    return FONT_OUT.stat().st_size


def main() -> int:
    if SRC is None or not SRC.is_file():
        raise SystemExit("pass --src <NotoSerif-Italic variable TTF>")
    size = build_font(SRC)
    print(f"font {FONT_OUT.name}: " + (f"{size / 1024:.1f} KB" if size >= 0 else "dry run"))

    pages = done = 0
    for f in sorted(SITE.rglob("*.html")):
        s = f.read_text(encoding="utf-8")
        if "class=logo__tagline" in s:
            done += 1
            continue
        if s.count(OLD) != 1:
            continue
        pages += 1
        if not DRY:
            f.write_text(s.replace(OLD, NEW), encoding="utf-8")
    print(f"tagline added to {pages} pages ({done} already had it)")

    css = CSS.read_text(encoding="utf-8")
    if MARKER in css:
        print("css rules already present")
    else:
        print("css rules appended")
        if not DRY:
            CSS.write_text(css + RULES, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
