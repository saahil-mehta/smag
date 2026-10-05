#!/usr/bin/env python3
"""Footer logo gets the header lockup: the S-MAG mark with its tagline.

Client request of 5 Oct 2026. The footer image becomes the same `.logo`
link the header uses (mark over "Leaders In Magnetic Engineering"), so the
existing `.logo__tagline` rule sizes it from `--logo-w`; smag.css sets the
footer width. The tagline text is the header's, so its translations carry
over unchanged.
"""
from __future__ import annotations

from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
LANGS = {"hi", "mr", "gu", "kn", "te", "ml", "ta"}

OLD = '<div><img src=/site/assets/images/logo.svg width=124 height=40 alt="Santosh Magnetic Works"><p class=address>'
NEW = (
    '<div><div class="logo footer-logo"><a href=/><img src=/site/assets/images/logo.svg '
    'width=124 height=40 alt="Santosh Magnetic Works"> '
    '<span class=logo__tagline>Leaders In Magnetic Engineering</span></a></div><p class=address>'
)


def main() -> None:
    pages = [p for p in sorted(SITE.rglob("*.html"))
             if p.relative_to(SITE).parts[0] not in LANGS]
    done, missed = 0, []
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if "<footer" not in text:
            continue
        if text.count(OLD) != 1:
            missed.append(page.relative_to(SITE))
            continue
        page.write_text(text.replace(OLD, NEW), encoding="utf-8")
        done += 1
    print(f"{done} footers given the tagline")
    if missed:
        raise SystemExit(f"footer logo not found once on: {missed[:5]}")


if __name__ == "__main__":
    main()
