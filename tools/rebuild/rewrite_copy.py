#!/usr/bin/env python3
"""Render SMAG's page copy from markdown sources into the site chrome.

Sources live in assets/source/pages/, mirroring the site path
(products/<family>/<slug>.md, products/<family>/index.md, industries/<slug>.md).
Each has a front matter block (type, title, meta, button) and named
sections. Three page types:

  product   -> product__intro (tagline, bullets) and the Overview tab
               (heading, paragraphs) are replaced; gallery, Technical Data
               and related-product grid are kept; the Eclipse FAQ accordion
               row is removed
  family    -> <main> is rebuilt: banner, breadcrumbs and product grid are
               kept from the page, everything else comes from the source
               (intro, products heading, why-us block)
  industry  -> <main> is rebuilt the same way around banner, breadcrumbs
               and the related-products grid

Product tile blurbs (the <p> under each tile heading) come from the
family source's Tiles section and are applied to every tile on the site
that links to that product, so the grid, related-product rows and industry
pages all say the same thing.

Copy rules: very simple English, short sentences, no idioms, no
contrastive negation, no formulaic openers, translatable. Facts only from
the brochures and inventories in assets/source/.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402
from build_guides import inline, render  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
SRC = REPO / "assets/source/pages"

CTA_ROW = ('<div class="row row--action"><div class=row__inner><h3>'
           "<a href=/contact-us/>\nTell us about the application and we will "
           "come back with a recommendation <i aria-hidden=true class=icon></i>"
           " </a></h3></div></div>")


# --- sources ----------------------------------------------------------------
def load(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    sections: dict[str, str] = {}
    for part in re.split(r"^## ", m.group(2), flags=re.M)[1:]:
        name, _, body = part.partition("\n")
        sections[name.strip().lower()] = body.strip()
    meta["sections"] = sections
    meta["rel"] = path.relative_to(SRC).with_suffix("").as_posix()
    return meta


def split_heading(body: str) -> tuple[str, str]:
    """A section whose first line is '### Heading' -> (heading, rest)."""
    lines = body.strip().splitlines()
    if lines and lines[0].startswith("### "):
        return lines[0][4:].strip(), "\n".join(lines[1:]).strip()
    return "", body


def tiles(body: str) -> dict[str, str]:
    out = {}
    for line in body.splitlines():
        if ":" in line:
            slug, _, blurb = line.partition(":")
            out[slug.strip().lstrip("- ")] = blurb.strip()
    return out


def element(text: str, opener_re: str, start: int = 0) -> tuple[int, int] | None:
    m = re.compile(opener_re).search(text, start)
    if not m:
        return None
    end = find_element_end(text, m.start())
    return (m.start(), end) if end else None


def cut(text: str, span: tuple[int, int]) -> str:
    return text[span[0]:span[1]]


# --- page types -------------------------------------------------------------
def product(text: str, g: dict) -> str:
    s = g["sections"]
    # intro: keep <h1>, replace tagline + bullets, keep the quote button
    sp = element(text, r'<div class="product__intro content">')
    intro = cut(text, sp)
    h1 = re.search(r"<h1[^>]*>.*?</h1>", intro, re.S).group(0)
    h1 = re.sub(r">.*?</h1>", f">{html.escape(g['title'], quote=False)}</h1>", h1, count=1, flags=re.S)
    bullets = "".join(f"<li>{inline(b[2:].strip())}"
                      for b in s.get("bullets", "").splitlines() if b.startswith("- "))
    new_intro = ('<div class="product__intro content">' + h1
                 + f"<p>{inline(s['tagline'].strip())}<ul>{bullets}</ul>"
                 '<div class=c2a><a href=/contact-us/ class="button button--large '
                 'button--full button--with-arrow">Get a quote</a></div></div>')
    text = text[:sp[0]] + new_intro + text[sp[1]:]
    # overview tab body
    sp = element(text, r'<div class=overview><div class="row content">')
    ov_start = sp[0] + len("<div class=overview>")
    inner = element(text, r'<div class="row content">', ov_start)
    heading, body = split_heading(s["overview"])
    new_ov = ('<div class="row content">'
              f"<p class=overview-mini-title>Overview - {html.escape(g['title'], quote=False)} "
              f"<h2>{inline(heading)}</h2>{render(body)}</div>")
    text = text[:inner[0]] + new_ov + text[inner[1]:]
    # FAQ accordion row
    m = re.search(r'<div class="row__inner accordion">', text)
    if m:
        row = text.rfind("<div class=row>", 0, m.start())
        end = find_element_end(text, row)
        text = text[:row] + text[end:]
    # breadcrumb trail ends with the product name
    text = re.sub(r"(<div class=breadcrumbs><div class=row__inner>.*?<span>&nbsp;/&nbsp;</span>)[^<]*(</div></div>)",
                  rf"\1{html.escape(g['title'], quote=False)} \2", text, count=1, flags=re.S)
    # related products row with no tiles left
    sp = element(text, r'<div class="grid grid--product-category">')
    if sp and "grid__item" not in re.sub(r"<div class=grid__item></div>", "", cut(text, sp)):
        row = text.rfind('<div class="row row--alt">', 0, sp[0])
        end = find_element_end(text, row)
        text = text[:row] + text[end:]
    # one call-to-action wording site-wide (pipeline pages had Eclipse's)
    sp = element(text, r'<div class="row row--action">')
    if sp:
        text = text[:sp[0]] + CTA_ROW + text[sp[1]:]
    return text


def rebuild_main(text: str, g: dict, kind: str) -> str:
    s = g["sections"]
    ms, me = text.find("<main"), text.find("</main>") + len("</main>")
    main = text[ms:me]
    banner = cut(main, element(main, r'<div class="banner row">'))
    crumbs = cut(main, element(main, r"<div class=breadcrumbs>"))
    grid_span = element(main, r'<div class="grid grid--product-category">')
    grid = cut(main, grid_span) if grid_span else ""
    subnav = ""
    if kind == "family":
        sn = element(main, r'<div class="row subnav">')
        subnav = cut(main, sn)
        # banner: h1 and button text from the source
        banner = re.sub(r"<h1 class=regular>.*?</h1>",
                        f"<h1 class=regular>{html.escape(g['title'], quote=False)}</h1>",
                        banner, count=1, flags=re.S)
        banner = re.sub(r"<div class=c2a>.*?</div>",
                        f'<div class=c2a><a href=/contact-us/ class=button> {g.get("button", "Ask for a quote")} </a></div>',
                        banner, count=1, flags=re.S)
        # drop the small kicker <h6> some banners carry
        banner = re.sub(r"<h6>.*?</h6>", "", banner, flags=re.S)

    ih, ib = split_heading(s["intro"])
    intro_row = ('<div class=row><div class="row__inner content content--text_1">'
                 f"<div><h2 class=configurable-header>{inline(ih)}</h2></div>"
                 f"<div class=content__body>{render(ib)}"
                 '<div class=c2a><a href=/contact-us/ class=button>Ask for a quote</a>'
                 "</div></div></div></div>")
    rows = [intro_row]
    if grid:
        ph, pb = split_heading(s.get("products", "### Products"))
        rows.append('<div class="row row--alt"><div class="row__inner row__intro">'
                    f"<h3 class=bordered-header>{inline(ph)}</h3>"
                    + (f"<p class=intro>{inline(pb)}" if pb else "")
                    + f"</div><div class=row__inner>{grid}</div></div>")
    for name in ("why", "where", "more"):
        if name in s:
            wh, wb = split_heading(s[name])
            rows.append('<div class=row><div class="row__inner content content--text_2">'
                        f"<div><h2 class=configurable-header>{inline(wh)}</h2></div>"
                        f"<div class=content__body>{render(wb)}</div></div></div>")
    new_main = ('<main><div class="content-wrapper content-wrapper--no-testimonials">'
                + subnav + banner + crumbs + "<div>" + "".join(rows) + "</div></div>"
                + CTA_ROW + "</main>")
    return text[:ms] + new_main + text[me:]


def intro_only(text: str, g: dict) -> str:
    """Replace the first content row's heading and body, keep the rest."""
    s = g["sections"]
    ih, ib = split_heading(s["intro"])
    sp = element(text, r'<div class="row__inner content content--text_\d">')
    inner = cut(text, sp)
    inner = re.sub(r"<h2 class=configurable-header>.*?</h2>",
                   f"<h2 class=configurable-header>{inline(ih)}</h2>", inner, count=1, flags=re.S)
    bs = element(inner, r"<div class=content__body>")
    inner = inner[:bs[0]] + f"<div class=content__body>{render(ib)}</div>" + inner[bs[1]:]
    text = text[:sp[0]] + inner + text[sp[1]:]
    return re.sub(r"<h1 class=regular>.*?</h1>",
                  f"<h1 class=regular>{html.escape(g['title'], quote=False)}</h1>", text, count=1, flags=re.S)


