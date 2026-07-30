#!/usr/bin/env python3
"""Prepare the two supplied badge images for the site footer.

ISO roundel: already RGBA with transparency. Trim the transparent margin and
downscale.

Make in India: RGB, opaque, pure white background. A global white-to-alpha
key would also erase the white "MAKE IN INDIA" lettering inside the lion, so
the background is removed by flood fill from the image edges instead, which
only reaches the contiguous outer white.

Both are then trimmed to their content and resized to 192px tall, 3x the 64px
footer display height, so they stay sharp on retina and when the footer's
mobile rule halves them.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw

SRC = Path.home() / "Downloads"
DEST = Path("/Users/saahil/Documents/GitHub/smag/site/site/assets/images")

ISO_SRC = SRC / "what-is-iso-9001-compliance.png.webp"
MII_SRC = SRC / "thequint-2016-01-5fe4b302-c270-4b8a-8c02-db7cf3ef93ed-Make-in-India.jpg.webp"

TARGET_H = 192  # 3x the 64px footer slot
TOLERANCE = 18  # how close to white still counts as background


def drop_outer_white(im: Image.Image, tol: int = TOLERANCE) -> Image.Image:
    """Make the contiguous white region touching the border transparent."""
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()

    def is_bg(xy):
        r, g, b, _ = px[xy]
        return r >= 255 - tol and g >= 255 - tol and b >= 255 - tol

    # Iterative flood fill from every border pixel that looks like background.
    seen = bytearray(w * h)
    stack = []
    for x in range(w):
        for y in (0, h - 1):
            if is_bg((x, y)):
                stack.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg((x, y)):
                stack.append((x, y))

    while stack:
        x, y = stack.pop()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        px[x, y] = (255, 255, 255, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and is_bg((nx, ny)):
                stack.append((nx, ny))

    return im


def finish(im: Image.Image, out: Path, label: str) -> None:
    box = im.getbbox()
    if box:
        im = im.crop(box)
    w, h = im.size
    new_w = max(1, round(w * TARGET_H / h))
    im = im.resize((new_w, TARGET_H), Image.LANCZOS)
    im.save(out, "WEBP", lossless=True, quality=100, method=6)
    disp_h = TARGET_H // 3
    disp_w = round(new_w / 3)
    print(
        f"{label}\n"
        f"  -> {out.name}  {im.size[0]}x{im.size[1]}  "
        f"{out.stat().st_size / 1024:.1f} KB\n"
        f"     footer display: {disp_w}x{disp_h}  (ratio {new_w / TARGET_H:.3f})"
    )
    return disp_w, disp_h


def main() -> None:
    for p in (ISO_SRC, MII_SRC):
        if not p.exists():
            sys.exit(f"missing source: {p}")
    DEST.mkdir(parents=True, exist_ok=True)

    iso = Image.open(ISO_SRC).convert("RGBA")
    print(f"ISO source: {iso.size} {iso.mode}")
    a = finish(iso, DEST / "badge-iso-9001.webp", "ISO 9001:2015 roundel")

    mii = Image.open(MII_SRC)
    print(f"\nMake in India source: {mii.size} {mii.mode}")
    mii = drop_outer_white(mii)
    alpha = mii.split()[-1]
    cleared = sum(1 for v in alpha.getdata() if v == 0)
    total = mii.size[0] * mii.size[1]
    print(f"  background cleared: {cleared}/{total} px ({100 * cleared / total:.1f}%)")
    b = finish(mii, DEST / "badge-made-in-india.webp", "Make in India lion")

    print(f"\nfooter sizes -> iso {a}, mii {b}")


if __name__ == "__main__":
    main()
