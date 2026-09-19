#!/usr/bin/env python3
"""Install the replacement photography supplied in ~/Downloads.

Four images, all of them Saahil's own:

  modular-pipeline-filter_new           the pipeline filter reshot without the
                                        ULTRAFILTREX placard or Eclipse roundel
  coolant-filter-group_new              the filter pair without the Filtramag
                                        printing; wants the S-MAG mark added
  Gemini_Generated_Image_akdm73...      About Us team photo, enlarged
  Gemini_Generated_Image_5c61xk...      Contact Us team photo, enlarged

Each product image is written into every rendition the site references, fitted
to the box its filename encodes so the dimensions match what the pages already
declare. The S-MAG mark is applied per rendition at the catalogue's own
settings (22% of width, 18% opacity, bottom right), matching
watermark_catalogue_images.py, and only where asked.

The banners replace their file and the <picture> width/height attributes are
updated to the new intrinsic size so the aspect-ratio hint stays honest.

Masters are copied into assets/source/supplied/ so provenance is tracked.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_smag_product_pages as build  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
DL = Path.home() / "Downloads"
MASTERS = REPO / "assets/source/supplied"
MANIFEST = REPO / "assets/source/watermarked.txt"
DRY = "--dry-run" in sys.argv

ECL = DL / "smag-eclipse-images/01-branding-in-photo"
BAN = DL / "smag-banners/upscaled"

# product image -> (source, watermark?, [(target, box_w, box_h)])
PRODUCTS = {
    "modular-pipeline-filter": (
        ECL / "modular-pipeline-filter_new.jpeg", False,
        [("site/assets/files/35852/modular-pipeline-filter.637x481.jpg", 637, 481),
         ("site/assets/files/35926/modular-pipeline-filter.355x205.jpg", 355, 205),
         ("site/assets/files/35926/modular-pipeline-filter.355x205.200x0.jpg", 200, 10000)],
    ),
    "coolant-filter-group": (
        ECL / "coolant-filter-group_new_TO_ADD_WATERMARK-SMAG.jpeg", True,
        [("site/assets/files/6812/coolant-filter-group.355x205.jpg", 355, 205)],
    ),
}

# banner -> (source, site file, pages that declare its size)
BANNERS = {
    "about-banner-mobile": (
        BAN / "Gemini_Generated_Image_akdm73akdm73akdm.jpeg",
        "site/assets/images/about-banner-mobile.jpg",
        ["company/about-us/index.html"],
    ),
    "contact-banner-mobile": (
        BAN / "Gemini_Generated_Image_5c61xk5c61xk5c61.jpeg",
        "site/assets/images/contact-banner-mobile.jpg",
        ["contact-us/index.html"],
    ),
}


def fit(im: Image.Image, bw: int, bh: int) -> Image.Image:
    scale = min(bw / im.width, bh / im.height)
    return im.resize((max(1, round(im.width * scale)),
                      max(1, round(im.height * scale))), Image.LANCZOS)


def stamp(im: Image.Image) -> Image.Image:
    wm = build.logo_mark()
    base = im.convert("RGBA")
    W, H = base.size
    tw = int(W * build.WM_WIDTH_FRAC)
    if tw < 24:
        return base
    th = round(tw * wm.height / wm.width)
    mark = wm.resize((tw, th), Image.LANCZOS)
    mark.putalpha(mark.split()[-1].point(lambda v: int(v * build.WM_OPACITY)))
    base.alpha_composite(mark, (W - tw - int(W * 0.035), H - th - int(H * 0.055)))
    return base


def save(im: Image.Image, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.suffix.lower() == ".png":
        im.save(dest, "PNG", optimize=True)
    else:
        im.convert("RGB").save(dest, "JPEG", quality=88, optimize=True,
                               progressive=True)


def main() -> int:
    for src, *_ in [(v[0],) for v in PRODUCTS.values()] + [(v[0],) for v in BANNERS.values()]:
        if not src.is_file():
            raise SystemExit(f"missing supplied image: {src}")

    if not DRY:
        MASTERS.mkdir(parents=True, exist_ok=True)

    marked: list[str] = []
    for name, (src, want_mark, targets) in PRODUCTS.items():
        master = Image.open(src).convert("RGB")
        print(f"{name}: {src.name} {master.size[0]}x{master.size[1]}"
              + (" (+ S-MAG mark)" if want_mark else ""))
        if not DRY:
            shutil.copy2(src, MASTERS / f"{name}{src.suffix}")
        for rel, bw, bh in targets:
            out = SITE / rel
            im = fit(master, bw, bh)
            if want_mark:
                im = stamp(im)
                marked.append("/" + rel)
            print(f"    {im.size[0]:>4}x{im.size[1]:<4}  {rel}")
            if not DRY:
                save(im, out)

    for name, (src, rel, pages) in BANNERS.items():
        master = Image.open(src).convert("RGB")
        out = SITE / rel
        with Image.open(out) as cur:
            old = cur.size
        print(f"{name}: {old[0]}x{old[1]} -> {master.size[0]}x{master.size[1]}")
        if not DRY:
            shutil.copy2(src, MASTERS / f"{name}{src.suffix}")
            save(master, out)
        for page in pages:
            p = SITE / page
            s = p.read_text(encoding="utf-8")
            old_attr = f"width={old[0]} height={old[1]}"
            if old_attr not in s:
                raise SystemExit(f"size attributes {old_attr!r} not found in {page}")
            n = s.count(old_attr)
            s = s.replace(old_attr, f"width={master.size[0]} height={master.size[1]}")
            print(f"    {page}: updated {n} size attribute pair(s)")
            if not DRY:
                p.write_text(s, encoding="utf-8")

    if marked:
        done = set(MANIFEST.read_text(encoding="utf-8").split()) if MANIFEST.exists() else set()
        added = [u for u in marked if u not in done]
        print(f"watermark manifest: {len(added)} new entr(ies)")
        if not DRY and added:
            MANIFEST.write_text("\n".join(sorted(done | set(marked))) + "\n",
                                encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
