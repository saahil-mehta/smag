#!/usr/bin/env python3
"""Add SMAG's client logo strip to the home and About pages.

On the home page it replaces the testimonials carousel. Those nine quotes are
named individuals at UK companies (AB MAURI, Simpsons Malt, Vallourec, the
Nuclear AMRC, Roquette) endorsing Eclipse; presenting them on this site would
attribute other firms' endorsements to SMAG.

The strip sits on a white row rather than a row--alt one on purpose: 15 of the
28 PNG logos are opaque with white backgrounds, and on the site's #F5F3F2
paper they would render as visible white rectangles. White background means
all 30 sit consistently without editing the artwork.

Every logo is already 120px tall, so they are copied as-is and displayed at
60px, giving a 2x pixel ratio for retina with no resampling.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
SRC_LOGOS = REPO / "assets/logos"
DEST_LOGOS = SITE / "site/assets/images/clients"
WEB_PATH = "/site/assets/images/clients"

DISPLAY_H = 60

# Filename stem -> display name for alt text.
NAMES = {
    "astral": "Astral", "britannia": "Britannia", "camlin-kokuyo": "Camlin Kokuyo",
    "castrol": "Castrol", "doms": "DOMS", "dukes": "Dukes",
    "empire-spices": "Empire Spices", "finolex": "Finolex", "hppl": "HPPL",
    "itc": "ITC", "johnson-matthey": "Johnson Matthey", "kabra": "Kabra",
    "klassic-klarol": "Klassic Klarol", "kleenoil": "Kleenoil",
    "lotte-chemical": "Lotte Chemical", "lucas": "Lucas", "matsui": "Matsui",
    "motan": "Motan", "nayara": "Nayara", "nilkamal": "Nilkamal",
    "parle": "Parle", "patanjali": "Patanjali", "prince-pipe": "Prince Pipe",
    "priyagold": "Priyagold", "reliance": "Reliance", "shibaura": "Shibaura",
    "smoor": "Smoor", "times-automation": "Times Automation",
    "uno-minda": "UNO Minda", "wittmann": "Wittmann",
}


def copy_logos() -> list[tuple[str, str]]:
    DEST_LOGOS.mkdir(parents=True, exist_ok=True)
    out = []
    for src in sorted(SRC_LOGOS.iterdir()):
        if src.suffix.lower() not in (".png", ".svg", ".jpg"):
            continue
        shutil.copyfile(src, DEST_LOGOS / src.name)
        out.append((src.name, NAMES.get(src.stem, src.stem.replace("-", " ").title())))
    return out


def build_strip(logos: list[tuple[str, str]], heading: str, sub: str) -> str:
    imgs = "".join(
        f'<img src={WEB_PATH}/{fn} height={DISPLAY_H} '
        f'style="height:{DISPLAY_H}px;width:auto;max-width:170px;'
        'object-fit:contain;flex:0 0 auto" '
        f'alt="{name}" loading=lazy decoding=async>'
        for fn, name in logos
    )
    # A closing label so the strip reads as a sample, not the full list.
    more = (
        '<span style="height:60px;display:flex;align-items:center;'
        "font-weight:600;font-size:.95em;color:#6b6770;flex:0 0 auto">"
        "+ many more</span>"
    )
    return (
        '<div class="row">'
        '<div class="row__inner row__intro">'
        f'<h3 class=bordered-header>{heading}</h3>'
        f'<p class=intro>{sub}'
        "</div>"
        "<div class=row__inner>"
        '<div class=clients-strip style="display:flex;flex-wrap:wrap;'
        "align-items:center;justify-content:center;gap:34px 46px\">"
        f"{imgs}{more}"
        "</div></div></div>"
    )


HOME_TESTIMONIALS_RE = re.compile(
    r'<div class="row testimonials">.*?(?=<div class="row row--action">)',
    re.DOTALL,
)
ABOUT_TAIL_RE = re.compile(r'(</div>)(<div class="row row--action">)')


def main() -> None:
    logos = copy_logos()
    total_kb = sum((DEST_LOGOS / f).stat().st_size for f, _ in logos) // 1024
    print(f"copied {len(logos)} logos ({total_kb} KB) -> {DEST_LOGOS.relative_to(SITE)}")

    strip_home = build_strip(
        logos,
        "Running on production lines across India",
        "Some of the manufacturers using our equipment.",
    )
    strip_about = build_strip(
        logos,
        "Who we supply",
        "Plants in food, plastics, chemicals, automotive and general "
        "engineering.",
    )

    # Home: swap the Eclipse testimonials carousel for the strip.
    home = SITE / "index.html"
    t = home.read_text(encoding="utf-8")
    t2, n = HOME_TESTIMONIALS_RE.subn(strip_home, t, count=1)
    if n:
        home.write_text(t2, encoding="utf-8")
        print(f"home: testimonials replaced with logo strip "
              f"({len(t)} -> {len(t2)} bytes)")
    else:
        print("home: NO testimonials block matched")

    # About: append the strip just before the closing CTA row.
    about = SITE / "company/about-us/index.html"
    a = about.read_text(encoding="utf-8")
    if "clients-strip" in a:
        print("about: strip already present, skipping")
    else:
        a2, n = ABOUT_TAIL_RE.subn(
            lambda m: strip_about + m.group(1) + m.group(2), a, count=1
        )
        if n:
            about.write_text(a2, encoding="utf-8")
            print(f"about: logo strip added ({len(a)} -> {len(a2)} bytes)")
        else:
            print("about: NO insertion point matched")

    for page in (home, about):
        s = page.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<main>.*</main>", s, re.DOTALL)
        seg = m.group(0)
        o, c = len(re.findall(r"<div\b", seg)), len(re.findall(r"</div>", seg))
        left = len(re.findall(r"testimonial|Eclipse Magnetics", seg))
        print(f"  {page.relative_to(SITE)}: div {o}/{c} "
              f"{'OK' if o == c else 'MISMATCH'}, testimonial/Eclipse refs {left}")


if __name__ == "__main__":
    main()
