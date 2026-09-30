#!/usr/bin/env python3
"""UX polish pass, 30 Sep 2026. Refinement of the incumbent design only.

- Logo lockup: the tagline is set to the red pill's exact width and centred
  under it. At the old logo size that needed 9.6px type, so the logo grows
  (140 to 172px on phones, 174 to 208px on desktop) and the tagline is 9.5px
  and 11.5px. The tagline runs 16.81 x its font size wide; the pill is
  521/560 of the logo's width.
- Header contact: the site exists to get a call or a WhatsApp message, and the
  header offered neither. It gains a phone link and a WhatsApp button; below
  1280px they collapse to two 40px icon buttons beside the menu.
- The mobile menu and the collapsed nav were pinned at top:80px, the header's
  height before the tagline. They now sit at var(--hdr), which javascript.js
  sets from the real header height; the values here are fallbacks.
- The footer kept margins (183px phones, 66px desktop) reserved for the sticky
  call-to-action bar removed on 2 Sep, which showed as a blank band under it.
- Keyboard: a skip link, the Products dropdown opens on focus-within (Tab used
  to walk into its invisible links), and one brand focus ring site-wide.
- Browser surfaces: text selection and link underline offset in the palette.
- Contrast: the theme's #848484 grey on the footer, breadcrumb separators, zoom
  tip and form notes measured 3.4:1; now about 5.5:1. The legal line in the
  footer grows from 11px to about 12.6px.
- Gallery zoom tip sat under the image layer and was half hidden.
- Home stats: an inline three-column grid squeezed them on phones; they stack
  below 768px now.
- Contact: form labels read "Where are you based?*:"; the asterisk is now a
  red " *" and optional labels drop the trailing colon. On phones the works details (call, WhatsApp) come before the form
  and the address no longer squeezes into a half-width column.
- Client logos: blank margins trimmed from four files, and every logo sized to
  the same visual area, so 7:1 wordmarks stop shrinking to 25px tall.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
CLIENTS = SITE / "site/assets/images/clients"
DRY = "--dry-run" in sys.argv

PHONE_TEL, PHONE_TEXT = "+919920143922", "+91 99201 43922"
WA = "https://wa.me/919920143922"

OTHER_NAV_OLD = "<nav class=other-nav><a href=# class=burger> <span></span> </a></nav>"
OTHER_NAV_NEW = (
    "<nav class=other-nav><div class=header-contact>"
    f'<a class=hc-call href="tel:{PHONE_TEL}" aria-label="Call {PHONE_TEXT}">'
    f'<i class="fas fa-phone" aria-hidden=true></i><span>{PHONE_TEXT}</span></a>'
    f'<a class=hc-wa href={WA} target=_blank rel="noopener noreferrer" aria-label="Message us on WhatsApp">'
    '<i class="fab fa-whatsapp" aria-hidden=true></i><span>WhatsApp</span></a>'
    "</div><a href=# class=burger aria-label=Menu> <span></span> </a></nav>"
)
STATS_OLD = '<div class=row__inner style="grid-template-columns:repeat(3,minmax(0,1fr))">'
STATS_NEW = "<div class=\"row__inner statistics__three\">"

# Earlier tagline rules, replaced by the lockup below.
TAGLINE_OLD = (
    ".logo__tagline{display:block;margin:5px 0 0 5px;text-indent:0;white-space:nowrap;"
    "font-family:'Noto Serif',Georgia,serif;font-style:italic;font-weight:700;"
    "font-size:11px;line-height:1.1;letter-spacing:0;color:#2a2a2a}\n"
    ".home header .logo__tagline{color:inherit;text-shadow:0 1px 3px rgba(0,0,0,.45)}\n"
    "@media (min-width:1024px){.logo__tagline{margin-left:6px;font-size:12px}}\n"
)
TAGLINE_NEW = (
    ".logo__tagline{display:block;box-sizing:border-box;margin-top:5px;text-indent:0;white-space:nowrap;"
    "text-align:center;font-family:'Noto Serif',Georgia,serif;font-style:italic;font-weight:700;"
    "line-height:1.1;letter-spacing:0;color:#2a2a2a;"
    # the pill spans 19.5..540.5 of the logo's 560 units
    "width:calc(var(--logo-w) * 521 / 560);margin-left:calc(var(--logo-w) * 19.5 / 560);"
    "font-size:calc(var(--logo-w) * 521 / 560 / 16.81)}\n"
    ".home header .logo__tagline{color:inherit;text-shadow:0 1px 3px rgba(0,0,0,.45)}\n"
    "header .logo{--logo-w:172px}header .logo img{width:var(--logo-w)}\n"
    "@media (min-width:1024px){header .logo{--logo-w:208px}header .logo img{width:var(--logo-w)}}\n"
)

MARKER = "/* smag: ux polish */"
RULES = f"""
{MARKER}
footer{{margin-bottom:0}}
@media (min-width:550px){{footer{{margin-bottom:0}}}}
::selection{{background:#E20026;color:#fff}}
a{{text-underline-offset:.18em}}
:focus-visible{{outline:2px solid #E20026;outline-offset:3px}}
.row--action a:focus-visible,.button:focus-visible,.hc-wa:focus-visible{{outline-color:#1B1D1F}}
.skip-link{{position:absolute;left:12px;top:-60px;z-index:200;background:#1B1D1F;color:#fff;padding:.7em 1.1em;font-weight:500;text-decoration:none;transition:top .15s ease-out}}
.skip-link:focus{{top:12px}}.skip-link:hover{{color:#fff}}
header nav li.parent:focus-within .children{{opacity:1;pointer-events:auto}}
body{{--hdr:111px}}
@media (min-width:550px){{body{{--hdr:125px}}}}
.mobile-drawer{{top:var(--hdr);height:calc(100% - var(--hdr))}}
header .main-nav{{top:var(--hdr);height:calc(100% - var(--hdr))}}
@media (min-width:1280px){{header .main-nav{{top:0;height:100%}}}}
header .other-nav{{display:flex;align-items:center}}
.header-contact{{display:flex;align-items:center;gap:10px;text-indent:0}}
.header-contact a{{display:inline-flex;align-items:center;justify-content:center;gap:.5em;box-sizing:border-box;width:40px;height:40px;text-decoration:none;white-space:nowrap;transition:background-color .15s ease-out,color .15s ease-out,border-color .15s ease-out}}
.header-contact a span{{display:none}}
.header-contact i{{font-size:17px}}
.hc-call{{border:1px solid rgba(27,29,31,.25)}}
.home header .hc-call{{border-color:rgba(255,255,255,.55)}}
.sticky-header .hc-call{{border-color:rgba(27,29,31,.25)}}
.hc-call:hover{{border-color:currentColor}}
.header-contact .hc-wa{{background:#E20026;color:#fff}}
.header-contact .hc-wa:hover{{background:#b8001f}}
@media (min-width:1280px){{
.header-contact{{gap:18px}}
.header-contact a{{width:auto;height:auto}}
.header-contact a span{{display:inline}}
.header-contact i{{font-size:15px}}
.hc-call,.home header .hc-call,.sticky-header .hc-call{{border:0;font-weight:500;padding:.5em 0}}
.hc-call:hover span{{text-decoration:underline}}
.header-contact .hc-wa{{padding:.62em 1.05em;font-weight:500}}
}}
.product__image .zoom-tip{{z-index:2;pointer-events:none}}
.statistics .row__inner.statistics__three{{grid-template-columns:1fr;grid-gap:28px}}
@media (min-width:768px){{.statistics .row__inner.statistics__three{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
.FormBuilder .InputfieldStateRequired label:not(.checkbox-label):not(.radio-label)::after{{content:" *";color:#E20026}}
.home .sticky-header .hc-call{{border-color:rgba(27,29,31,.25)}}
.home .sticky-header .logo__tagline{{text-shadow:none}}
.FormBuilder label:not(.radio-label):not(.checkbox-label)::after{{content:""}}
footer .footer-columns .address,footer .footer-columns ul,footer .row--bordered p{{color:#5F646A}}
footer .row--bordered p{{font-size:.7em}}
.breadcrumbs span,.product__gallery .zoom-tip,form .description,form .notes{{color:#666A6F}}
@media (max-width:1023px){{.contact-detail__locations{{order:-1}}}}
@media (max-width:549px){{.locations__item{{grid-template-columns:1fr;grid-gap:4px}}.locations__item>div:last-child{{margin-left:0}}}}
"""

AREA = 4600      # target visual area per client logo, px squared
MAX_H, MAX_W = 58, 172


def trim(path: Path) -> tuple[int, int]:
    """Crop blank margins, keeping a 4% pad; return the new size."""
    im = Image.open(path)
    rgba = im.convert("RGBA")
    alpha = rgba.split()[-1].point(lambda v: 255 if v > 8 else 0)
    ink = ImageChops.difference(rgba.convert("RGB"), Image.new("RGB", im.size, "white"))
    mask = ImageChops.multiply(ink.convert("L").point(lambda v: 255 if v > 18 else 0), alpha)
    bb = mask.getbbox()
    if not bb:
        return im.size
    pad = round(0.04 * max(bb[2] - bb[0], bb[3] - bb[1]))
    box = (max(bb[0] - pad, 0), max(bb[1] - pad, 0), min(bb[2] + pad, im.width), min(bb[3] + pad, im.height))
    if (box[2] - box[0]) * (box[3] - box[1]) < 0.85 * im.width * im.height:
        if not DRY:
            im.crop(box).save(path, optimize=True)
        print(f"  trimmed {path.name}: {im.width}x{im.height} -> {box[2]-box[0]}x{box[3]-box[1]}")
        return box[2] - box[0], box[3] - box[1]
    return im.size


def svg_ratio(path: Path) -> float:
    vb = re.search(r'viewBox="([\d.\s-]+)"', path.read_text(encoding="utf-8"))
    _, _, w, h = map(float, vb.group(1).split())
    return w / h


def logo_heights() -> dict[str, int]:
    heights = {}
    for p in sorted(CLIENTS.iterdir()):
        if p.suffix == ".png":
            w, h = trim(p)
            r = w / h
        elif p.suffix == ".svg":
            r = svg_ratio(p)
        else:
            continue
        hgt = min(MAX_H, math.sqrt(AREA / r))
        if hgt * r > MAX_W:
            hgt = MAX_W / r
        heights[p.name] = round(hgt)
    return heights


def main() -> int:
    heights = logo_heights()
    counts = dict(header=0, skip=0, stats=0, logos=0)
    for f in sorted(SITE.rglob("*.html")):
        s = orig = f.read_text(encoding="utf-8")
        if OTHER_NAV_OLD in s:
            s = s.replace(OTHER_NAV_OLD, OTHER_NAV_NEW)
            counts["header"] += 1
        if "class=skip-link" not in s and "<main>" in s:
            s = re.sub(r"(<body[^>]*>)", r"\1<a class=skip-link href=#main>Skip to content</a>", s, count=1)
            s = s.replace("<main>", "<main id=main>", 1)
            counts["skip"] += 1
        if STATS_OLD in s:
            s = s.replace(STATS_OLD, STATS_NEW)
            counts["stats"] += 1
        if "class=clients-strip" in s:
            def size(m: re.Match) -> str:
                name = m.group(1)
                tag = re.sub(r' style="height:\d+px"', "", m.group(0))
                return tag.replace("<img ", f'<img style="height:{heights[name]}px" ', 1)
            s2 = re.sub(r"<img [^>]*src=/site/assets/images/clients/([^ >]+)[^>]*>", size, s)
            counts["logos"] += s2 != s
            s = s2
        if s != orig and not DRY:
            f.write_text(s, encoding="utf-8")
    for k, v in counts.items():
        print(f"  {k:7s} {v} pages")

    css = CSS.read_text(encoding="utf-8")
    if TAGLINE_OLD in css:
        css = css.replace(TAGLINE_OLD, TAGLINE_NEW)
        print("  tagline rules replaced with the lockup")
    if MARKER not in css:
        css += RULES
        print("  ux polish rules appended")
    if not DRY:
        CSS.write_text(css, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
