#!/usr/bin/env python3
"""Build the Indian language copies of the site from the English pages.

    build.py [--dry-run]

For each language in LANGS, every English page whose segments are at least
MIN_COVER translated is written to site/<lang>/<same path>, with:

- each segment and readable attribute swapped for its translation
  (assets/source/i18n/<lang>/*.json, merged);
- links to pages that exist in that language pointed at the language copy,
  and links to pages that do not yet exist left on the English page;
- lang, canonical and og:url set for the language;
- the enquiry form's email subject naming the language, so SMAG knows which
  language to reply in.

Every page, English included, then gets hreflang alternates for the
languages it exists in and the language menu: a small menu in the header and
a row of language links in the mobile drawer, each linking to the same page
in that language, or to that language's home page if the page is not
translated yet. site/sitemap.xml lists every language page.

Re-running rebuilds everything from the English pages and the translations.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import extract as X  # noqa: E402
import segments as S  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
SRC = REPO / "assets/source/i18n"
ORIGIN = "https://santoshmagneticworks.com"
DRY = "--dry-run" in sys.argv
MIN_COVER = 0.97

# code, name in its own script, English name (for the enquiry subject)
LANGS = [
    ("hi", "हिन्दी", "Hindi"), ("mr", "मराठी", "Marathi"), ("gu", "ગુજરાતી", "Gujarati"),
    ("kn", "ಕನ್ನಡ", "Kannada"), ("te", "తెలుగు", "Telugu"), ("ml", "മലയാളം", "Malayalam"),
    ("ta", "தமிழ்", "Tamil"),
]
ALL = [("en", "English", "English")] + LANGS
HREF = re.compile(r'(\shref=)("?)(/(?!/)[^"\s>]*)\2')
SWITCH = re.compile(r"<details class=lang-switch>.*?</details>", re.S)
DRAWER = re.compile(r"<ul class=drawer-langs>.*?</ul>", re.S)
ALTS = re.compile(r"<link rel=alternate hreflang=[^>]*>")
GLOBE = ('<svg viewBox="0 0 24 24" width=16 height=16 aria-hidden=true><circle cx=12 cy=12 r=9 fill=none '
         'stroke=currentColor stroke-width=1.6 /><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9'
         'c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z" fill=none stroke=currentColor stroke-width=1.6 /></svg>')


def url_of(rel: str) -> str:
    """Page file (index.html, a/b/index.html) to its URL path (/, /a/b/)."""
    return "/" + rel[: -len("index.html")] if rel.endswith("index.html") else "/" + rel


def rel_of(path: str) -> str | None:
    """URL path to page file, or None for anything that is not a page."""
    path = path.split("#")[0].split("?")[0]
    if path.startswith("/site/") or path.startswith("/brochures/") and path != "/brochures/":
        return None
    if path.endswith("/"):
        return path[1:] + "index.html"
    return None


def load(lang: str) -> dict[str, str]:
    tr: dict[str, str] = {}
    for p in sorted((SRC / lang).glob("*.json")):
        tr.update(json.loads(p.read_text(encoding="utf-8")))
    return tr


def lookup_for(tr: dict[str, str]):
    def look(text: str):
        return tr.get(S.key_of(text))
    return look


def coverage(page: str, look) -> float:
    _, done, left = S.translate(page, look)
    return done / max(done + left, 1)


def switcher(rel: str, here: str, has: dict[str, set[str]]) -> tuple[str, str]:
    """The header menu and the drawer row for one page in one language."""
    def link(code: str) -> str:
        if code == "en":
            return url_of(rel)
        return f"/{code}{url_of(rel)}" if rel in has[code] else f"/{code}/"
    name = dict((c, n) for c, n, _ in ALL)[here]
    items = "".join(
        f'<li><a href={link(c)} lang={c} hreflang={c}'
        f'{" aria-current=true" if c == here else ""}>{n}</a>'
        for c, n, _ in ALL)
    menu = (f"<details class=lang-switch><summary>{GLOBE}<span lang={here}>{name}</span></summary>"
            f"<ul>{items}</ul></details>")
    return menu, f"<ul class=drawer-langs>{items}</ul>"


def dress(page: str, rel: str, here: str, has: dict[str, set[str]]) -> str:
    """Add the hreflang alternates and the language menu to a page."""
    page = SWITCH.sub("", ALTS.sub("", page))
    page = DRAWER.sub("", page)
    alts = [f"<link rel=alternate hreflang=en href={ORIGIN}{url_of(rel)}>"]
    alts += [f"<link rel=alternate hreflang={c} href={ORIGIN}/{c}{url_of(rel)}>"
             for c, _, _ in LANGS if rel in has[c]]
    if len(alts) > 1:
        alts.append(f"<link rel=alternate hreflang=x-default href={ORIGIN}{url_of(rel)}>")
        page = re.sub(r"(<link rel=canonical[^>]*>)", lambda m: m.group(1) + "".join(alts), page, count=1)
    menu, drawer = switcher(rel, here, has)
    page = page.replace("<div class=header-contact>", menu + "<div class=header-contact>", 1)
    page = page.replace("</ul></div></div><main", f"</ul>{drawer}</div></div><main", 1)
    return page


def localise(page: str, rel: str, code: str, english: str, look, has: set[str]) -> str:
    page, _, _ = S.translate(page, look)
    page = page.replace("<html lang=en>", f"<html lang={code}>", 1)

    def href(m: re.Match) -> str:
        target = rel_of(m.group(3))
        if target and target in has:
            return f"{m.group(1)}{m.group(2)}/{code}{m.group(3)}{m.group(2)}"
        return m.group(0)
    page = HREF.sub(href, page)
    here = f"{ORIGIN}/{code}{url_of(rel)}"
    page = re.sub(r"<link rel=canonical href=[^>]*>", f"<link rel=canonical href={here}>", page, count=1)
    page = re.sub(r"<meta property=og:url content=[^>]*>", f"<meta property=og:url content={here}>", page, count=1)
    page = page.replace('value="New enquiry from the SMAG website"',
                        f'value="New enquiry from the SMAG website ({english})"')
    return page


def sitemap(has: dict[str, set[str]]) -> None:
    path = SITE / "sitemap.xml"
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"  <url><loc>" + re.escape(ORIGIN) + r"/(?:" + "|".join(c for c, _, _ in LANGS)
               + r")/[^<]*</loc></url>\n", "", s)
    add = "".join(f"  <url><loc>{ORIGIN}/{c}{url_of(rel)}</loc></url>\n"
                  for c, _, _ in LANGS for rel in sorted(has[c]))
    s = s.replace("</urlset>", add + "</urlset>")
    if not DRY:
        path.write_text(s, encoding="utf-8")


def main() -> int:
    pages = {p.relative_to(SITE).as_posix(): p.read_text(encoding="utf-8")
             for p in X.pages() if p.name == "index.html"}
    # English pages carry the menu already after the first run; strip it so
    # the translation input is the same every time
    english = {rel: DRAWER.sub("", SWITCH.sub("", ALTS.sub("", s))) for rel, s in pages.items()}
    has: dict[str, set[str]] = {}
    looks = {}
    for code, _, _ in LANGS:
        looks[code] = lookup_for(load(code))
        has[code] = {rel for rel, s in english.items() if coverage(s, looks[code]) >= MIN_COVER}
        print(f"  {code}: {len(has[code])} of {len(english)} pages translated")
    for code, _, name in LANGS:
        out_root = SITE / code
        if out_root.exists() and not DRY:
            shutil.rmtree(out_root)
        for rel in sorted(has[code]):
            page = localise(english[rel], rel, code, name, looks[code], has[code])
            page = dress(page, rel, code, has)
            if not DRY:
                out = out_root / rel
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(page, encoding="utf-8")
    for rel, s in english.items():
        new = dress(s, rel, "en", has)
        if not DRY and new != pages[rel]:
            (SITE / rel).write_text(new, encoding="utf-8")
    sitemap(has)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
