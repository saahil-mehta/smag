#!/usr/bin/env python3
"""Write SMAG images over the Eclipse images the site still serves.

Each Eclipse asset is served as several renditions (different sizes and
crops) under site/site/assets/files/. Writing the replacement over every
rendition, cropped to that rendition's own size, changes no HTML, so all
eight languages pick it up at once.

    replace_eclipse_images.py <asset dir id> <master image> [--watermark] [--contain] [--focus X,Y]

<asset dir id> is the numbered folder under site/site/assets/files/, which
holds one asset's renditions (35880 for the oil and gas tile).
--watermark adds the S-MAG mark (product photos, like every catalogue image).
--contain fits a product photo inside each rendition on white; the default
crops to fill, for scenes. --focus keeps the crop centred on that fraction of
the master (0.5,0.5 is the centre).

Masters and their provenance are listed in assets/source/generated-image-prompts.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_smag_product_pages as build  # noqa: E402

FILES = Path("/Users/saahil/Documents/GitHub/smag/site/site/assets/files")
IMAGE = (".jpg", ".jpeg", ".png", ".webp")


def cover(im: Image.Image, w: int, h: int, fx: float, fy: float) -> Image.Image:
    scale = max(w / im.width, h / im.height)
    rw, rh = round(im.width * scale), round(im.height * scale)
    im = im.resize((rw, rh), Image.LANCZOS)
    x = min(max(round(rw * fx - w / 2), 0), rw - w)
    y = min(max(round(rh * fy - h / 2), 0), rh - h)
    return im.crop((x, y, x + w, y + h))


def contain(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.copy()
    im.thumbnail((round(w * 0.92), round(h * 0.92)), Image.LANCZOS)
    canvas = Image.new("RGB", (w, h), "white")
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    focus = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--focus"), "0.5,0.5")
    args = [a for a in args if a != focus]
    folder, master = FILES / args[0], Image.open(args[1]).convert("RGB")
    fx, fy = (float(v) for v in focus.split(","))
    targets = [p for p in sorted(folder.iterdir()) if p.suffix.lower() in IMAGE]
    if not targets:
        raise SystemExit(f"no images in {folder}")
    for p in targets:
        w, h = Image.open(p).size
        out = contain(master, w, h) if "--contain" in sys.argv else cover(master, w, h, fx, fy)
        if p.suffix.lower() == ".png":
            out.save(p, optimize=True)
        elif p.suffix.lower() == ".webp":
            out.save(p, quality=82)
        else:
            out.save(p, quality=84, optimize=True, progressive=True)
        if "--watermark" in sys.argv:
            build.watermark(p)  # writes JPEG bytes whatever the extension
            if p.suffix.lower() != ".jpg" and p.suffix.lower() != ".jpeg":
                Image.open(p).save(p, format=p.suffix.lstrip(".").upper().replace("JPG", "JPEG"))
        print(f"{p.relative_to(FILES)} {w}x{h}")


if __name__ == "__main__":
    main()
