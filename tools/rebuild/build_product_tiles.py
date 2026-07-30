#!/usr/bin/env python3
"""Watermark and size SMAG's six product-family tiles.

Sources are 2592x1664 (ratio 1.558, matching the 405x260 tile almost exactly),
so every output is a downscale. Nothing is upscaled.

The S-MAG mark is composited bottom-right at 18% opacity. The raster of the
logo SVG arrives with an opaque white background, so the outer white is removed
by edge flood fill; the letters inside the capsule are also white, and a global
white key would erase them.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

DL = Path.home() / "Downloads"
DEST = Path("/Users/saahil/Documents/GitHub/smag/site/site/assets/images/products")
LOGO_SVG_PNG = Path(
    "/private/tmp/claude-501/-Users-saahil-Documents-GitHub-smag/"
    "1a6d8a81-1486-437b-9c1f-664d93de7ded/scratchpad/wm/logo-clean.png"
)

WM_OPACITY = 0.18
WM_WIDTH_FRAC = 0.22
WIDTHS = [810, 405, 300, 200]          # 810 = 2x for retina

# family slug -> (source tag, alt text)
TILES = {
    "separators": ("qe8izk", "Magnetic separator with pull-out magnetic bars"),
    "filters": ("dj6fr3", "Skid-mounted magnetic filtration unit"),
    "lifters": ("71heap", "Permanent magnetic lifter holding a steel plate"),
    "chucks": ("7niljb", "Round permanent magnetic chuck"),
    "grills": ("tedzd9", "Hopper magnetic grill with magnetic tubes"),
    "tools": ("3gvcnq", "Magnetic V-block, tool rack and demagnetiser"),
}


def source_for(tag: str) -> Path:
    hits = sorted(DL.glob(f"Gemini_Generated_Image_{tag}*.jpg"))
    if not hits:
        raise SystemExit(f"no source for tag {tag}")
    return hits[0]


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    wm = Image.open(LOGO_SVG_PNG).convert("RGBA")

    for slug, (tag, alt) in TILES.items():
        src = source_for(tag)
        base = Image.open(src).convert("RGBA")
        W, H = base.size

        tw = int(W * WM_WIDTH_FRAC)
        th = round(tw * wm.height / wm.width)
        mark = wm.resize((tw, th), Image.LANCZOS)
        mark.putalpha(mark.split()[-1].point(lambda v: int(v * WM_OPACITY)))
        base.alpha_composite(
            mark, (W - tw - int(W * 0.035), H - th - int(H * 0.055))
        )
        flat = base.convert("RGB")

        for w in WIDTHS:
            h = round(w * 260 / 405)
            out = DEST / (f"{slug}.{w}.jpg" if w != 405 else f"{slug}.jpg")
            flat.resize((w, h), Image.LANCZOS).save(
                out, "JPEG", quality=87, optimize=True, progressive=True
            )
        sizes = ", ".join(
            f"{w}w {(DEST / (f'{slug}.{w}.jpg' if w != 405 else f'{slug}.jpg')).stat().st_size // 1024}KB"
            for w in WIDTHS
        )
        print(f"  {slug:12s} <- {src.name[23:29]}  {sizes}")

    total = sum(f.stat().st_size for f in DEST.glob("*.jpg")) // 1024
    print(f"\n  {len(list(DEST.glob('*.jpg')))} files, {total} KB total")


if __name__ == "__main__":
    main()
