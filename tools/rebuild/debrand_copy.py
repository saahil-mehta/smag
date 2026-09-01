#!/usr/bin/env python3
"""Replace or remove the Eclipse copy the earlier sweeps left in place.

Three layers, applied in order:

1. Element removals: whole rows/cards for things SMAG cannot claim at all
   (the Sesotec partnership, Eclipse's distributor network, Eclipse staff
   profiles, the ATEX icon box) and every list bullet claiming ATEX.
2. Curated sentence rewrites: Eclipse's century of history becomes SMAG's
   real history (works founded 1978), the UK/Sheffield framing becomes
   Mumbai, Eclipse's client list and ISO 14001 self-claims go, ATEX claims
   in running prose go. Anchored, bounded regexes; entity and curly-quote
   tolerant.
3. Blanket brand swap: any remaining "Eclipse Magnetics" text becomes
   Santosh Magnetic Works (possessives become SMAG's), then stray
   standalone "Eclipse" words become SMAG. Asset paths are excluded.

Also drops og:image tags whose file does not exist locally (the domain swap
left them pointing at images the mirror never fetched).

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end, li_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

# needles whose innermost enclosing card/row is removed entirely
ELEMENT_NEEDLES = [
    "Sesotec", "SESOTEC", "Richard Leach",
    "Global Distribution of Our Products",
    "Stockists can also add value",
    "Meet the minimum safety requirements of the workplace",
]
CONTAINER_RES = [
    re.compile(r'<div class="?icon_boxes_1__item\b[^>]*>'),
    re.compile(r"<div class=accordion__item>"),
    re.compile(r'<div class="?grid__item\b[^>]*>'),
    re.compile(r'<div class="?swiper-slide\b[^>]*>'),
    re.compile(r'<div class="?row\b[^>]*>'),
]

# (pattern, replacement) applied in order; bounded and anchored
REWRITES: list[tuple[str, str]] = [
    (r"With more than 100 years of magnetic engineering heritage"
     r"[\s\S]{0,400}?for over a century, supplying",
     "Santosh Magnetic Works has built its reputation on reliability and "
     "technical care since 1978, supplying"),
    (r"At Eclipse Magnetics we(?:’|&#039;|')ve spent over 100 years "
     r"enabling our customers to [\"“]Work Smart with Magnets[\"”] by "
     r"saving time, money or improving safety",
     "At Santosh Magnetic Works we have spent more than four decades "
     "helping customers save time and money and improve safety"),
    (r"As a 100-year-old company based in Sheffield, the home of steel, "
     r"it is no surprise we are",
     "From our works in Mumbai, we are"),
    (r"\s*Our client base includes leading names such as"
     r"[\s\S]{0,700}?Abbey Forged Products\.</strong>", ""),
    (r"For over 100 years(?:’|&#039;|')? we have been the benchmark for "
     r"quality and pioneered",
     "Since 1978 we have set our benchmark on quality and"),
    (r"With over 100 years of magnetic expertise, we are one of the "
     r"world(?:’|&#039;|')s leading magnet suppliers\.",
     "With decades of magnetic expertise, we build magnets to your "
     "specification."),
    (r"With over 100 years(?:’|&#039;|')? experience in the design and "
     r"manufacture of high performance magnetic systems, we serve",
     "We design and manufacture high performance magnetic systems, "
     "serving"),
    (r"Eclipse Magnetics offers over 100 years of expertise in magnetic "
     r"technology,",
     "Santosh Magnetic Works offers decades of expertise in magnetic "
     "technology,"),
    (r"and over 100 years of magnetic expertise",
     "and decades of magnetic expertise"),
    (r"Our 100 years of magnetic expertise",
     "Our decades of magnetic expertise"),
    (r"\s*We are also certified in the ISO 14001 Environmental Management "
     r"System\.", ""),
    (r"Eclipse Magnetics has a UK Quality Control system that helps us",
     "We run a quality control system that helps us"),
    # ATEX claims in running prose
    (r"\s*Our products can be supplied with full[\s\S]{0,160}?ATEX"
     r"[\s\S]{0,80}?\.", ""),
    (r"\s*Available fully ATEX certified\.", ""),
    (r"\s*and can be made ATEX certified to work in hazardous and "
     r"explosive conditions", ""),
    (r"\s*and are also available fully ATEX certified", ""),
    (r"\s*Many of our (?:magnetic separation )?products"
     r"(?: also)? carry (?:the relevant approvals such as ATEX"
     r"|ATEX[^.<]*)\.?", ""),
    (r"\s*Many of our magnetic separators carry ATEX type approval\.", ""),
    (r"\s*Eclipse Magnetics also offer; where applicable; ATEX-certified "
     r"units[^.<]*\.", ""),
    (r"(?:\s|&nbsp;)+including ATEX environments", ""),
    (r",?(?:\s|&nbsp;)+including ATEX certification for hazardous"
     r"(?:\s|&nbsp;)+environments", ""),
    (r"BRC,(?:\s|&nbsp;)+HACCP(?:\s|&nbsp;)+and(?:\s|&nbsp;)+ATEX"
     r"(?:\s|&nbsp;)+standards", "BRC and HACCP standards"),
    (r"(?:\s|&nbsp;)*ATEX approved version available\.", ""),
    # Eclipse's web shop and brochure plug
    (r"<p>For customers looking to buy online[\s\S]{0,600}?of all sizes\.",
     ""),
    (r"Download Work Smart [Ww]ith Magnets Brochure",
     "Download our brochures"),
    (r"eclipse magnetic chuck repair,\s*", ""),
    # Eclipse slogan
    (r"Work Smart with Magnets", "Put Magnets to Work"),
    # mop-up for any remaining corporate-age claim
    (r"over 100 years", "many decades"),
]

BRAND_SWAPS = [
    ("Eclipse Magnetics&#039;", "SMAG&#039;s"),
    ("Eclipse Magnetics’", "SMAG’s"),
    ("Eclipse Magnetics'", "SMAG's"),
    ("Eclipse Magnetics", "Santosh Magnetic Works"),
]
# standalone leftover, excluding asset paths and lowercase filenames
ECLIPSE_WORD = re.compile(r"(?<![/_\-.a-zA-Z0-9])Eclipse(?![a-zA-Z])")

ATEX_IMG = re.compile(r"<img[^>]*atex[^>]*>", re.I)
OG_IMAGE = re.compile(r'<meta property=og:image content="?([^">]+)"?>')


def remove_elements(text: str) -> tuple[str, int]:
    removed = 0
    for needle in ELEMENT_NEEDLES:
        while needle in text:
            i = text.find(needle)
            best = None
            for cre in CONTAINER_RES:
                for c in cre.finditer(text, 0, i):
                    end = find_element_end(text, c.start())
                    if end and c.start() < i < end:
                        span = end - c.start()
                        if best is None or span < best[2]:
                            best = (c.start(), end, span)
            if best:
                text = text[: best[0]] + text[best[1]:]
                removed += 1
            else:
                text = text.replace(needle, "", 1)
    return text, removed


def remove_atex_lis(text: str) -> tuple[str, int]:
    """Remove every short <li> bullet claiming ATEX; leave other hits."""
    removed = 0
    changed = True
    while changed:
        changed = False
        for m in re.finditer(r"ATEX", text):
            best = None
            for c in re.finditer(r"<li\b[^>]*>", text[: m.start()]):
                end = (find_element_end(text, c.start())
                       or li_element_end(text, c.start()))
                if end and c.start() < m.start() < end:
                    span = end - c.start()
                    if best is None or span < best[2]:
                        best = (c.start(), end, span)
            if best and best[2] < 800:
                text = text[: best[0]] + text[best[1]:]
                removed += 1
                changed = True
                break
    return text, removed


def main() -> None:
    dry = "--dry-run" in sys.argv
    stats = {"elements": 0, "lis": 0, "rewrites": 0, "brand": 0, "og": 0}

    for page in sorted(SITE.rglob("*.html")):
        text = orig = page.read_text(encoding="utf-8")

        text, n = remove_elements(text)
        stats["elements"] += n

        # the guides filter form still lists Eclipse product types and its
        # filter result pages no longer exist
        while "category-filter" in text:
            f = None
            for m in re.finditer(r"<form\b[^>]*>", text):
                end = find_element_end(text, m.start())
                if end and "category-filter" in text[m.start():end]:
                    f = (m.start(), end)
                    break
            if not f:
                break
            text = text[: f[0]] + text[f[1]:]
            stats["elements"] += 1

        for pat, repl in REWRITES:
            text, n = re.subn(pat, repl, text)
            stats["rewrites"] += n

        text, n = remove_atex_lis(text)
        stats["lis"] += n
        text = ATEX_IMG.sub("", text)

        for old, new in BRAND_SWAPS:
            stats["brand"] += text.count(old)
            text = text.replace(old, new)
        text, n = ECLIPSE_WORD.subn("SMAG", text)
        stats["brand"] += n

        for m in reversed(list(OG_IMAGE.finditer(text))):
            path = urlparse(m.group(1)).path
            if path.startswith("/site/") and not (SITE / path.lstrip("/")).exists():
                text = text[: m.start()] + text[m.end():]
                stats["og"] += 1

        if text != orig and not dry:
            page.write_text(text, encoding="utf-8")

    print(stats)


if __name__ == "__main__":
    main()
