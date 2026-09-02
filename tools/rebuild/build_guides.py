#!/usr/bin/env python3
"""Build the Guides section from SMAG's own markdown sources.

Sources: assets/source/guides/<slug>.md, one per guide, with a small front
matter block (title, category, description, image, product, product_label,
home). The body is plain markdown: ## headings, paragraphs, - and 1. lists,
**bold**, [links](/path/) and | tables |. Keeping the copy in markdown makes
it reviewable in git and hands the next workstream (translation) a clean
source per page.

Builds:
  - one guide page per source, inside the chrome of the existing guide page
    (donor: are-all-stainless-steels-magnetic) with the Eclipse byline date,
    tag filter form and broken share buttons removed
  - the /resources/guides/ index: new intro, one card per guide, no
    pagination (the crawl never fetched pages 2 to 6)
  - the home page Resources carousel: six slides from guides marked home:
    true, tagged Guide, with SMAG imagery
  - card renditions (315x247 index, 350x370 home) from the brochure stills,
    watermarked like every other catalogue image
  - sitemap rows renamed to the new titles

Copy rules applied to the sources: very simple English, short sentences,
no idioms, no contrastive negation, translatable. See the memory notes.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_smag_product_pages as build  # noqa: E402
from remove_sections import find_element_end  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
SRC = REPO / "assets/source/guides"
GUIDES = SITE / "resources/guides"
DONOR = GUIDES / "are-all-stainless-steels-magnetic/index.html"
HOME = SITE / "index.html"
SMAP = SITE / "sitemap/index.html"
DOMAIN = "https://santoshmagneticworks.com"

CATEGORY_ORDER = ["Basics", "Food Safety", "Separation", "Lifting",
                  "Workholding", "Filtration"]

INDEX_INTRO = (
    "<h2>Guides</h2>"
    "<p>Short, plain guides on magnets and how they are used in a factory. "
    "Which metals a magnet holds. How to keep metal out of food. How to lift "
    "steel safely. How to choose a chuck or a filter."
    "<p>If your question is not answered here, ask us. We reply with a "
    "straight answer and, where it helps, a recommendation for your line."
    '<p> <p><a class=button href=/contact-us/>Ask a question</a>'
)


# --- markdown ---------------------------------------------------------------
def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def render(md: str) -> str:
    out: list[str] = []
    lines = md.strip().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("## "):
            out.append(f"<h3>{inline(line[3:].strip())}</h3>")
            i += 1
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells if c):
                    rows.append(cells)
                i += 1
            head, body = rows[0], rows[1:]
            th = "".join(f"<th>{inline(c)}" for c in head)
            tr = "".join("<tr>" + "".join(f"<td>{inline(c)}" for c in r)
                         for r in body)
            out.append('<div style="overflow-x:auto"><table>'
                       f"<thead><tr>{th}</thead><tbody>{tr}</tbody></table></div>")
        elif re.match(r"^(- |\d+\. )", line):
            ordered = line[0].isdigit()
            items = []
            while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
                items.append(re.sub(r"^(- |\d+\. )", "", lines[i]).strip())
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(t)}" for t in items)
                       + f"</{tag}>")
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(## |- |\d+\. |\|)", lines[i]):
                para.append(lines[i].strip())
                i += 1
            out.append(f"<p>{inline(' '.join(para))}")
    return "".join(out)


def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    meta["home"] = meta.get("home", "false").lower() == "true"
    meta["slug"] = path.stem
    meta["body"] = m.group(2)
    words = len(re.sub(r"[#*|\[\]()-]", " ", meta["body"]).split())
    meta["words"] = words
    if not (SRC.parent / "brochure-stills" / f"{meta['image']}.png").exists():
        raise FileNotFoundError(f"{path.name}: no still {meta['image']}.png")
    return meta


# --- renditions -------------------------------------------------------------
def card(stem: str, kind: str, tw: int, th: int) -> str:
    """Fit the still inside tw x th on white, watermark, return URL."""
    src = build.prepared(stem)
    w, h = build.dims(src)
    dst = build.IMGDIR / f"{stem}.{kind}.jpg"
    scale = (["--resampleWidth", str(tw)] if w / h > tw / th
             else ["--resampleHeight", str(th)])
    build.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
               *scale, "--padToHeightWidth", str(th), str(tw),
               "--padColor", "FFFFFF", str(src), "--out", str(dst)])
    build.watermark(dst)
    return f"{build.IMGURL}/{stem}.{kind}.jpg"


# --- page -------------------------------------------------------------------
def guide_page(g: dict, donor: str) -> str:
    url = f"/resources/guides/{g['slug']}/"
    title = html.escape(g["title"], quote=False)
    desc = html.escape(g["description"], quote=True)
    back = '<p class=back-link><a href=/resources/guides/>Back to Guides</a>'
    main = (
        '<main><div class="content-wrapper content-wrapper--no-testimonials">'
        '<div class="row article-intro"><div class="row__inner row__inner--narrow">'
        f"<div class=breadcrumbs><a href=/resources/guides/>Guides</a> / {title} </div>"
        f"<h1 class=bordered-header>{title}</h1>"
        f"<p class=byline>{g['category']} guide"
        f'<p class="back-link back-link--desktop"><a href=/resources/guides/>'
        "Back to Guides</a></div></div>"
        '<div class="row row--bordered"><div class="row__inner row__inner--narrow content">'
        f"<div class=page-builder-simple><div>{render(g['body'])}</div></div>"
        f"{back}</div></div></div>"
        # outside the content wrapper: its last-row rule would otherwise add
        # 5.8em of bottom padding and push the banner text to the top
        '<div class="row row--action"><div class=row__inner><h3><a href=/contact-us/>\n'
        "Tell us about the application and we will come back with a recommendation "
        "<i aria-hidden=true class=icon></i> </a></h3></div></div></main>"
    )
    ms, me = donor.find("<main"), donor.find("</main>") + len("</main>")
    page = donor[:ms] + main + donor[me:]
    page = re.sub(r"<title>[^<]*</title>",
                  f"<title>{title} | Santosh Magnetic Works</title>", page)
    page = re.sub(r'(<meta name=description content=)"[^"]*"', rf'\1"{desc}"', page)
    page = re.sub(r'(<meta property=og:description content=)"[^"]*"',
                  rf'\1"{desc}"', page)
    page = re.sub(r'(<meta property=og:title content=)"[^"]*"',
                  rf'\1"{title} | Santosh Magnetic Works"', page)
    page = re.sub(r"(<meta property=og:url content=)[^>]+>",
                  rf"\1{DOMAIN}{url}>", page)
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Home",
                   "item": f"{DOMAIN}/"},
                  {"@type": "ListItem", "position": 2, "name": "Guides",
                   "item": f"{DOMAIN}/resources/guides/"},
                  {"@type": "ListItem", "position": 3, "name": g["title"],
                   "item": f"{DOMAIN}{url}"}]}
    page = re.sub(r"<script type=application/ld\+json>.*?</script>",
                  "<script type=application/ld+json>"
                  + json.dumps(crumbs, ensure_ascii=False) + "</script>",
                  page, count=1, flags=re.S)
    return page


def index_card(g: dict, img: str) -> str:
    return (f"<div class=grid__item><a href=/resources/guides/{g['slug']}/> "
            f"<span class=tag>\n{g['category']} </span> "
            f'<img src={img} width=315 height=247 alt="" />'
            f"<div><h4>{html.escape(g['title'], quote=False)}</h4>"
            "<p class=read-more>Read More </div></a></div>")


def home_slide(g: dict, img: str) -> str:
    return ('<div class="swiper-slide grid__item expandHint">'
            f"<a href=/resources/guides/{g['slug']}/> <span class=tag> Guide </span> "
            f'<img src={img} width=350 height=370 alt="" />'
            f"<div class=expandHint__text><h4>{html.escape(g['title'], quote=False)}</h4>"
            "<div class=expandHint__positioner></div></div></a></div>")


def replace_between(text: str, opener: str, body: str) -> str:
    i = text.find(opener)
    if i < 0:
        raise ValueError(f"anchor missing: {opener[:50]}")
    end = find_element_end(text, i)
    close = re.match(r"<(\w+)", opener).group(1)
    return text[:i] + opener + body + f"</{close}>" + text[end:]


def main() -> None:
    dry = "--dry-run" in sys.argv
    guides = sorted((load(p) for p in SRC.glob("*.md")),
                    key=lambda g: (CATEGORY_ORDER.index(g["category"]), g["title"]))
    donor = DONOR.read_text(encoding="utf-8")
    if "gallery-swiper" in donor or "<body" not in donor:
        raise ValueError("donor is not a guide page")

    for g in guides:
        page = guide_page(g, donor)
        out = GUIDES / g["slug"] / "index.html"
        print(f"{g['words']:4d} words  {g['category']:<12} {g['slug']}")
        if not dry:
            out.parent.mkdir(exist_ok=True)
            out.write_text(page, encoding="utf-8")

    # index
    idx = GUIDES / "index.html"
    text = idx.read_text(encoding="utf-8")
    cards = "".join(index_card(g, card(g["image"], "card", 315, 247)
                               if not dry else "") for g in guides)
    # idempotent: undo the inline widths added below before re-anchoring
    text = text.replace(
        '<div class="row__inner category-detail" style="grid-template-columns:1fr">',
        '<div class="row__inner category-detail">')
    text = text.replace(
        '<div class="grid grid--resources" style="grid-template-columns:repeat(3,minmax(0,1fr))">',
        '<div class="grid grid--resources">')
    text = replace_between(text, '<div class="grid grid--resources">', cards)
    # The mirror laid the grid beside a filter form in a 1fr 4fr grid. The
    # form posted to a backend and is gone, so the cards were squeezed into
    # the 1fr column. Single column wrapper, three cards per row (the home
    # page already sets its statistics grid the same inline way).
    text = text.replace(
        '<div class="row__inner category-detail">',
        '<div class="row__inner category-detail" style="grid-template-columns:1fr">', 1)
    text = text.replace(
        '<div class="grid grid--resources">',
        '<div class="grid grid--resources" style="grid-template-columns:repeat(3,minmax(0,1fr))">', 1)
    m = re.search(r"<ul class=MarkupPagerNav[^>]*>", text)
    if m:
        end = find_element_end(text, m.start())
        text = text[:m.start()] + text[end:]
    text = replace_between(
        text, '<div class="row__inner row__intro content content--text_2">',
        INDEX_INTRO)
    text = re.sub(r"<title>[^<]*</title>",
                  "<title>Guides | Santosh Magnetic Works</title>", text)
    text = re.sub(r'(<meta (?:name=description|property=og:description) content=)"[^"]*"',
                  r'\1"Plain guides on magnets in industry: which metals are '
                  r'held, keeping metal out of food, lifting steel safely, '
                  r'choosing chucks and filters."', text)
    print(f"index: {len(guides)} cards, pagination removed")
    if not dry:
        idx.write_text(text, encoding="utf-8")

    # home carousel
    home = HOME.read_text(encoding="utf-8")
    featured = [g for g in guides if g["home"]]
    slides = "".join(home_slide(g, card(g["image"], "home", 350, 370)
                                if not dry else "") for g in featured)
    i = home.find('<div class="swiper-container page-swiper">')
    j = home.find("<div class=swiper-wrapper>", i)
    end = find_element_end(home, j)
    home = home[:j] + "<div class=swiper-wrapper>" + slides + "</div>" + home[end:]
    home = home.replace('<div class="row row--alt" id=case-studies>',
                        '<div class="row row--alt" id=guides>', 1)
    home = home.replace("<h3 class=bordered-header>Resources</h3>",
                        "<h3 class=bordered-header>Guides</h3>", 1)
    print(f"home: {len(featured)} slides")
    if not dry:
        HOME.write_text(home, encoding="utf-8")

    # sitemap titles
    smap = SMAP.read_text(encoding="utf-8")
    n = 0
    for g in guides:
        pat = re.compile(rf"(<a href=/resources/guides/{re.escape(g['slug'])}/>)[^<]*(</a>)")
        smap, k = pat.subn(rf"\g<1>{html.escape(g['title'], quote=False)}\g<2>", smap)
        n += k
    print(f"sitemap: {n} guide titles updated")
    if not dry:
        SMAP.write_text(smap, encoding="utf-8")


if __name__ == "__main__":
    main()
