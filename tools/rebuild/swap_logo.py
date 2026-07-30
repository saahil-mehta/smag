#!/usr/bin/env python3
"""Swap the Eclipse brand logo for the SMAG mark across site/.

Two steps:
  1. Overwrite the shared SVG at site/assets/images/logo.svg with the SMAG
     mark. All 436 pages reference this one path, so the image changes
     everywhere at once with no HTML edits.
  2. Rewrite the <img> tags: replace Eclipse alt text with "Santosh
     Magnetic Works", and correct the footer's hardcoded height=36
     (built for Eclipse's 3.41:1 mark) to 40 for SMAG's 3.11:1 mark.

Reversible: every file here is byte-identical to reference-mirror/, so
any page can be restored with a copy from there.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
SMAG_SVG = SITE / "smag-logo.svg"
TARGET_SVG = SITE / "site/assets/images/logo.svg"

ALT = "Santosh Magnetic Works"

# Exact tag replacements. Ordered longest-first so the footer variant
# (which also carries width/height) is matched before the bare one.
REPLACEMENTS = [
    (
        "<img src=/site/assets/images/logo.svg width=124 height=36 alt=\"Eclipse Magnetics\">",
        f"<img src=/site/assets/images/logo.svg width=124 height=40 alt=\"{ALT}\">",
    ),
    (
        "<img src=/site/assets/images/logo.svg alt=\"Eclipse Magnetics North America\">",
        f"<img src=/site/assets/images/logo.svg alt=\"{ALT}\">",
    ),
    (
        "<img src=/site/assets/images/logo.svg alt=\"Eclipse Magnetics\">",
        f"<img src=/site/assets/images/logo.svg alt=\"{ALT}\">",
    ),
    (
        "<img src=/site/assets/images/logo.svg alt=磁性过滤器-易克磁性技术>",
        f"<img src=/site/assets/images/logo.svg alt=\"{ALT}\">",
    ),
]


def swap_svg() -> None:
    if not SMAG_SVG.exists():
        sys.exit(f"missing SMAG logo at {SMAG_SVG}")
    if not TARGET_SVG.exists():
        sys.exit(f"missing target logo at {TARGET_SVG}")
    shutil.copyfile(SMAG_SVG, TARGET_SVG)
    print(f"svg: {TARGET_SVG.relative_to(SITE)} <- smag-logo.svg "
          f"({TARGET_SVG.stat().st_size} bytes)")


def rewrite_tags() -> None:
    counts = {old: 0 for old, _ in REPLACEMENTS}
    files_changed = 0

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (not utf-8): {page.relative_to(SITE)}")
            continue

        original = text
        for old, new in REPLACEMENTS:
            n = text.count(old)
            if n:
                text = text.replace(old, new)
                counts[old] += n

        if text != original:
            page.write_text(text, encoding="utf-8")
            files_changed += 1

    print(f"\nhtml: {files_changed} files rewritten")
    for old, n in counts.items():
        label = old[:62].rsplit("alt=", 1)[-1] or old[:40]
        print(f"  {n:>4}  alt={label}")
    print(f"  {sum(counts.values()):>4}  total tags")


if __name__ == "__main__":
    swap_svg()
    rewrite_tags()
