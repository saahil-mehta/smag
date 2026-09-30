#!/usr/bin/env python3
"""Repair navigation and metadata faults found in the September polish pass.

1. Visible breadcrumbs opened with a bare "/". The mirror's first crumb was
   <a href=/en-gb/>Home</a>; /en-gb/ does not exist here, so the dead-link
   scrub removed the link and left its separator. Put Home back.
2. BreadcrumbList JSON-LD still carried the mirror's root ("Sites" at /home/,
   which does not exist), and the product pages cloned from the Grids for
   Sieves template all pointed their last crumb at that page's URL, with the
   lifter filed under Magnetic Separation. Rebuild each list from the visible
   breadcrumb and the page's own path.
3. The family pages' "Products" subnav link targets #products, which no
   element carried. The theme's smooth-scroll handler then threw on
   $(target).offset().top and the click did nothing. The id goes on the row
   that holds the product grid.
4. "Download FREE Brochures" is the mirror's sales wording. The page, its
   title and the footer link become "Brochures".
5. No page had a canonical link. Each gets one matching its og:url.
6. On the home hero the inactive slider dots were black at 20% over dark
   video, so only the active dot showed. They become white at 60%.
7. The #products jump landed under the sticky header and subnav. The theme's
   scroll handler now subtracts them (javascript.js) and scroll-margin-top
   covers the sticky clone, whose links jump natively.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
CSS = SITE / "site/assets/pwpc/pwpc-fb9a7d5e6ed970114ca5fe0828946bafa8c73ab0.css"
ORIGIN = "https://santoshmagneticworks.com"
DRY = "--dry-run" in sys.argv

BC_OPEN = "<div class=breadcrumbs><div class=row__inner><span>&nbsp;/&nbsp;</span>"
BC_HOME = "<div class=breadcrumbs><div class=row__inner><a href=/>Home</a><span>&nbsp;/&nbsp;</span>"
LD_RE = re.compile(r'(<script type="?application/ld\+json"?>)(.*?)(</script>)', re.S)

MARKER = "/* smag: home slider dots */"
RULES = (f"\n{MARKER}\n"
         ".home .home-banner__container .swiper-pagination-bullet{background:#fff;opacity:.6}\n"
         ".home .home-banner__container .swiper-pagination-bullet-active{background:#E20026;opacity:1}\n"
         # The sticky header clone's subnav links are unbound and jump natively.
         "#products{scroll-margin-top:170px}\n")


def page_url(f: Path) -> str:
    rel = f.parent.relative_to(SITE).as_posix()
    return "/" if rel == "." else f"/{rel}/"


def visible_crumbs(s: str, own: str) -> list[tuple[str, str]] | None:
    m = re.search(r"<div class=breadcrumbs><div class=row__inner>(.*?)</div>", s, re.S)
    if not m:
        return None
    parts = [p.strip() for p in m.group(1).split("<span>&nbsp;/&nbsp;</span>")]
    crumbs = []
    for p in parts:
        a = re.fullmatch(r'<a href=["]?([^" >]+)["]?>(.*?)</a>', p, re.S)
        if a:
            crumbs.append((html.unescape(a.group(2).strip()), a.group(1)))
        elif p:
            crumbs.append((html.unescape(re.sub(r"\s+", " ", p)), own))
    return crumbs


def fix_ld(s: str, crumbs: list[tuple[str, str]]) -> tuple[str, bool]:
    changed = False

    def repl(m: re.Match) -> str:
        nonlocal changed
        try:
            data = json.loads(m.group(2))
        except json.JSONDecodeError:
            return m.group(0)
        nodes = data.get("@graph", [data]) if isinstance(data, dict) else data
        here = False
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                new = [{"@type": "ListItem", "position": i + 1, "name": name, "item": ORIGIN + url}
                       for i, (name, url) in enumerate(crumbs)]
                if node.get("itemListElement") != new:
                    node["itemListElement"] = new
                    here = True
        if not here:
            return m.group(0)
        changed = True
        body = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
        return m.group(1) + body + m.group(3)

    return LD_RE.sub(repl, s), changed


def main() -> int:
    counts = dict(home=0, ld=0, anchor=0, brochures=0, canonical=0)
    for f in sorted(SITE.rglob("*.html")):
        s = orig = f.read_text(encoding="utf-8")
        own = page_url(f)

        if BC_OPEN in s:
            s = s.replace(BC_OPEN, BC_HOME, 1)
            counts["home"] += 1

        crumbs = visible_crumbs(s, own)
        if crumbs and crumbs[0][1] == "/":
            s, changed = fix_ld(s, crumbs)
            counts["ld"] += changed

        if "href=#products class=internal" in s and "id=products" not in s:
            g = s.find('class="grid grid--product-category"')
            r = s.rfind('<div class="row row--alt">', 0, g)
            if g < 0 or r < 0:
                raise SystemExit(f"no product grid row in {f}")
            s = s[:r] + '<div class="row row--alt" id=products>' + s[r + len('<div class="row row--alt">'):]
            counts["anchor"] += 1

        if "Download FREE Brochures" in s:
            s = s.replace("Download FREE Brochures", "Brochures")
            counts["brochures"] += 1

        # 404.html is cut from the contact page and keeps its og:url.
        og = re.search(r"<meta property=og:url content=([^ >]+)>", s)
        if og and "rel=canonical" not in s and f.name != "404.html":
            s = s.replace(og.group(0), f"<link rel=canonical href={og.group(1)}>\n{og.group(0)}", 1)
            counts["canonical"] += 1

        if s != orig and not DRY:
            f.write_text(s, encoding="utf-8")

    for k, v in counts.items():
        print(f"  {k:10s} {v} pages")

    css = CSS.read_text(encoding="utf-8")
    if MARKER not in css:
        print("  slider dot rule appended")
        if not DRY:
            CSS.write_text(css + RULES, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
