#!/usr/bin/env python3
"""Copy and metadata fixes from the September content audit.

Each fix is an exact string swap applied to the page and, where the copy has
a source (markdown under assets/source/ or an earlier rebuild script), to that
source too, so a re-render does not bring the old wording back. A swap whose
old text is missing everywhere is reported, so a stale entry cannot pass
silently.

Also here, because they are structural:
- the brochures page loses its "Select All" checkbox and the Download button,
  which drove checkboxes that do not exist and was permanently disabled;
- the sitemap page loses the Webinars stub and the four workholding and
  gauss meter entries repeated under Stock Magnets, and gains Brochures and
  the two policies;
- the sweeper's related product is a pot magnet in place of a grinding chuck;
- pages with no meta description get one.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fill_industry_products import catalogue_cards, grid_span  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
DRY = "--dry-run" in sys.argv

WORKHOLDING_MD = "assets/source/pages/products/workholding-systems/index.md"
STAINLESS_MD = "assets/source/guides/are-all-stainless-steels-magnetic.md"
HOME_TITLE = "Magnetic Separation, Filtration, Lifting and Workholding | Santosh Magnetic Works"
HOME_DESC = ("Magnetic separators, filters, lifters, chucks and stock magnets, designed, "
             "machined and tested at our works in Mumbai since 1978.")
POT_CTA = ("<div class=c2a><p><a href=/contact-us/ class=button>"
           "Want to discuss this in more detail? Get in touch</a></div>")

# (files, old, new). Files are relative to the repo.
SWAPS = [
    (["site/index.html"],
     'og:title content="100 Years of Innovation in Magnetic Technology | Santosh Magnetic Works"',
     f'og:title content="{HOME_TITLE}"'),
    (["site/index.html"],
     ("Leading manufacturer and supplier of magnets and magnetic equipment, including industrial "
      "filters, magnetic separators, metal detectors and magnetic assemblies."),
     HOME_DESC),
    (["site/resources/guides/index.html"],
     'og:title content="Free Resource Centre - Magnetic Solutions | Santosh Magnetic Works"',
     'og:title content="Guides | Santosh Magnetic Works"'),
    (["site/index.html"],
     "<p class=title>4 <span></span><p class=text>Product lines: separation, filtration, lifting, workholding ",
     ("<p class=title>6 <span></span><p class=text>Product families: separation, filtration, "
      "pipeline filtration, lifting, workholding and stock magnets ")),
    (["site/index.html"],
     "People working in engineering and a plane in a hanger",
     "Engineers at work beside an aircraft in a hangar"),
    # One name per product: the product pages say grids.
    (["site/index.html", "tools/rebuild/wire_product_tiles.py"], "Magnetic Grills", "Magnetic Grids"),
    (["site/index.html", "tools/rebuild/wire_product_tiles.py"],
     "Hopper and chute grills", "Hopper and chute grids"),
    (["site/index.html"], "Hopper magnetic grill with magnetic tubes", "Hopper magnetic grid with magnetic tubes"),
    (["site/products/workholding-systems/index.html", WORKHOLDING_MD],
     "Hold the work with a lever, not a clamp", "Hold the work with one lever"),
    # The guide goes on to describe all five, four of them magnetic.
    (["site/resources/guides/are-all-stainless-steels-magnetic/index.html", STAINLESS_MD],
     "There are five families. Three of them matter for magnets.", "There are five families."),
    (["site/information/privacy-policy/index.html", "tools/rebuild/write_policies.py"],
     "work-holding", "workholding"),
    (["site/information/privacy-policy/index.html", "tools/rebuild/write_policies.py"],
     "<li>Couriers and transporters, to deliver your order.</li>",
     ("<li>Web3Forms, which passes the enquiry form on our contact page to our email.</li>\n"
      "<li>Couriers and transporters, to deliver your order.</li>")),
    (["site/products/magnetic-tools-and-standard-magnets/alnico-shallow-pot-magnets/index.html"],
     "<div class=c2a><p>Want to discuss this in more detail? Get in touch</div>", POT_CTA),
    (["site/sitemap/index.html"], "<title>Sitemap</title>", "<title>Sitemap | Santosh Magnetic Works</title>"),
]

DESCRIPTIONS = {
    "brochures/index.html": ("Download our printed brochures as PDF files: magnetic rods and grids, "
                             "Maxx magnetic lifters and the Maxx-Clean rare earth range."),
    "contact-us/index.html": ("Contact Santosh Magnetic Works in Dahisar East, Mumbai. Call, WhatsApp "
                              "or email us, or send an enquiry about your application."),
    "information/cookie-policy/index.html": "How the Santosh Magnetic Works website uses cookies.",
    "information/privacy-policy/index.html": ("How Santosh Magnetic Works collects, uses and protects "
                                              "your personal data."),
    "sitemap/index.html": "Every page on the Santosh Magnetic Works website.",
    "404.html": "The page you asked for is not on the Santosh Magnetic Works website.",
}

SITEMAP_STOCK_DUPES = [
    "<li class=no-child>&raquo; <a href=/products/workholding-systems/table-top-demagnetiser/>Table Top Demagnetiser</a>",
    "<li class=no-child>&raquo; <a href=/products/workholding-systems/rectangular-premier-chuck/>Rectangular Premier Chuck</a>",
    "<li class=no-child>&raquo; <a href=/products/workholding-systems/circular-premier-chuck/>Circular Premier Chuck</a>",
    ("<li class=no-child>&raquo; <a href=/products/magnetic-separation-and-metal-detection/gauss-meter/>"
     "Gauss Meter</a>"),
]
SITEMAP_COMPANY_OLD = "<ul><li class=no-child>&raquo; <a href=/company/about-us/>About Us</a></ul>"
SITEMAP_COMPANY_NEW = ("<ul><li class=no-child>&raquo; <a href=/company/about-us/>About Us</a>"
                       "<li class=no-child>&raquo; <a href=/brochures/>Brochures</a>"
                       "<li class=no-child>&raquo; <a href=/information/privacy-policy/>Privacy Policy</a>"
                       "<li class=no-child>&raquo; <a href=/information/cookie-policy/>Cookie Policy</a></ul>")


def swap_all(files: dict[Path, str]) -> list[str]:
    problems = []
    for rels, old, new in SWAPS:
        hit = False
        for rel in rels:
            p = REPO / rel
            s = files.setdefault(p, p.read_text(encoding="utf-8"))
            # Done when new is present and old is gone, or when old lives
            # inside new (the Web3Forms line), where old never goes away.
            if new in s and (old not in s or old in new):
                continue
            if old in s:
                files[p] = s.replace(old, new)
                hit = True
            else:
                problems.append(f"{rel}: text not found: {old[:60]!r}")
        print(f"  {'swapped' if hit else 'already '} {old[:64]!r}")
    return problems


def brochures(s: str) -> str:
    s = re.sub(r'<label class="checkbox-label label-right"> <input id=selectAll type=checkbox>\s*'
               r"Select All Brochures </label>", "", s)
    s = re.sub(r"<div class=brochure__button-container><div class=\"brochure__button-wrap disabled\">"
               r"<input type=submit class=\"button button--download\" value=Download disabled></div></div>", "", s)
    return re.sub(r"<script>\$\('#selectAll'\).*?</script>", "", s, flags=re.S)


def sitemap(s: str) -> str:
    stock = s.find(">Stock Magnets and Tools</a><ul>")
    end = s.find("</ul>", stock)
    block = s[stock:end]
    for dupe in SITEMAP_STOCK_DUPES:
        block = block.replace(dupe, "")
    s = s[:stock] + block + s[end:]
    s = s.replace("<li>&raquo; Webinars</a>", "")
    return s.replace(SITEMAP_COMPANY_OLD, SITEMAP_COMPANY_NEW)


def sweeper_related(s: str) -> str:
    card = catalogue_cards()["magnetic-tools-and-standard-magnets/alnico-deep-pot-magnets"]
    i = s.find("<h3 class=bordered-header>Related Products</h3>")
    g = s.find('<div class="grid grid--product-category">', i)
    a, b = grid_span(s, g)
    return s[:a] + '<div class="grid grid--product-category">' + card + "</div>" + s[b:]


def describe(s: str, desc: str) -> str:
    if "<meta name=description" in s:
        return s
    tags = f'<meta name=description content="{desc}">'
    if "og:title" in s and "og:description" not in s:
        tags += f'<meta property=og:description content="{desc}">'
    return re.sub(r"(</title>)", r"\1" + tags.replace("\\", r"\\"), s, count=1)


def main() -> int:
    files: dict[Path, str] = {}
    problems = swap_all(files)

    structural = {
        SITE / "brochures/index.html": brochures,
        SITE / "sitemap/index.html": sitemap,
        SITE / "products/magnetic-tools-and-standard-magnets/magnetic-sweeper/index.html": sweeper_related,
    }
    for p, fn in structural.items():
        s = files.setdefault(p, p.read_text(encoding="utf-8"))
        files[p] = fn(s)
        print(f"  rebuilt  {p.relative_to(SITE)}" + ("" if files[p] != s else " (unchanged)"))

    for rel, desc in DESCRIPTIONS.items():
        p = SITE / rel
        s = files.setdefault(p, p.read_text(encoding="utf-8"))
        files[p] = describe(s, desc)
        print(f"  describe {rel}" + ("" if files[p] != s else " (unchanged)"))

    for p, s in files.items():
        if not DRY and s != p.read_text(encoding="utf-8"):
            p.write_text(s, encoding="utf-8")
    for line in problems:
        print("  PROBLEM", line)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
