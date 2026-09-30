#!/usr/bin/env python3
"""Regenerate the SMAG gallery thumbnails that prepare_deploy.py deleted.

build_smag_product_pages.py writes each gallery thumbnail as an inline
background-image: url('/site/assets/images/smag/<stem>.thumb.jpg'). The
reference scan in prepare_deploy.py only matched unquoted url(/...), so every
one looked orphaned and was pruned before site/ was first committed, and the
thumbnail strips under the product galleries have been blank since.

prepare_deploy.py now matches quoted urls too. This rebuilds the missing
files from the brochure-stills masters with the builder's own recipe (fit
inside 160 x 120, pad white, no watermark), using its helpers so the output
matches what it would have written.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_smag_product_pages as b  # noqa: E402

DRY = "--dry-run" in sys.argv
TW, TH = 160, 120


def main() -> int:
    stems = set()
    for f in b.SITE.rglob("*.html"):
        for m in re.finditer(r"url\('" + re.escape(b.IMGURL) + r"/([^']+)\.thumb\.jpg'\)",
                             f.read_text(encoding="utf-8")):
            stems.add(m.group(1))
    todo = sorted(s for s in stems if not (b.IMGDIR / f"{s}.thumb.jpg").exists())
    print(f"  {len(stems)} thumbnails referenced, {len(todo)} missing")
    for stem in todo:
        src = b.prepared(stem)
        w, h = b.dims(src)
        scale = (["--resampleWidth", str(TW)] if w / h > TW / TH
                 else ["--resampleHeight", str(TH)])
        dst = b.IMGDIR / f"{stem}.thumb.jpg"
        print(f"  {dst.name}")
        if not DRY:
            b.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85", *scale,
                   "--padToHeightWidth", str(TH), str(TW), "--padColor", "FFFFFF",
                   str(src), "--out", str(dst)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
