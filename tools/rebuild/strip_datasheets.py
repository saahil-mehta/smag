#!/usr/bin/env python3
"""Replace Eclipse datasheet downloads with SMAG data on the page.

Every "Download datasheet" style link pointed at an Eclipse PDF (all now
deleted by remove_eclipse_pages.py). This script:

  1. removes every remaining link to a non-SMAG PDF, taking its c2a wrapper
     or list row with it (a bare in-prose link is unwrapped)
  2. rewrites each product page's Technical Data tab with the figures from
     SMAG's own brochures (assets/source/inventory-*.md is the source;
     where sources conflicted the printed SMAG brochure wins, per client);
     pages with no brochure data get a made-to-order note instead
  3. rebuilds /brochures/ as a plain list of SMAG's own printed brochures
     (hosted under /site/assets/files/smag/), dropping the Eclipse list and
     its checkbox download flow
  4. adds the neoLIFT brochure as the datasheet on the lifter product page

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
SMAG_PDF = "/site/assets/files/smag/"

RODS_TECH = (
    "<ul><li><strong>Standard strength:</strong> 7,000 to 8,000 gauss"
    "<li><strong>High strength:</strong> 8,000 to 9,000 gauss"
    "<li><strong>Super high strength:</strong> 9,500 to 11,000 gauss"
    "<li><strong>Extreme high strength:</strong> 12,000 to 13,500 gauss"
    "<li><strong>Magnet material:</strong> NdFeB grades N35 and N45; ferrite"
    " (3,000 gauss) and Ferrearth (5,000 gauss) versions available"
    "<li><strong>Tube:</strong> 304 stainless steel, fully welded and"
    " polished, watertight"
    "<li><strong>Standard rod diameter:</strong> 25.4 mm (1 inch); round,"
    " square and triangle sections; lengths to drawing"
    "<li><strong>Temperature limit:</strong> 100 deg C for rare earth rods"
    "<li>Supplied with a tested certificate of magnetic strength</ul>"
)

GENERIC_TECH = (
    "<p>Built to order at our Mumbai works, with dimensions, connection"
    " sizes and magnetic strengths matched to your line. Every unit ships"
    " with a tested certificate of magnetic strength."
    "<p><a href=/contact-us/>Ask us for the specification sheet</a> for"
    " your duty."
)

# product page path -> technical data tab content
TECH: dict[str, str] = {
    "products/magnetic-separation-and-metal-detection/magnetic-grids-for-sieves":
        RODS_TECH,
    "products/magnetic-separation-and-metal-detection/magnetic-separation-grids":
        "<ul><li><strong>Square grids:</strong> 6 x 6, 8 x 8 and"
        " 12 x 12 inch ex stock; specials to drawing"
        "<li><strong>Round grids:</strong> 10, 12, 15 and 24 inch and"
        " 350 mm diameters ex stock"
        "<li><strong>Frame:</strong> 304 stainless steel, welded and"
        " polished; one-stage and two-stage lattices"
        "<li><strong>Magnets:</strong> NdFeB grades N35 to N52, up to"
        " 11,000 gauss at the rod surface; ferrite versions available"
        "<li><strong>Temperature limit:</strong> 100 deg C for rare earth"
        " rods<li>Supplied with a tested certificate of magnetic strength"
        "</ul>",
    "products/magnetic-separation-and-metal-detection/easy-clean-magnetic-grid-separator":
        "<ul><li><strong>Construction:</strong> 304 stainless steel"
        " throughout, welded and polished"
        "<li><strong>Cores:</strong> NdFeB rods inside outer stainless"
        " tubes, two-stage lattice"
        "<li><strong>Cleaning:</strong> toggle-clamp quick release lifts"
        " the magnet frame clear of the tubes"
        "<li><strong>Mounting:</strong> flanged square frame, drilled to"
        " suit the hopper<li><strong>Sizes:</strong> to drawing</ul>",
    "products/magnetic-separation-and-metal-detection/housed-easy-clean-grid-magnet-separator":
        "<ul><li><strong>Housing:</strong> 304 stainless steel, polished,"
        " fully sealed between inlet hood and outlet cone"
        "<li><strong>Magnets:</strong> NdFeB separator rods, 7,000 to"
        " 13,500 gauss by grade"
        "<li><strong>Cleaning:</strong> rod assembly withdraws from the"
        " housing<li><strong>Sizes:</strong> built to the hopper or line"
        " dimensions<li>Supplied with a tested certificate of magnetic"
        " strength</ul>",
    "products/magnetic-separation-and-metal-detection/high-intensity-liquid-filter-separator":
        "<ul><li><strong>In-line trap:</strong> 75 mm prong diameter x"
        " 250 mm, 7 magnetic bars"
        "<li><strong>Housed trap:</strong> 150 mm prong diameter x 250 mm,"
        " 9 magnetic bars"
        "<li><strong>Magnets:</strong> neodymium bars, watertight 304"
        " stainless sheaths"
        "<li><strong>Connections:</strong> flanged; single wall and double"
        " wall (jacketed) builds<li><strong>Duties:</strong> lubricants,"
        " coolants, hydraulic oils, slurries, liquid chemicals and liquid"
        " food products</ul>",
    "products/magnetic-separation-and-metal-detection/deep-field-magnetic-plate-separator":
        "<ul><li><strong>Magnets:</strong> anisotropic ferrite (ceramic);"
        " neodymium builds for deeper fields"
        "<li><strong>Encapsulation:</strong> LM-6 cast aluminium or"
        " SS 304/316"
        "<li><strong>Sizes:</strong> a range of plate sizes and magnetic"
        " depths, made to drawing"
        "<li><strong>Mounting:</strong> over chutes and conveyors; hinged"
        " easy-clean frames on request</ul>",
    "products/filtration-systems/filtramag": GENERIC_TECH,
    "products/oil-and-gas-pipeline-filtration/filtramag-xt": GENERIC_TECH,
    "products/oil-and-gas-pipeline-filtration/ultrafiltrex": GENERIC_TECH,
    "products/workholding-systems/rectangular-premier-chuck":
        "<ul><li><strong>Magnets:</strong> N35 grade neodymium, permanent"
        " (no power supply)"
        "<li><strong>Pole pitch:</strong> close and standard options"
        "<li><strong>Body:</strong> corrosion resistant; sizes to your"
        " grinder table<li>Electromagnetic and multicoil electromagnetic"
        " builds to customer sizes</ul>",
    "products/workholding-systems/rectangular-universal-chuck":
        "<ul><li><strong>Magnets:</strong> permanent neodymium, transverse"
        " pole arrangement"
        "<li><strong>Sizes:</strong> to your machine table, made to order"
        "<li>Electromagnetic builds available to customer sizes</ul>",
    "products/workholding-systems/circular-premier-chuck":
        "<ul><li><strong>Diameters:</strong> up to 600 mm"
        "<li><strong>Poles:</strong> concentric; close and standard pitch"
        " options<li><strong>Magnets:</strong> N35 grade neodymium,"
        " permanent<li>Operated by T-key; no power supply</ul>",
    "products/workholding-systems/circular-universal-chuck":
        "<ul><li><strong>Diameters:</strong> up to 600 mm"
        "<li><strong>Poles:</strong> radial, for turning and rotary"
        " grinding<li><strong>Magnets:</strong> permanent neodymium"
        "<li>Electromagnetic builds available to customer sizes</ul>",
    "products/workholding-systems/table-top-demagnetiser":
        "<ul><li><strong>Model:</strong> Maxx-Demag bench unit"
        "<li><strong>Plate size:</strong> 150 x 100 mm"
        "<li><strong>Supply:</strong> 230 V AC, single phase, 50 Hz"
        "<li>Larger surface demagnetisers built to order</ul>",
    "products/magnetic-tools-and-standard-magnets/magnetic-sweeper":
        "<ul><li><strong>Sweeping widths:</strong> 12 inch and 24 inch"
        " standard; wider builds to order"
        "<li><strong>Release:</strong> quick-release lever drops the"
        " collected metal<li><strong>Handle:</strong> 4 to 5 ft"
        "<li><strong>Frame:</strong> steel or aluminium, on rubber wheels"
        "</ul>",
    "products/magnetic-tools-and-standard-magnets/alnico-power-magnets":
        "<ul><li><strong>Material:</strong> cast alnico"
        "<li><strong>Form:</strong> cylindrical pot with central threaded"
        " hole, red painted finish"
        "<li><strong>Sizes:</strong> from 5 mm diameter; custom diameters"
        " and heights to order"
        "<li>Holds its strength at high temperatures and gives a very"
        " stable field</ul>",
    "products/magnetic-tools-and-standard-magnets/neodymium-block-magnets":
        "<ul><li><strong>Grades:</strong> N35 to N52"
        "<li><strong>Plating:</strong> nickel-copper-nickel"
        "<li><strong>Tolerance:</strong> +/-0.05 mm"
        "<li><strong>Maximum working temperature:</strong> 80 deg C"
        "<li>Custom shapes and sizes made to order</ul>",
    "products/magnetic-tools-and-standard-magnets/neodymium-disc-magnets":
        "<ul><li><strong>Grades:</strong> N35 to N52"
        "<li><strong>Example size:</strong> 4 to 10 mm diameter x 2 mm"
        " thick<li><strong>Plating:</strong> nickel-copper-nickel"
        "<li><strong>Maximum working temperature:</strong> 80 deg C"
        "<li>Custom shapes and sizes made to order</ul>",
    "products/magnetic-tools-and-standard-magnets/neodymium-channel-magnet":
        "<ul><li><strong>Grades:</strong> N35 to N52"
        "<li><strong>Plating:</strong> nickel-copper-nickel"
        "<li><strong>Maximum working temperature:</strong> 80 deg C"
        "<li>Channel bodies sized to order</ul>",
    "products/magnetic-tools-and-standard-magnets/alnico-shallow-pot-magnets":
        "<ul><li><strong>Example size:</strong> 25 mm diameter x 8 mm"
        " thick<li><strong>Build:</strong> magnet set in a steel cup that"
        " concentrates the field on the working face"
        "<li><strong>Fittings:</strong> plain, threaded or hook"
        "<li>Custom diameters and heights on request</ul>",
    "products/magnetic-tools-and-standard-magnets/alnico-deep-pot-magnets":
        "<ul><li><strong>Build:</strong> deep steel shell for a longer"
        " reach and higher pull"
        "<li><strong>Fittings:</strong> plain, threaded or hook"
        "<li>Custom diameters and heights on request</ul>",
}

BROCHURES = [
    ("Magnetic Rods &amp; Grills",
     "Separator rods, round and square grills, housings and the Maxx-Clean"
     " easy-clean range, with sizes and gauss ratings.",
     "smag-magnetic-rods-and-grills.pdf"),
    ("neoLIFT Magnetic Lifters",
     "The Maxx series permanent magnetic lifters, twelve models from 100 kg"
     " to 6,000 kg with the full specification table.",
     "smag-neolift-magnetic-lifters.pdf"),
    ("Maxx-Clean Rare Earth Range",
     "Rare earth separator equipment: magnet grades, strengths and"
     " construction standards.",
     "smag-maxx-clean-rare-earth.pdf"),
]

LIFTER_PAGE = "products/lifting-and-handling/permanent-magnetic-lifter"

PDF_A_RE = re.compile(r'<a\s[^>]*href="?[^">\s]*\.pdf"?[^>]*>')


def strip_pdf_links(text: str) -> tuple[str, int]:
    n = 0
    while True:
        hit = None
        for m in PDF_A_RE.finditer(text):
            if SMAG_PDF in m.group(0):
                continue
            hit = m
            break
        if hit is None:
            return text, n
        # innermost c2a div, p or li wrapping the link
        best = None
        for cre in [re.compile(r"<div class=c2a>"), re.compile(r"<p\b[^>]*>"),
                    re.compile(r"<li\b[^>]*>")]:
            for c in cre.finditer(text, 0, hit.start()):
                end = find_element_end(text, c.start())
                if end and c.start() < hit.start() < end:
                    span = end - c.start()
                    if best is None or span < best[2]:
                        best = (c.start(), end, span)
        # a c2a/li wrapper holding just the link goes entirely; a paragraph
        # goes only if the link is essentially its whole content
        if best:
            inner = text[best[0]:best[1]]
            bare = re.sub(r"<[^>]+>", "", inner)
            link_text = ""
            a_end = find_element_end(text, hit.start())
            if a_end:
                link_text = re.sub(r"<[^>]+>", "",
                                   text[hit.end():a_end - 4])
            if len(bare.strip()) <= len(link_text.strip()) + 24:
                text = text[:best[0]] + text[best[1]:]
                n += 1
                continue
        a_end = find_element_end(text, hit.start())
        if a_end:
            text = (text[:hit.start()] + text[hit.end():a_end - 4]
                    + text[a_end:])
        else:
            text = text[:hit.start()] + text[hit.end():]
        n += 1


def set_tech_tab(text: str, content: str) -> str | None:
    """Rewrite the Technical Data tab; fall back to the Models tab, which on
    the workholding and tools pages carries Eclipse's model tables."""
    for tab_id in ("technical_data", "models"):
        m = re.search(rf"<div class=tab-item id={tab_id}>", text)
        if not m:
            continue
        end = find_element_end(text, m.start())
        block = (f"<div class=tab-item id={tab_id}><div class=row>"
                 "<h3 class=bordered-header>Technical Data</h3>"
                 f"{content}</div></div>")
        text = text[:m.start()] + block + text[end:]
        return re.sub(rf"(data-target={tab_id}>)[^<]+<",
                      r"\1Technical Data<", text)
    return None


