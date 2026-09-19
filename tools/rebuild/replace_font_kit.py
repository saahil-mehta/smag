#!/usr/bin/env python3
"""Replace Eclipse's Effra font kit with self-hosted Archivo.

Every page loaded https://use.typekit.net/ytg3zas.css, the identical Adobe
Fonts kit ID the Eclipse mirror uses, so the site was serving Effra under
Eclipse's licence. Archivo is SIL OFL 1.1 and is served from the site itself,
so no third-party font request is made at all.

Two edits:
1. The 66 pages swap the typekit <link> for /site/assets/fonts/fonts.css.
2. The theme CSS swaps the four "effra" family declarations for "Archivo".

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
FONTS = SITE / "site/assets/fonts/fonts.css"

OLD_LINK = "<link rel=stylesheet href=https://use.typekit.net/ytg3zas.css>"
NEW_LINK = "<link rel=stylesheet href=/site/assets/fonts/fonts.css>"
OLD_FAM = 'font-family:"effra",sans-serif'
NEW_FAM = 'font-family:"Archivo",sans-serif'

DRY = "--dry-run" in sys.argv


def main() -> int:
    if not FONTS.is_file():
        raise SystemExit(f"self-hosted font css missing: {FONTS}")

    pages = sorted(SITE.rglob("*.html"))
    missing = [p for p in pages if OLD_LINK not in p.read_text(encoding="utf-8")]
    if missing:
        raise SystemExit(
            f"{len(missing)} page(s) do not carry the expected typekit link, "
            f"first: {missing[0]}"
        )

    for p in pages:
        s = p.read_text(encoding="utf-8")
        if not DRY:
            p.write_text(s.replace(OLD_LINK, NEW_LINK), encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    n = css.count(OLD_FAM)
    if n == 0:
        raise SystemExit(f"no '{OLD_FAM}' declaration in {CSS.name}")
    if not DRY:
        CSS.write_text(css.replace(OLD_FAM, NEW_FAM), encoding="utf-8")

    print(f"{'would swap' if DRY else 'swapped'} the font link on {len(pages)} pages")
    print(f"{'would swap' if DRY else 'swapped'} {n} effra family declaration(s) in {CSS.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