def head(text: str, g: dict) -> str:
    title = html.escape(g["title"], quote=False)
    if g.get("page_title"):
        title = html.escape(g["page_title"], quote=False)
    text = re.sub(r"<title>[^<]*</title>", f"<title>{title} | Santosh Magnetic Works</title>", text)
    text = re.sub(r'(<meta property=og:title content=)"[^"]*"',
                  rf'\1"{title} | Santosh Magnetic Works"', text)
    # JSON-LD breadcrumb: last item carries the page name
    text = re.sub(r'("position":3,"name":")[^"]*(")', rf"\g<1>{g['title']}\g<2>", text, count=1)
    # Eclipse keyword lists add nothing and carry old product names
    text = re.sub(r"<meta name=keywords content=\"[^\"]*\">", "", text)
    if g.get("meta"):
        d = html.escape(g["meta"], quote=True)
        text = re.sub(r'(<meta name=description content=)"[^"]*"', rf'\1"{d}"', text)
        text = re.sub(r'(<meta property=og:description content=)"[^"]*"', rf'\1"{d}"', text)
    return text


TILE_RE = re.compile(
    r'(<div class=grid__item><a href=(/products/[a-z0-9-]+/[a-z0-9-]+/)[^>]*>'
    r'<div class=image>.*?</div><div class=text><h3>)(.*?)(</h3><p>)(.*?)(</div>)', re.S)


