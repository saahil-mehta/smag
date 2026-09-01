#!/usr/bin/env python3
"""Author the SMAG product pages the mirror never held.

The mirror's separation listing linked eight detail pages that were never
crawled (bullet, sampling probe, strip, underflow x2, rods, gauss meter,
chute), and the Lifting & Handling family was cleared of the Eclipse range.
This script builds those pages from SMAG's own brochures:

  - copy in the brochure stills kept under assets/source/brochure-stills/
    (chosen and cropped from the PDFs in the client's docs folder)
  - generate web renditions with sips into site/site/assets/images/smag/
  - compose each page from the site's own component classes (same approach
    as refurb_about.py), inside the chrome of a donor product page
  - rebuild the separation index grid in range order with the new tiles,
    give Lifting & Handling its SMAG range, and extend the sitemap

Copy is written fresh from the brochure inventory; the IndiaMART capture
text is AI-written and is deliberately never reused. No prices are shown.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
MIRROR = REPO / "reference-mirror/www.eclipsemagnetics.com"
MASTERS = REPO / "assets/source/brochure-stills"
IMGDIR = SITE / "site/assets/images/smag"
IMGURL = "/site/assets/images/smag"
SEP = "magnetic-separation-and-metal-detection"
LIFT = "lifting-and-handling"
DONOR = SITE / "products" / SEP / "magnetic-grids-for-sieves/index.html"

GRID_OPEN = '<div class="grid grid--product-category">'
TILE_OPEN = "<div class=grid__item>"

# final separation grid order (existing pages by slug, new pages built below)
SEP_ORDER = [
    "housed-easy-clean-grid-magnet-separator",
    "high-intensity-liquid-filter-separator",
    "magnetic-grids-for-sieves",
    "magnetic-separation-grids",
    "easy-clean-magnetic-grid-separator",
    "housed-bullet-magnet",
    "magnetic-sampling-probe",
    "deep-field-magnetic-plate-separator",
    "magnetic-strip-separator",
    "underflow-magnet",
    "magnetic-rods",
    "gauss-meter",
    "housed-underflow-magnetic-separator",
    "chute-separator",
]

RODS_TECH = (
    "<ul><li><strong>Standard strength:</strong> 7,000 to 8,000 gauss"
    "<li><strong>High strength:</strong> 8,000 to 9,000 gauss"
    "<li><strong>Super high strength:</strong> 9,500 to 11,000 gauss"
    "<li><strong>Extreme high strength:</strong> 12,000 to 13,500 gauss"
    "<li><strong>Magnet material:</strong> NdFeB grades N35 and N45; ferrite"
    " (3,000 gauss) and Ferrearth (5,000 gauss) versions available"
    "<li><strong>Tube:</strong> 304 stainless steel, fully welded and"
    " polished, watertight"
    "<li><strong>Standard diameter:</strong> 25.4 mm (1 inch); round, square"
    " and triangle sections; lengths to drawing"
    "<li><strong>Temperature limit:</strong> 100 deg C for rare earth rods"
    "<li>Supplied with a tested certificate of magnetic strength</ul>"
)

LIFTER_ROWS = [
    ("Maxx-100", 100, 15, 50, 300, "92 x 62 x 69", 155, 3),
    ("Maxx-200", 200, 20, 100, 600, "122 x 62 x 69", 155, 4.5),
    ("Maxx-300", 300, 20, 150, 900, "160 x 95 x 95", 200, 9.5),
    ("Maxx-400", 400, 25, 200, 1200, "160 x 95 x 95", 200, 9.5),
    ("Maxx-600", 600, 30, 300, 1800, "210 x 120 x 120", 230, 20),
    ("Maxx-1000", 1000, 40, 500, 3000, "260 x 150 x 140", 255, 40),
    ("Maxx-1500", 1500, 45, 750, 4500, "340 x 150 x 140", 255, 45),
    ("Maxx-2000", 2000, 55, 1000, 6000, "350 x 175 x 175", 320, 60),
    ("Maxx-3000", 3000, 60, 1500, 9000, "440 x 175 x 175", 380, 90),
    ("Maxx-4000", 4000, 75, 2000, 12000, "520 x 175 x 175", 550, 150),
    ("Maxx-5000", 5000, 85, 2500, 15000, "600 x 230 x 215", 600, 230),
    ("Maxx-6000", 6000, 100, 3000, 18000, "600 x 270 x 265", 700, 300),
]


def lifter_table() -> str:
    head = ("<tr><th>Model<th>Flat load (kg)<th>Min job thickness (mm)"
            "<th>Round load (kg)<th>Pull strength (kgf)"
            "<th>L x W x H (mm)<th>Handle (mm)<th>Weight (kg)")
    rows = "".join(
        f"<tr><td>{m}<td>{f}<td>{t}<td>{r}<td>{p}<td>{d}<td>{h}<td>{w}"
        for m, f, t, r, p, d, h, w in LIFTER_ROWS
    )
    return ('<div style="overflow-x:auto"><table>'
            f"<thead>{head}</thead><tbody>{rows}</tbody></table></div>"
            "<p>Every lifter is load tested to three times its safe working"
            " load before dispatch. Round load ratings are half the flat"
            " rating. Maximum job temperature 80 deg C.")


# slug -> page definition
PAGES: dict[str, dict] = {
    "housed-bullet-magnet": dict(
        family=SEP, name="Housed Bullet Magnetic Separator",
        tagline="In-line drawer housing for enclosed transfer lines",
        meta="Flanged in-line magnetic separator with two drawers of "
             "neodymium rods in offset rows, cleaned through a "
             "toggle-clamped access door.",
        bullets=[
            "Two sliding drawers of neodymium rods in offset rows",
            "Round flanged inlet and outlet for in-line fitting",
            "Toggle-clamped access door; drawers pull out for cleaning",
            "Painted mild steel or full stainless steel builds",
            "Sized to the line bore and throughput",
        ],
        overview_h2="Staggered rods across the full bore",
        overview=[
            "Product falls through a staggered lattice of magnetic rods, so "
            "every path through the housing passes close to a magnet face. "
            "Nails, wire, swarf and fine iron hold to the rods while the "
            "product carries on down the line.",
            "Opening the toggle-clamped door and drawing each drawer out "
            "takes the rods clear of the product zone, so captured iron can "
            "be wiped off in seconds. The housing suits gravity and lean "
            "phase pneumatic lines in milling, plastics and chemicals.",
        ],
        tech=RODS_TECH,
        images=[("double-drawer-housing-blue-01",
                 "Housed bullet magnetic separator with access door open and "
                 "both rod drawers part drawn"),
                ("double-drawer-housing-ss-01",
                 "Stainless steel housed magnetic separator with round "
                 "flanges and rod drawers extended")],
        tile="Drawer-mounted magnetic rods in a flanged in-line housing",
    ),
    "magnetic-sampling-probe": dict(
        family=SEP, name="Magnetic Sampling Probe",
        tagline="T-handled probe for checking incoming material",
        meta="Hand-held magnetic probe with a sliding release sleeve for "
             "spot checks on ferrous contamination in bins, sacks and "
             "hoppers.",
        bullets=[
            "Dip tests bins, sacks and hoppers for ferrous fines",
            "Sliding outer sleeve releases the captured iron cleanly",
            "304 stainless steel, sealed and watertight",
            "Neodymium core for high surface strength",
            "Doubles as a simple audit probe for goods inwards",
        ],
        overview_h2="A quick answer on contamination",
        overview=[
            "Push the probe into the material, draw it out and the ferrous "
            "content of the batch is sitting on the sleeve. Sliding the "
            "magnet core out of the sleeve drops the captured iron onto a "
            "tray for inspection or weighing.",
            "Works as a routine goods-inwards check and as a fast way to "
            "trace which stage of a process is shedding metal.",
        ],
        tech=RODS_TECH,
        images=[("magnetic-sampling-rod-01",
                 "Magnetic sampling probe with T-handle and sliding release "
                 "sleeve")],
        tile="T-handled probe for spot checks on incoming material",
    ),
    "magnetic-strip-separator": dict(
        family=SEP, name="Magnetic Strip Separator",
        tagline="Hand-held easy-clean magnet for batch checking",
        meta="Hand-held plate magnet in a stainless easy-release cover for "
             "sweeping tramp iron out of small batches and spot checks.",
        bullets=[
            "Strontium ferrite block in a 304 stainless cover",
            "Release action drops collected iron without scraping",
            "Rectangular and round faces, two sizes",
            "Light enough for one-handed sweeps",
        ],
        overview_h2="Sweep, lift, release",
        overview=[
            "Sweep the face over the material and tramp iron collects on "
            "the cover. Lifting the cover away from the magnet drops the "
            "catch straight into a bin, so hands never touch sharp swarf.",
            "Used for batch checking of raw material in foundries, "
            "plastics, scrap and chemicals, and for clean-up sweeps around "
            "the works.",
        ],
        tech="<ul><li><strong>Magnet:</strong> strontium ferrite"
             "<li><strong>Cover:</strong> 304 stainless steel, easy release"
             "<li><strong>Shapes:</strong> rectangular or round, two sizes"
             "<li><strong>Typical face strength:</strong> about 1,700 gauss"
             "</ul>",
        images=[("hand-magnet-easy-clean-01",
                 "Two sizes of hand-held easy-clean magnetic separator")],
        tile="Hand-held easy-clean magnet for batch checking",
    ),
    "underflow-magnet": dict(
        family=SEP, name="Underflow Magnetic Separator",
        tagline="Plate magnets for open chutes and underflow ducts",
        meta="Plate magnets mounted beneath the product flow on open chutes "
             "and underflow ducts, pulling out large tramp iron.",
        bullets=[
            "Mounts under the product flow on inclined chutes",
            "Removes large tramp iron ahead of finer separation stages",
            "Cast aluminium or stainless encapsulated plate",
            "Sized to the chute width and burden depth",
            "Hinged mountings available for fast cleaning",
        ],
        overview_h2="First line of defence on the chute",
        overview=[
            "An underflow plate sits below the moving product so the "
            "burden passes directly over the magnet face. Bolts, nuts and "
            "tool pieces pull down onto the plate and stay there until the "
            "plate is swung clear and wiped.",
            "Fitted ahead of grids and rod separators, it takes out the "
            "large iron that would otherwise bridge or damage the finer "
            "stages.",
        ],
        tech="<ul><li><strong>Magnet:</strong> anisotropic ferrite; "
             "neodymium builds for deeper reach"
             "<li><strong>Encapsulation:</strong> LM-6 cast aluminium or "
             "SS 304/316"
             "<li><strong>Sizes:</strong> to the chute and duty, made to "
             "drawing</ul>",
        images=[("suspension-magnet-01",
                 "Encapsulated plate magnet with lifting eye bolts")],
        tile="Plate magnets for open chutes and underflow ducts",
    ),
    "magnetic-rods": dict(
        family=SEP, name="Neodymium Magnetic Rod",
        tagline="Sealed separator rods up to 13,500 gauss",
        meta="Fully welded 304 stainless separator rods with neodymium "
             "cores, from 7,000 to 13,500 gauss, singly or built into "
             "grids.",
        bullets=[
            "Strengths from 7,000 to 13,500 gauss by grade",
            "25.4 mm standard diameter; lengths to drawing",
            "Round, square and triangle sections",
            "Watertight 304 stainless, fully welded and polished",
            "Build into grids or fit to an existing filter housing",
        ],
        overview_h2="The building block of every separator",
        overview=[
            "Each rod is a sealed stainless tube holding neodymium magnets "
            "and pole concentrators, machined and welded in our own works. "
            "Rods are supplied singly, assembled with side plates into "
            "grids, or fitted into an existing mechanical filter to form a "
            "combination filter.",
            "Watertight construction suits liquid lines as well as dry "
            "product, across sugar, grain, tea, plastic granulate and "
            "powdered chemicals. Every rod ships with a tested certificate "
            "of magnetic strength.",
        ],
        tech=RODS_TECH,
        images=[("neodymium-magnetic-rod-01",
                 "Neodymium separator rod in a sealed stainless tube"),
                ("magnetic-rod-01",
                 "Stainless cased magnetic rod cartridge")],
        tile="Sealed 304 stainless rods up to 13,500 gauss",
    ),
    "gauss-meter": dict(
        family=SEP, name="Gauss Meter",
        tagline="Verify magnet strength on site",
        meta="Hand-held gauss meter with probe for checking the surface "
             "strength of separator rods, grids and plates in service.",
        bullets=[
            "Reads surface gauss on rods, grids and plates",
            "Confirms separators still meet their rated strength",
            "Supports audit and quality records",
            "Pairs with the tested certificate supplied with our magnets",
        ],
        overview_h2="Proof the magnets still perform",
        overview=[
            "Magnet strength falls if a separator is overheated or "
            "mechanically damaged, and an audit trail needs numbers. A "
            "gauss meter pressed to the rod or plate face gives a direct "
            "reading to log against the tested certificate supplied with "
            "the equipment.",
            "We use the same instruments to certify every separator that "
            "leaves the works, and supply meters to customers who run "
            "their own periodic checks.",
        ],
        tech="<ul><li><strong>Type:</strong> hand-held meter with remote "
             "probe<li><strong>Use:</strong> surface strength checks on "
             "separator rods, grids, plates and chucks"
             "<li><strong>Records:</strong> readings log directly against "
             "the tested certificate supplied with SMAG equipment</ul>",
        images=[("gauss-meter-with-hand",
                 "Hand-held gauss meter with probe")],
        tile="Hand-held meter for verifying magnet strength",
    ),
    "housed-underflow-magnetic-separator": dict(
        family=SEP, name="Housed Underflow Magnetic Separator",
        tagline="Drawer magnets for enclosed underflow ducts",
        meta="Enclosed underflow separator with pull-out drawers of "
             "neodymium rods, built for gravity ducts in milling, plastics "
             "and chemicals.",
        bullets=[
            "Fully enclosed housing keeps dust in and fingers out",
            "Drawers of neodymium rods pull out for cleaning",
            "Flanged to match the duct at inlet and outlet",
            "Painted mild steel or full stainless steel builds",
        ],
        overview_h2="Separation inside the duct",
        overview=[
            "Where the product stream runs inside closed ducting, the "
            "separator has to live in the line itself. This housing bolts "
            "between flanges and presents staggered rows of magnetic rods "
            "to everything passing through.",
            "Cleaning is the same drawer action as our bullet housing: "
            "unclamp the door, draw the rods clear and wipe them down, "
            "with no need to break the duct joints.",
        ],
        tech=RODS_TECH,
        images=[("double-drawer-housing-ss-01",
                 "Stainless steel housed underflow separator with rod "
                 "drawers extended")],
        tile="Drawer magnets for enclosed underflow ducts",
    ),
    "chute-separator": dict(
        family=SEP, name="Chute Magnetic Separator",
        tagline="Deep-reach plate magnets for angled chutes",
        meta="Plate magnets for vertical and inclined chute sections, "
             "encapsulated in aluminium or stainless steel and sized to "
             "the chute.",
        bullets=[
            "Mounts on the inside face of vertical or angled chutes",
            "Deep-reach field pulls iron out of the moving burden",
            "LM-6 cast aluminium or SS 304/316 encapsulation",
            "Hinged easy-clean mountings available",
            "Made to the chute dimensions",
        ],
        overview_h2="Protection where the product already flows",
        overview=[
            "A chute separator uses the chute itself as the process "
            "vessel: the plate bolts to the chute face and works on the "
            "product sliding past. There is nothing to drive and nothing "
            "to maintain beyond a periodic wipe of the plate.",
            "Used across textiles, tea, coffee, chemical and plastics "
            "processing, ahead of mills, sieves and packing lines.",
        ],
        tech="<ul><li><strong>Magnet:</strong> anisotropic ferrite; "
             "neodymium for deeper fields"
             "<li><strong>Encapsulation:</strong> LM-6 cast aluminium or "
             "SS 304/316"
             "<li><strong>Mounting:</strong> bolt-on or hinged easy-clean "
             "frames<li><strong>Sizes:</strong> made to drawing</ul>",
        images=[("magnetic-plate-magnet-01",
                 "Encapsulated plate magnet for chute mounting")],
        tile="Deep-reach plate magnets for angled chutes",
    ),
    "permanent-magnetic-lifter": dict(
        family=LIFT, name="Permanent Magnetic Lifter",
        tagline="Hand-lever lifting magnets, 100 kg to 6,000 kg",
        meta="Maxx series permanent magnetic lifters, twelve models from "
             "100 kg to 6,000 kg, load tested to three times the rated "
             "load.",
        bullets=[
            "Twelve models, Maxx-100 to Maxx-6000",
            "Every unit load tested to 3 times the safe working load",
            "Locking hand lever prevents accidental release",
            "Two-pole face works on flat and round material",
            "Neodymium powered; no electricity, no maintenance",
            "3 year guarantee",
        ],
        overview_h2="One person, one lever, no slings",
        overview=[
            "A Maxx lifter switches on and off with a locking hand lever, "
            "so a single operator can attach a crane or hoist to plate, "
            "block or round bar without slings or clamps. The neodymium "
            "circuit needs no power supply, which removes the drop risk "
            "of an electromagnet mains failure.",
            "Round loads rate at half the flat figure, and every magnet "
            "is tested to lift three times its safe working load before "
            "it leaves the works.",
        ],
        tech=lifter_table(),
        images=[("permanent-magnetic-lifter-01",
                 "Maxx 1000 permanent magnetic lifter, three-quarter view"),
                ("permanent-magnetic-lifter-02",
                 "Maxx 1000 permanent magnetic lifter, side view"),
                ("permanent-magnetic-lifter-03",
                 "Permanent magnetic lifter with rubber handle grip")],
        tile="Hand-lever lifting magnets rated 100 kg to 6,000 kg",
    ),
}

FAMILY_NAMES = {SEP: "Magnetic Separation", LIFT: "Lifting &amp; Handling"}

# The brochure exports carry captions baked into the image near the bottom.
# Captions are painted out (or cropped off) here at build time; the masters
# stay exactly as cut from the PDFs. The small S-MAG corner marks stay: they
# are the works' own brand. Fractions of width/height.
CLEANUP: dict[str, dict] = {
    "double-drawer-housing-blue-01": {"rects": [(0.20, 0.80, 0.90, 0.92)]},
    "double-drawer-housing-ss-01": {"rects": [(0.05, 0.825, 0.95, 0.90)]},
    "hand-magnet-easy-clean-01": {"rects": [(0.46, 0.83, 0.95, 0.92)]},
    "magnetic-sampling-rod-01": {"rects": [(0.0, 0.875, 1.0, 1.0)]},
    "neodymium-magnetic-rod-01": {"crop_bottom": 0.78},
}
WORK = Path("/private/tmp/claude-501/-Users-saahil-Documents-GitHub-smag"
            "/8ffed195-094f-484f-99fa-015540bcc480/scratchpad/img-prep")


def prepared(stem: str) -> Path:
    """Master with baked-in captions painted out, ready for renditions."""
    src = MASTERS / f"{stem}.png"
    ops = CLEANUP.get(stem)
    if not ops:
        return src
    from PIL import Image, ImageDraw
    WORK.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if "crop_bottom" in ops:
        im = im.crop((0, 0, w, int(h * ops["crop_bottom"])))
    for x0, y0, x1, y1 in ops.get("rects", []):
        ImageDraw.Draw(im).rectangle(
            (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)),
            fill=(255, 255, 255))
    dst = WORK / f"{stem}.png"
    im.save(dst)
    return dst


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


# --- watermark -------------------------------------------------------------
# Same treatment as the home category tiles (build_product_tiles.py): the
# S-MAG mark composited bottom-right at 18% opacity, 22% of the image width.
# The mark is rasterised from assets/logo.svg; the raster arrives on an
# opaque white square, so the outer white is removed by edge flood fill (the
# letters inside the capsule are also white and must survive).
LOGO_SVG = REPO / "assets/logo.svg"
LOGO_MARK = REPO / "assets/source/logo-mark.png"
WM_OPACITY = 0.18
WM_WIDTH_FRAC = 0.22


def logo_mark():
    from PIL import Image, ImageDraw
    if not LOGO_MARK.exists():
        WORK.mkdir(parents=True, exist_ok=True)
        for f in WORK.glob("logo.svg.png"):
            f.unlink()
        run(["qlmanage", "-t", "-s", "1024", "-o", str(WORK),
             str(LOGO_SVG)])
        im = Image.open(WORK / "logo.svg.png").convert("RGBA")
        for corner in [(0, 0), (im.width - 1, 0), (0, im.height - 1),
                       (im.width - 1, im.height - 1)]:
            ImageDraw.floodfill(im, corner, (0, 0, 0, 0), thresh=40)
        im = im.crop(im.getbbox())
        im.save(LOGO_MARK)
    return Image.open(LOGO_MARK).convert("RGBA")


def watermark(path: Path) -> None:
    from PIL import Image
    wm = logo_mark()
    base = Image.open(path).convert("RGBA")
    W, H = base.size
    tw = int(W * WM_WIDTH_FRAC)
    th = round(tw * wm.height / wm.width)
    mark = wm.resize((tw, th), Image.LANCZOS)
    mark.putalpha(mark.split()[-1].point(lambda v: int(v * WM_OPACITY)))
    base.alpha_composite(mark, (W - tw - int(W * 0.035),
                                H - th - int(H * 0.055)))
    base.convert("RGB").save(path, "JPEG", quality=87, optimize=True,
                             progressive=True)


def dims(path: Path) -> tuple[int, int]:
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        check=True, capture_output=True, text=True).stdout
    w = int(re.search(r"pixelWidth: (\d+)", out).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", out).group(1))
    return w, h


def renditions(stem: str) -> dict[str, str]:
    """Generate hero/zoom/thumb/tile jpgs for a master; return URLs+dims."""
    src = prepared(stem)
    IMGDIR.mkdir(parents=True, exist_ok=True)
    w, h = dims(src)
    out = {}

    def make(kind: str, ops: list[str]) -> str:
        dst = IMGDIR / f"{stem}.{kind}.jpg"
        run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
             *ops, str(src), "--out", str(dst)])
        if kind != "thumb":  # the mark would be illegible at 160px
            watermark(dst)
        return f"{IMGURL}/{stem}.{kind}.jpg"

    hero_ops = ["--resampleWidth", "590"] if w > 590 else []
    out["hero"] = make("hero", hero_ops)
    hw, hh = dims(IMGDIR / f"{stem}.hero.jpg")
    out["hero_w"], out["hero_h"] = hw, hh
    out["zoom"] = make("zoom", ["--resampleWidth", "1000"] if w > 1000 else [])

    def fit_pad(tw: int, th: int) -> list[str]:
        # scale to fit inside tw x th, then pad to exactly tw x th
        scale = (["--resampleWidth", str(tw)] if w / h > tw / th
                 else ["--resampleHeight", str(th)])
        return scale + ["--padToHeightWidth", str(th), str(tw),
                        "--padColor", "FFFFFF"]

    out["thumb"] = make("thumb", fit_pad(160, 120))
    out["tile"] = make("tile", fit_pad(355, 205))
    return out


def slide(img: dict, alt: str) -> str:
    return (
        '<div class="product__image swiper-slide">'
        '<div class="product-image-wrapper product-zoom" '
        f'data-zoom={img["zoom"]}>'
        f'<img src={img["hero"]} width={img["hero_w"]} '
        f'height={img["hero_h"]} alt="{alt}" /></div>'
        '<p class=zoom-tip><i class="fas fa-search"></i> Hover to zoom</div>'
    )


def thumb(img: dict, n: int) -> str:
    return (f'<a href=# data-img={n}>'
            f'<div style="background-image:url(\'{img["thumb"]}\')">'
            "</div></a>")


def tile_html(fam: str, slug: str, name: str, blurb: str, img: dict,
              alt: str) -> str:
    return (
        "<div class=grid__item>"
        f"<a href=/products/{fam}/{slug}/ class=alt-swap>"
        f'<div class=image><img src={img["tile"]} width=355 height=205 '
        f'alt="{alt}" /></div>'
        f"<div class=text><h3>{name}</h3><p>{blurb}</div>"
        '<span class="button button--large button--full button--with-arrow">'
        "\nExplore product </span></a></div>"
    )


def build_page(slug: str, spec: dict, donor: str, subnav: str,
               imgs: list[dict]) -> str:
    fam, name = spec["family"], spec["name"]
    url = f"/products/{fam}/{slug}/"

    slides = "".join(slide(i, alt) for i, (_, alt) in
                     zip(imgs, spec["images"]))
    thumbs = ""
    if len(imgs) > 1:
        thumbs = ("<div class=product__thumbnails>"
                  + "".join(thumb(i, n + 1) for n, i in enumerate(imgs))
                  + "</div>")
    bullets = "".join(f"<li>{b}" for b in spec["bullets"])
    paras = "".join(f"<p>{p}" for p in spec["overview"])

    main = (
        "<main>"
        + (subnav if fam == SEP else "")
        + '<div class="row row--alt row--x-small-padding">'
          '<div class="row__inner product__top"><div class=product__top-left>'
          '<div class=breadcrumbs><div class=row__inner>'
          "<span>&nbsp;/&nbsp;</span>\n"
          f"<a href=/products/{fam}/>{FAMILY_NAMES[fam]}</a>"
          f"<span>&nbsp;/&nbsp;</span>{name} </div></div>"
          '<div class="product__gallery swiper-container '
          'gallery-swiper-container">'
          f'<div class="product__images swiper-wrapper">{slides}</div>'
          "<button class=prev></button><button class=next></button></div>"
          f"{thumbs}</div>"
          '<div class="product__intro content">'
          f"<h1 class=bordered-header>{name}</h1>"
          f'<p>{spec["tagline"]}<ul>{bullets}</ul>'
          '<div class=c2a><a href=/contact-us/ class="button button--large '
          'button--full button--with-arrow">Get a quote</a></div>'
          "</div></div></div>"
        + '<div class=row><div class="row__inner product__details">'
          '<div class=tabbed-content><div class=horizontal-overflow>'
          "<ul class=tabbed-content__tabs>"
          "<li class=active><a href=# data-target=overview>Overview</a>"
          "<li><a href=# data-target=technical_data>Technical Data</a>"
          "</ul></div><div class=tabbed-content__content>"
          '<div class="tab-item active" id=overview><div class=overview>'
          '<div class="row content">'
          f"<p class=overview-mini-title>Overview - {name} "
          f'<h2>{spec["overview_h2"]}</h2>{paras}</div></div></div>'
          "<div class=tab-item id=technical_data><div class=row>"
          "<h3 class=bordered-header>Technical Data</h3>"
          f'{spec["tech"]}</div></div>'
          "</div></div></div></div>"
        + '<div class="row row--action"><div class=row__inner><h3>'
          "<a href=/contact-us/>\nTell us about the application and we will "
          "come back with a recommendation "
          "<i aria-hidden=true class=icon></i> </a></h3></div></div>"
        + "</main>"
    )

    ms = donor.find("<main")
    me = donor.find("</main>") + len("</main>")
    page = donor[:ms] + main + donor[me:]

    # head swaps: title, descriptions, og:url; donor name in any leftovers
    page = re.sub(r"<title>[^<]*</title>",
                  f"<title>{name} | Santosh Magnetic Works</title>", page)
    page = re.sub(r"(<meta name=description content=)\"[^\"]*\"",
                  rf'\1"{spec["meta"]}"', page)
    page = re.sub(r"(<meta property=og:description content=)\"[^\"]*\"",
                  rf'\1"{spec["meta"]}"', page)
    page = re.sub(r"(<meta property=og:title content=)\"[^\"]*\"",
                  rf'\1"{name} | Santosh Magnetic Works"', page)
    page = re.sub(r"(<meta property=og:url content=)[^>]+>",
                  rf"\1https://santoshmagneticworks.com{url}>", page)
    page = page.replace("Magnetic Grids for Sieves", name)
    return page


def rebuild_grid(index: Path, order: list[str], fam: str,
                 new_tiles: dict[str, str]) -> None:
    text = index.read_text(encoding="utf-8")
    i = text.find(GRID_OPEN)
    end = find_element_end(text, i)
    seg = text[i:end]
    tiles = dict(new_tiles)
    for m in re.finditer(re.escape(TILE_OPEN), seg):
        te = find_element_end(seg, m.start())
        t = seg[m.start():te]
        a = re.search(rf"href=/products/{re.escape(fam)}/([a-z0-9-]+)/", t)
        if a and a.group(1) not in tiles:
            tiles[a.group(1)] = t
    missing = [s for s in order if s not in tiles]
    if missing:
        print(f"  !! grid {fam}: no tile for {missing}")
    body = "".join(tiles[s] for s in order if s in tiles)
    text = text[:i] + GRID_OPEN + body + "</div>" + text[end:]
    index.write_text(text, encoding="utf-8")
    print(f"  grid {fam}: {len(order)} tiles")


def main() -> None:
    dry = "--dry-run" in sys.argv
    donor = DONOR.read_text(encoding="utf-8")
    sm = re.search(r'<div class="row subnav"', donor)
    subnav = donor[sm.start():find_element_end(donor, sm.start())]

    # the gauss meter still comes from the mirror, not the brochures
    gm_src = MIRROR / "site/assets/files/35758/gauss-meter-with-hand.637x481.png"
    if not dry:
        shutil.copy2(gm_src, MASTERS / "gauss-meter-with-hand.png")

    pages_built = []
    new_sep_tiles: dict[str, str] = {}
    new_lift_tiles: dict[str, str] = {}
    for slug, spec in PAGES.items():
        fam = spec["family"]
        print(f"build {fam}/{slug}/")
        if dry:
            continue
        imgs = [renditions(stem) for stem, _ in spec["images"]]
        page = build_page(slug, spec, donor, subnav, imgs)
        d = SITE / "products" / fam / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page, encoding="utf-8")
        t = tile_html(fam, slug, spec["name"], spec["tile"], imgs[0],
                      spec["images"][0][1])
        (new_sep_tiles if fam == SEP else new_lift_tiles)[slug] = t
        pages_built.append(slug)

    if not dry:
        rebuild_grid(SITE / "products" / SEP / "index.html",
                     SEP_ORDER, SEP, new_sep_tiles)
        rebuild_grid(SITE / "products" / LIFT / "index.html",
                     ["permanent-magnetic-lifter"], LIFT, new_lift_tiles)

        # sitemap: lifter entry under Lifting & Handling
        smap = SITE / "sitemap/index.html"
        text = smap.read_text(encoding="utf-8")
        li = ('<li class=no-child>&raquo; <a href=/products/'
              'lifting-and-handling/permanent-magnetic-lifter/>'
              "Permanent Magnetic Lifter</a>")
        if li not in text:
            m = re.search(
                r"<li>&raquo; <a href=/products/lifting-and-handling/>"
                r"[^<]*</a><ul>", text)
            if m:
                text = text[:m.end()] + li + text[m.end():]
                smap.write_text(text, encoding="utf-8")
                print("sitemap: lifter entry added")

    print(f"pages built: {len(pages_built)}")


if __name__ == "__main__":
    main()
