#!/usr/bin/env python3
"""Rewrite the Eclipse footer lower bar across site/.

Three targeted changes, each by pattern rather than exact block, so all 436
pages are covered regardless of which regional lower-bar variant they carry:

  1. Copyright holder: Eclipse Magnetics -> Santosh Magnetic Works. The
     localised "All Rights Reserved" wording is left as found.
  2. Agency credit: Castus -> Saahil Mehta, linked to self@saahil.co.uk.
  3. Accreditation badges: BSI / Made in Britain / LWE are Eclipse's, so they
     go. Replaced with SMAG's own three, drawn in brand colours and matching
     the trust items in the content spec (ISO, Made in India, since 1978).

Policy links in the lower bar are deliberately untouched. They point at
Eclipse legal text that needs rewriting, not relinking, which is its own job.

Reversible: every page is otherwise byte-identical to reference-mirror/.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
IMG = SITE / "site/assets/images"

BADGES = [
    ("badge-made-in-india.webp", 140, 64, "Make in India"),
    ("badge-iso-9001.webp", 64, 64, "ISO 9001:2015 certified company"),
]

# 1. copyright holder
COPY_RE = re.compile(r"© 2026 Eclipse Magnetics,")
COPY_NEW = "© 2026 Santosh Magnetic Works,"

# 2. agency credit (the newline before "Castus" is in the source)
CASTUS_RE = re.compile(
    r"Castus, <a href=https://www\.castus\.co\.uk>Custom Software Agency</a>"
)
CASTUS_NEW = (
    'Developed by <a href="mailto:self@saahil.co.uk">Saahil Mehta</a>'
)

# 3. badge row (matches the empty cn variant too)
LOGOS_RE = re.compile(r"<div class=footer-logos>.*?</div>", re.DOTALL)


def logos_new() -> str:
    imgs = " ".join(
        f"<img src=/site/assets/images/{f} width={w} height={h} "
        f'style="max-width: {w}px; max-height: {h}px" alt="{alt}" '
        "loading=lazy decoding=async>"
        for f, w, h, alt in BADGES
    )
    return f"<div class=footer-logos>{imgs}</div>"


def main() -> None:
    for f, _, _, _ in BADGES:
        if not (IMG / f).exists():
            sys.exit(f"missing badge asset: {IMG / f}")

    counts = {"copyright": 0, "castus": 0, "badges": 0}
    files = 0

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (not utf-8): {page.relative_to(SITE)}")
            continue

        original = text
        text, n = COPY_RE.subn(COPY_NEW, text)
        counts["copyright"] += n
        text, n = CASTUS_RE.subn(CASTUS_NEW, text)
        counts["castus"] += n
        text, n = LOGOS_RE.subn(logos_new(), text)
        counts["badges"] += n

        if text != original:
            page.write_text(text, encoding="utf-8")
            files += 1

    print(f"{files} files rewritten\n")
    for k, v in counts.items():
        print(f"  {v:>4}  {k}")

    print("\nremaining site-wide:")
    for frag in (
        "castus",
        "Eclipse Magnetics, All Rights",
        "bsi-cropped",
        "made-in-britain",
        "lwe_logo",
        "lw_employer",
    ):
        hits = sum(
            p.read_text(encoding="utf-8", errors="replace").lower().count(frag.lower())
            for p in SITE.rglob("*.html")
        )
        print(f"  {hits:>5}  {frag}")


if __name__ == "__main__":
    main()