def apply_tiles(blurbs: dict[str, tuple[str, str]], dry: bool) -> int:
    n = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")

        def sub(m):
            href = m.group(2)
            if href in blurbs:
                name, blurb = blurbs[href]
                return m.group(1) + name + m.group(4) + blurb + m.group(6)
            return m.group(0)
        new = TILE_RE.sub(sub, text)
        if new != text:
            n += 1
            if not dry:
                page.write_text(new, encoding="utf-8")
    return n


def main() -> None:
    dry = "--dry-run" in sys.argv
    sources = sorted((load(p) for p in SRC.rglob("*.md")), key=lambda g: g["rel"])
    blurbs: dict[str, tuple[str, str]] = {}
    titles: dict[str, str] = {}
    for g in sources:
        if g["type"] == "product":
            titles["/" + g["rel"] + "/"] = g["title"]
    for g in sources:
        if "tiles" in g["sections"]:
            fam = g["rel"].rsplit("/", 1)[0]
            for slug, blurb in tiles(g["sections"]["tiles"]).items():
                href = f"/{fam}/{slug}/"
                blurbs[href] = (html.escape(titles.get(href, slug), quote=False), inline(blurb))
    for g in sources:
        rel = g["rel"]
        page = SITE / (rel[:-len("/index")] if rel.endswith("/index") else rel) / "index.html"
        if not page.exists():
            print(f"  !! no page for {rel}")
            continue
        text = page.read_text(encoding="utf-8")
        if g["type"] == "product":
            new = product(text, g)
        elif g["type"] in ("family", "industry"):
            new = rebuild_main(text, g, g["type"])
        elif g["type"] == "intro":
            new = intro_only(text, g)
        else:
            raise ValueError(g["type"])
        new = head(new, g)
        words = len(re.sub(r"<[^>]+>", " ", new[new.find("<main"):new.find("</main>")]).split())
        print(f"{g['type']:9s} {words:5d} words  {rel}")
        if not dry:
            page.write_text(new, encoding="utf-8")
    print(f"tile blurbs applied on {apply_tiles(blurbs, dry)} pages")
    # sitemap rows carry the current page names
    smap = SITE / "sitemap/index.html"
    text = smap.read_text(encoding="utf-8")
    n = 0
    for g in sources:
        rel = g["rel"][:-len("/index")] if g["rel"].endswith("/index") else g["rel"]
        pat = re.compile(rf"(<a href=/{re.escape(rel)}/>)[^<]*(</a>)")
        text, k = pat.subn(rf"\g<1>{html.escape(g['title'], quote=False)}\g<2>", text)
        n += k
    print(f"sitemap: {n} names updated")
    if not dry:
        smap.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