def rebuild_brochures(dry: bool) -> None:
    page = SITE / "brochures/index.html"
    text = page.read_text(encoding="utf-8")

    items = "".join(
        "<div class=grid__item><div class=brochure>"
        f"<h4>{name}</h4><p>{desc}"
        f'<div class=c2a><a href={SMAG_PDF}{pdf} '
        'class="button button--large button--with-arrow">Download PDF</a>'
        "</div></div></div>"
        for name, desc, pdf in BROCHURES
    )
    m = re.search(r'<div class="grid grid--brochure-list">', text)
    end = find_element_end(text, m.start())
    text = (text[:m.start()]
            + '<div class="grid grid--brochure-list">' + items + "</div>"
            + text[end:])

    # drop the checkbox flow chrome
    text = text.replace(
        "Please select the brochure(s) you’d like to download",
        "Our printed brochures, straight from the works")
    tp = re.search(r"<div class=thankyou-panel>", text)
    if tp:
        tend = find_element_end(text, tp.start())
        text = text[:tp.start()] + text[tend:]
    print(f"brochures page: {len(BROCHURES)} SMAG brochures listed")
    if not dry:
        page.write_text(text, encoding="utf-8")


def main() -> None:
    dry = "--dry-run" in sys.argv
    stripped = tabs = fallbacks = 0

    for page in sorted(SITE.rglob("*.html")):
        rel = str(page.parent.relative_to(SITE))
        text = orig = page.read_text(encoding="utf-8")
        text, n = strip_pdf_links(text)
        stripped += n

        if rel in TECH:
            new = set_tech_tab(text, TECH[rel])
            if new:
                text = new
                tabs += 1
        elif "<div class=tab-item id=technical_data>" in text:
            m = re.search(r"<div class=tab-item id=technical_data>", text)
            end = find_element_end(text, m.start())
            bare = re.sub(r"<[^>]+>", " ", text[m.start():end])
            bare = bare.replace("Technical Data", "").strip()
            if len(bare) < 60:
                text = set_tech_tab(text, GENERIC_TECH)
                fallbacks += 1

        if text != orig:
            if n:
                print(f"  {n} pdf links stripped: {page.relative_to(SITE)}")
            if not dry:
                page.write_text(text, encoding="utf-8")

    rebuild_brochures(dry)

    # neoLIFT brochure as the lifter datasheet
    page = SITE / LIFTER_PAGE / "index.html"
    text = page.read_text(encoding="utf-8")
    ds = (f"<div class=c2a><a href={SMAG_PDF}smag-neolift-magnetic-lifters.pdf>"
          "Download datasheet</a></div>")
    if ds not in text:
        text = text.replace(
            '<div class=c2a><a href=/contact-us/ class="button button--large '
            'button--full button--with-arrow">Get a quote</a></div>',
            ds + '<div class=c2a><a href=/contact-us/ class="button '
            'button--large button--full button--with-arrow">Get a quote</a>'
            "</div>", 1)
        print("lifter page: neoLIFT datasheet link added")
        if not dry:
            page.write_text(text, encoding="utf-8")

    print(f"pdf links stripped: {stripped}, tech tabs written: {tabs}, "
          f"generic tabs: {fallbacks}")


if __name__ == "__main__":
    main()
