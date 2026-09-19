#!/usr/bin/env python3
"""Replace Font Awesome 5 Pro with masked RemixIcon glyphs.

The theme CSS opens with an 80KB Font Awesome Pro 5.8.1 block whose own
banner names the Commercial License, backed by 10MB of webfonts under
site/assets/fontawesome/. That is Eclipse's paid licence, and the whole of it
renders six glyphs: phone, envelope, store, search, whatsapp and google.

The six are replaced with RemixIcon (Apache 2.0), inlined as mask-image data
URIs against the existing class names, so no page markup changes. The element
itself becomes the icon, background-color:currentColor keeps `color` working
(the theme sets .locations__item .fas{color:#E20026}), and the em-based box
keeps fa-lg scaling.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path
from urllib.parse import quote

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
FA_DIR = SITE / "site/assets/fontawesome"
ICONS = Path(sys.argv[sys.argv.index("--icons") + 1]) if "--icons" in sys.argv else None

CUT_ANCHOR = "\n.lity{"
FA_BANNER = "Font Awesome Pro 5.8.1"

# site class -> RemixIcon svg file
MAP = {
    "fa-phone": "phone-fill.svg",
    "fa-envelope": "mail-fill.svg",
    "fa-store": "store-2-fill.svg",
    "fa-search": "search-line.svg",
    "fa-whatsapp": "whatsapp-fill.svg",
    "fa-google": "google-fill.svg",
}

BASE = (
    ".fa,.fas,.fab,.far,.fal{display:inline-block;width:1em;height:1em;"
    "background-color:currentColor;vertical-align:-.125em;"
    "-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;"
    "-webkit-mask-position:center;mask-position:center;"
    "-webkit-mask-size:contain;mask-size:contain}"
    ".fa-fw{width:1.25em}"
    ".fa-lg{font-size:1.33333em;line-height:.75em;vertical-align:-.0667em}"
    ".sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;"
    "overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}"
)

DRY = "--dry-run" in sys.argv


def data_uri(svg: str) -> str:
    svg = " ".join(svg.split())
    return "data:image/svg+xml," + quote(svg, safe="")


def main() -> int:
    if ICONS is None or not ICONS.is_dir():
        raise SystemExit("pass --icons <dir> holding the RemixIcon svg files")

    css = CSS.read_text(encoding="utf-8")
    if FA_BANNER not in css[:400]:
        raise SystemExit("theme css does not open with the Font Awesome banner")
    cut = css.find(CUT_ANCHOR)
    if cut == -1:
        raise SystemExit(f"cut anchor {CUT_ANCHOR!r} not found")

    rules = [BASE]
    for cls, fname in MAP.items():
        f = ICONS / fname
        if not f.is_file():
            raise SystemExit(f"missing icon svg: {f}")
        uri = data_uri(f.read_text(encoding="utf-8"))
        rules.append(
            f'.{cls}{{-webkit-mask-image:url("{uri}");mask-image:url("{uri}")}}'
        )

    new_css = css[cut + 1:] + "\n" + "".join(rules) + "\n"

    fa_bytes = sum(f.stat().st_size for f in FA_DIR.rglob("*") if f.is_file()) if FA_DIR.is_dir() else 0

    print(f"theme css {len(css):,} -> {len(new_css):,} bytes "
          f"({cut:,} of Font Awesome removed, {len(''.join(rules)):,} of RemixIcon added)")
    print(f"webfont directory to delete: {fa_bytes/1e6:.1f} MB, "
          f"{sum(1 for f in FA_DIR.rglob('*') if f.is_file()) if FA_DIR.is_dir() else 0} files")
    print(f"icons mapped: {', '.join(MAP)}")

    if not DRY:
        CSS.write_text(new_css, encoding="utf-8")
        if FA_DIR.is_dir():
            shutil.rmtree(FA_DIR)
        print("written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
