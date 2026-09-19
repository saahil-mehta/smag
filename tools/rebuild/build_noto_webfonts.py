#!/usr/bin/env python3
"""Build self-hosted Noto Sans webfonts from the supplied variable TTFs.

Noto Sans ships as a two-axis variable font (wdth, wght). The site only uses
normal width, so wdth is pinned at 100 and the wght axis is kept whole, then
the result is subset to the latin and latin-ext ranges and written as woff2.
The full TTFs are ~2MB each; the subsets are a fraction of that.

Usage:
    build_noto_webfonts.py --src ~/Downloads/Noto_Sans [--dry-run]
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

REPO = Path("/Users/saahil/Documents/GitHub/smag")
OUT = REPO / "site/site/assets/fonts"

RANGES = {
    "latin": ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
              "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,"
              "U+2212,U+2215,U+FEFF,U+FFFD"),
    # Google's stock latin-ext also carries the phonetic extensions
    # (U+1D00-1DBF) and Latin Extended-D (U+A720-A7FF), which together are most
    # of its weight in Noto and are of no use to this site. Kept: the accented
    # Latin a European name or place needs, plus the currency and misc marks.
    "latin-ext": ("U+0100-024F,U+0259,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,"
                  "U+02DD-02FF,U+0304,U+0308,U+0329,U+1E00-1EFF,U+2020,"
                  "U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F"),
}

SOURCES = {
    "normal": "NotoSans-VariableFont_wdth,wght.ttf",
    "italic": "NotoSans-Italic-VariableFont_wdth,wght.ttf",
}

DRY = "--dry-run" in sys.argv
SRC = Path(sys.argv[sys.argv.index("--src") + 1]).expanduser() if "--src" in sys.argv else None


def build(ttf: Path, style: str, subset_name: str, unicodes: str) -> tuple[str, int]:
    font = TTFont(ttf)
    axes = {a.axisTag for a in font["fvar"].axes}
    if "wdth" in axes:
        font = instancer.instantiateVariableFont(font, {"wdth": 100})
        # Instancing leaves gvar lazily loaded and out of step with the glyph
        # order, which makes the subsetter raise KeyError on the first glyph it
        # cannot find there. A save/reload round trip settles every table.
        buf = io.BytesIO()
        font.save(buf)
        font.close()
        buf.seek(0)
        font = TTFont(buf)
    opts = subset.Options()
    opts.flavor = "woff2"
    # Noto ships heavily hinted; hinting is dead weight in a woff2 for screen
    # use and dominates the subset size. Keep the default layout features and
    # name records rather than "*", which drags in every optional table.
    opts.hinting = False
    opts.desubroutinize = False
    opts.notdef_outline = True
    opts.recalc_bounds = True
    s = subset.Subsetter(options=opts)
    s.populate(unicodes=subset.parse_unicodes(unicodes))
    s.subset(font)
    name = f"notosans{'-italic' if style == 'italic' else ''}-{subset_name}.woff2"
    out = OUT / name
    if not DRY:
        OUT.mkdir(parents=True, exist_ok=True)
        font.save(out)
        size = out.stat().st_size
    else:
        size = -1
    font.close()
    return name, size


def main() -> int:
    if SRC is None or not SRC.is_dir():
        raise SystemExit("pass --src <dir> containing the Noto Sans variable TTFs")
    built = []
    for style, fname in SOURCES.items():
        ttf = SRC / fname
        if not ttf.is_file():
            raise SystemExit(f"missing source font: {ttf}")
        for subset_name, unicodes in RANGES.items():
            # The site has two <em> elements in total; an accented character
            # inside one of them is not worth a third of a megabyte.
            if style == "italic" and subset_name == "latin-ext":
                continue
            name, size = build(ttf, style, subset_name, unicodes)
            built.append((name, size))
            print(f"  {name:34s} {size/1024:7.1f} KB" if size >= 0 else f"  {name} (dry run)")
    # The stylesheet is written here so the unicode ranges have one home.
    faces = []
    for name, _ in built:
        style = "italic" if "-italic-" in name else "normal"
        subset_name = "latin-ext" if name.endswith("-latin-ext.woff2") else "latin"
        faces.append(
            "@font-face {\n"
            "  font-family: 'Noto Sans';\n"
            f"  font-style: {style};\n"
            "  font-weight: 100 900;\n"
            "  font-display: swap;\n"
            f"  src: url(/site/assets/fonts/{name}) format('woff2');\n"
            f"  unicode-range: {RANGES[subset_name].replace(',', ', ')};\n"
            "}"
        )
    css = ("/* Noto Sans, self-hosted variable font, SIL Open Font License 1.1.\n"
           "   Width axis pinned to normal; the weight axis covers 100 to 900. */\n\n"
           + "\n".join(faces) + "\n")
    if not DRY:
        (OUT / "fonts.css").write_text(css, encoding="utf-8")

    total = sum(s for _, s in built if s > 0)
    print(f"{'would build' if DRY else 'built'} {len(built)} files"
          + (f", {total/1024:.1f} KB total" if total else "")
          + f"; {len(faces)} @font-face rules written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
