#!/usr/bin/env python3
"""Remove the three <source> elements that point at files which never existed.

The About, Contact and Home banners each carry a <picture> with a <source>
naming a rendition that has never been in the repo at any commit:

    company/about-us   about-banner.jpg        (min-width: 768px)  desktop
    contact-us         contact-banner.jpg      (min-width: 768px)  desktop
    index              home-banner-mobile.jpg  no media            mobile

A <source> that matches wins the negotiation, so the browser requests the
missing file, gets a 404 and renders a broken image. It does not fall back to
the <img>. Each page therefore had a broken banner at one breakpoint.

Dropping the dead <source> lets the working image serve every width, which
object-fit:cover already crops to the band. object-position is set on the two
that need it so the crop keeps the subject in frame.

A scrim is also added behind banner headings, because white text sits directly
on a photograph on these pages and only the home banner had one.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
DRY = "--dry-run" in sys.argv

# page -> (dead source element, optional (img anchor, replacement with object-position))
FIXES = {
    "company/about-us/index.html": (
        '<source srcset=/site/assets/images/about-banner.jpg media="(min-width: 768px)" width=1280 height=360>\n',
        ('<img src=/site/assets/images/about-banner-mobile.jpg width=640 height=834 alt=',
         '<img style="object-position:50% 15%" src=/site/assets/images/about-banner-mobile.jpg width=640 height=834 alt='),
    ),
    "contact-us/index.html": (
        '<source srcset=/site/assets/images/contact-banner.jpg media="(min-width: 768px)" width=1280 height=360>\n',
        ('<img src=/site/assets/images/contact-banner-mobile.jpg width=640 height=834 alt=',
         '<img style="object-position:50% 24%" src=/site/assets/images/contact-banner-mobile.jpg width=640 height=834 alt='),
    ),
    "index.html": (
        '<source srcset=/site/assets/images/home-banner-mobile.jpg width=700 height=912>\n',
        None,
    ),
}

# white headings sit straight on a photo here; only .home had a scrim
SCRIM = (".banner__text{position:relative;z-index:3}"
         ".banner:not(.home-banner)::after{content:\"\";position:absolute;inset:0;"
         "z-index:2;pointer-events:none;"
         "background:linear-gradient(90deg,rgba(14,17,20,.55) 0%,rgba(14,17,20,.25) 45%,rgba(14,17,20,0) 75%)}")


def main() -> int:
    for rel, (dead, img_swap) in FIXES.items():
        p = SITE / rel
        s = p.read_text(encoding="utf-8")
        if dead not in s:
            raise SystemExit(f"dead <source> not found in {rel}")
        s = s.replace(dead, "", 1)
        if img_swap:
            old, new = img_swap
            if old not in s:
                raise SystemExit(f"img anchor not found in {rel}")
            s = s.replace(old, new, 1)
        print(f"  {rel}: dropped dead <source>" + (" and set object-position" if img_swap else ""))
        if not DRY:
            p.write_text(s, encoding="utf-8")

    css = CSS.read_text(encoding="utf-8")
    if "banner:not(.home-banner)::after" in css:
        print("  scrim already present")
    else:
        print("  added a scrim behind banner headings")
        if not DRY:
            CSS.write_text(css + "\n" + SCRIM + "\n", encoding="utf-8")

    print(f"{'would fix' if DRY else 'fixed'} {len(FIXES)} banners")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
