#!/usr/bin/env python3
"""Convert the three Font Awesome pseudo-element icons to masked RemixIcon.

replace_font_awesome.py handles the icons that appear as <i> elements in the
markup. Three more are drawn by the theme's own CSS through ::after content
and private-use codepoints, so they survive that pass and would render as
tofu once the webfonts are gone:

    header .burger::after                 \\f0c9  bars    -> menu-line
    body.mobile-menu-active .burger::after \\f00d  times   -> close-line
    .checkbox-label.checked::after        \\f00c  check   -> check-line

Each keeps its own positioning and colour; only the glyph delivery changes,
from a font codepoint to a mask-image. content is set to "" so the box still
generates. Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote

REPO = Path("/Users/saahil/Documents/GitHub/smag")
CSS = REPO / "site/site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
ICONS = Path(sys.argv[sys.argv.index("--icons") + 1]) if "--icons" in sys.argv else None
DRY = "--dry-run" in sys.argv

# selector -> (icon file, box size in the rule's own units)
RULES = {
    "header .burger::after": ("menu-line.svg", "26.2px"),
    "body.mobile-menu-active .burger::after": ("close-line.svg", "26.2px"),
    ".checkbox-label.checked::after": ("check-line.svg", "12px"),
}

MASK = ("display:inline-block;background-color:currentColor;"
        "-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;"
        "-webkit-mask-position:center;mask-position:center;"
        "-webkit-mask-size:contain;mask-size:contain")


def data_uri(svg: str) -> str:
    return "data:image/svg+xml," + quote(" ".join(svg.split()), safe="")


def main() -> int:
    if ICONS is None or not ICONS.is_dir():
        raise SystemExit("pass --icons <dir> holding the RemixIcon svg files")

    css = CSS.read_text(encoding="utf-8")
    changed = 0

    for sel, (fname, size) in RULES.items():
        f = ICONS / fname
        if not f.is_file():
            raise SystemExit(f"missing icon svg: {f}")
        i = css.find(sel + "{")
        if i == -1:
            raise SystemExit(f"selector not found: {sel}")
        end = css.find("}", i)
        if end == -1:
            raise SystemExit(f"unterminated rule for: {sel}")
        body = css[i + len(sel) + 1:end]

        # keep everything that is not font/glyph delivery
        keep = [d for d in body.split(";")
                if d and not re.match(
                    r"\s*(content|font-family|font-weight|font-style|font-variant|"
                    r"font-size|text-rendering|-webkit-font-smoothing|display)\s*:", d)]
        uri = data_uri(f.read_text(encoding="utf-8"))
        new_body = (f'content:"";{MASK};width:{size};height:{size};'
                    f'-webkit-mask-image:url("{uri}");mask-image:url("{uri}")'
                    + ("".join(";" + d for d in keep)))
        css = css[:i + len(sel) + 1] + new_body + css[end:]
        changed += 1
        print(f"  {sel}  ->  {fname} at {size}")

    if not DRY:
        CSS.write_text(css, encoding="utf-8")
    print(f"{'would rewrite' if DRY else 'rewrote'} {changed} rule(s); css now {len(css):,} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
