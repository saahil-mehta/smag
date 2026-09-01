#!/usr/bin/env python3
"""Watermark every catalogue product photo with the S-MAG mark.

Same treatment as the home category tiles and the brochure-derived images:
the mark bottom-right at 18% opacity, 22% of the image width. Covers every
image referenced from a product gallery (slides, zoom targets and their
srcset renditions) and every tile image in a product family grid, across
the whole site. Editorial and industry stock photography is left unmarked;
branding scenery SMAG does not own would be wrong.

Files already marked are recorded in assets/source/watermarked.txt so the
sweep never double-stamps; images under /site/assets/images/smag/ and
/site/assets/images/products/ are marked at generation time and skipped
here. SVG and GIF files are skipped.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402
import build_smag_product_pages as build  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
MANIFEST = REPO / "assets/source/watermarked.txt"

RASTER = (".jpg", ".jpeg", ".png", ".webp")
SKIP_PREFIXES = ("/site/assets/images/smag/", "/site/assets/images/products/")

URL_RE = re.compile(r"/site/assets/[^\s\"'(),>]+")


def collect_targets() -> set[str]:
    urls: set[str] = set()
    for page in SITE.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        segments = []
        # product gallery blocks (slide image + zoom target + srcset)
        for m in re.finditer(r'<div class="product-image-wrapper[^"]*"[^>]*>',
                             text):
            end = find_element_end(text, m.start())
            zoom = re.search(r"data-zoom=([^\s>]+)", m.group(0))
            if zoom:
                urls.add(zoom.group(1).strip('"'))
            if end:
                segments.append(text[m.start():end])
        # product family grid tiles
        for m in re.finditer(r'<div class="grid grid--product-category">',
                             text):
            end = find_element_end(text, m.start())
            if end:
                segments.append(text[m.start():end])
        for seg in segments:
            urls.update(URL_RE.findall(seg))
    return {
        u for u in urls
        if u.lower().endswith(RASTER) and not u.startswith(SKIP_PREFIXES)
    }


def stamp(path: Path) -> None:
    from PIL import Image
    wm = build.logo_mark()
    im = Image.open(path)
    fmt = im.format  # preserve on save
    base = im.convert("RGBA")
    W, H = base.size
    tw = int(W * build.WM_WIDTH_FRAC)
    th = round(tw * wm.height / wm.width)
    if tw < 24:
        return  # too small for a legible mark
    mark = wm.resize((tw, th), Image.LANCZOS)
    mark.putalpha(mark.split()[-1].point(
        lambda v: int(v * build.WM_OPACITY)))
    base.alpha_composite(mark, (W - tw - int(W * 0.035),
                                H - th - int(H * 0.055)))
    if fmt == "PNG":
        base.save(path, "PNG", optimize=True)
    elif fmt == "WEBP":
        base.convert("RGB").save(path, "WEBP", quality=87)
    else:
        base.convert("RGB").save(path, "JPEG", quality=87, optimize=True,
                                 progressive=True)


def main() -> None:
    dry = "--dry-run" in sys.argv
    done = set()
    if MANIFEST.exists():
        done = set(MANIFEST.read_text(encoding="utf-8").split())

    targets = collect_targets()
    stamped = missing = skipped = 0
    for url in sorted(targets):
        if url in done:
            skipped += 1
            continue
        f = SITE / url.lstrip("/")
        if not f.exists():
            missing += 1
            continue
        if not dry:
            stamp(f)
            done.add(url)
        stamped += 1
    if not dry:
        MANIFEST.write_text("\n".join(sorted(done)) + "\n", encoding="utf-8")
    print(f"targets {len(targets)}, stamped {stamped}, "
          f"already done {skipped}, missing {missing}")


if __name__ == "__main__":
    main()
