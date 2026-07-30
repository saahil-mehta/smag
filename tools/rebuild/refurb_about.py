#!/usr/bin/env python3
"""Rebuild the About Us page for SMAG.

Replaces Eclipse's 100-year history, five UK directors, ISO 14001 and ATEX
accreditations, and an empty case-studies carousel left over from the earlier
section removal.

Copy is taken from SMAG's own pre-takedown about-us.html (commit 6e952db^)
rather than invented: the workshop-control story, the three-step specification
process, and Rahul Ingle (CEO) / Sushil Ingle (COO). Statistics use only
verified facts: founded 1978, ISO 9001:2015, and the 4.7/5 from 23 reviews
recorded in docs/superpowers/specs/2026-06-16-smag-content-redesign.md.

Everything is built from the mirror's own components (image-text-pair,
statistics__item, team__item, grid__item) so no new CSS is needed.
"""
from __future__ import annotations

import re
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
PAGE = SITE / "company/about-us/index.html"
IMG = "/site/assets/images"

BANNER = (
    "<picture> "
    f'<source srcset={IMG}/about-banner.jpg media="(min-width: 768px)" '
    "width=1280 height=360>\n"
    f"<source srcset={IMG}/about-banner-mobile.jpg width=640 height=834>\n"
    f'<img src={IMG}/about-banner-mobile.jpg width=640 height=834 '
    'alt="The Santosh Magnetic Works team at our Mumbai works" /></picture>'
)


def row(inner: str, alt: bool = False, extra: str = "") -> str:
    """A section. row--alt gives the site's paper background, used to alternate."""
    cls = "row row--alt" if alt else "row"
    if extra:
        cls += " " + extra
    return f'<div class="{cls}">{inner}</div>'


def intro_two_col(eyebrow: str, heading: str, paras: list[str]) -> str:
    """The site's eyebrow + heading / body two-column intro (content--text_2)."""
    body = "".join(f"<p>{p}" for p in paras)
    return (
        '<div class="row__inner content content--text_2">'
        f"<div><h6>{eyebrow}</h6><h2>{heading}</h2></div>"
        f"<div class=content__body>{body}</div>"
        "</div>"
    )


def icon_boxes(items: list[tuple[str, str]], cols: int = 0) -> str:
    """The site's icon_boxes_1 grid: a styled card per item, no bare paragraphs.

    cols overrides the default two-column layout. Three items in a two-column
    grid leave the third orphaned on a row of its own.
    """
    style = (
        f' style="grid-template-columns:repeat({cols},minmax(0,1fr))"'
        if cols
        else ""
    )
    return (
        f'<div class="row__inner icon_boxes_1"{style}>'
        + "".join(
            '<div class="icon_boxes_1__item alt-swap"><div>'
            f"<h4>{title}</h4><span>{text} </span>"
            "</div></div>"
            for title, text in items
        )
        + "</div>"
    )


def section_heading(heading: str, sub: str = "") -> str:
    p = f"<p class=intro>{sub}" if sub else ""
    return (
        '<div class="row__inner row__intro">'
        f"<h3 class=bordered-header>{heading}</h3>{p}</div>"
    )


# 1. Intro: eyebrow-led, two columns.
INTRO = row(
    intro_two_col(
        "About SMAG",
        "A Mumbai magnet workshop, on production lines since 1978",
        [
            "We design, machine and test every unit at our own works in Dahisar, "
            "Mumbai. Nothing leaves until it has been matched to the job it is "
            "going to do. We have worked this way since 1978, for plants across "
            "India and for export.",
            "<strong>Every unit is sized from the application itself.</strong> "
            "Your material, your throughput and your load decide the pull, the "
            "reach and the housing we build.",
        ],
    ),
    alt=True,
)

# 2. Story: image and text pair.
STORY = row(
    '<div class="row__inner content image-text-pair image-text-pair--left">'
    "<div class=image-text-pair__image><div>"
    # style=height:auto: the component CSS sets width:100% but not height:auto,
    # so a bare height attribute becomes the used height and distorts the image.
    f'<img src={IMG}/about-story.jpg width=1080 height=815 style="height:auto" '
    'alt="The Santosh Magnetic Works team at our Mumbai works" /></div></div>'
    "<div class=image-text-pair__text>"
    "<h3 class=bordered-header>Built in-house, matched to the job</h3>"
    "<p>Magnet circuits, housings and machined faces are all made here, which "
    "puts build quality and delivery dates in our own hands. Inspection and "
    "dispatch run under an ISO 9001:2015 system."
    "<p>Years after a unit ships we still carry spares for it, re-magnetise "
    "assemblies that have weakened, and service what we sold."
    "</div></div>"
)

# 3. Statistics. Titles are kept short: the CSS lays this out as repeat(4,1fr),
# and a title that wraps to two lines pushes its caption out of alignment.
STATS = (
    '<div class="row statistics"><div class=row__inner>'
    "<div class=statistics__item><p class=title>1978 <span></span>"
    "<p class=text>The year we started making magnets in Mumbai </div>"
    "<div class=statistics__item><p class=title>ISO 9001 <span></span>"
    "<p class=text>Quality system certified for manufacture and export </div>"
    "<div class=statistics__item><p class=title>4.7 / 5 <span></span>"
    "<p class=text>Average across 23 customer reviews </div>"
    "<div class=statistics__item><p class=title>Export <span></span>"
    "<p class=text>Shipped to plants across India and overseas </div>"
    "</div></div>"
)

# 4. Selection process, as cards rather than loose text.
STEPS = [
    ("01. Read the application",
     "What is the material, how fast is it moving, how much room is there, and "
     "what are you trying to catch or lift."),
    ("02. Match the circuit",
     "Pull, reach, pole layout and housing get sized to those answers and "
     "drawn up for your line."),
    ("03. Build, test and dispatch",
     "Made, tested and packed here. Servicing and spares later come from the "
     "same workshop."),
]
PROCESS = row(
    section_heading(
        "How we specify a magnet",
        "The same three steps whether you need one stock magnet or a separator "
        "built around your line.",
    )
    + icon_boxes(STEPS, cols=3),
    alt=True,
)

# 5. Manufacturing strengths, from SMAG's own pre-takedown copy.
STRENGTHS = [
    ("Application review",
     "We look at the material, the load, the flow and the space you have before "
     "anything gets selected."),
    ("Magnet circuit",
     "Pull, reach and pole layout matched to the separation, lifting or holding "
     "task in front of us."),
    ("Fabrication",
     "Housings, frames and working faces built to take daily plant-floor "
     "use."),
    ("Inspection",
     "Every unit checked against the order and the application before it "
     "leaves."),
    ("Packing and supply",
     "Packed for the journey, whether that is across Mumbai or onto an export "
     "container."),
    ("After-sales support",
     "Spares, servicing and re-magnetising, years after the sale."),
]
CONTROL = row(
    section_heading(
        "What stays under our control",
        "The stages we handle on our own floor.",
    )
    + icon_boxes(STRENGTHS)
)

# 6. Leadership.
TEAM_MEMBERS = [
    ("Rahul Ingle", "CEO", "team-rahul-ingle.jpg"),
    ("Sushil Ingle", "COO", "team-sushil-ingle.jpg"),
]
TEAM = row(
    section_heading("The people behind SMAG")
    # grid--about is a 3-column grid; with two people the third column reads as
    # a gap, so constrain it to two and cap the width.
    + '<div class=row__inner><div class="grid grid--about" '
      'style="grid-template-columns:repeat(2,minmax(0,1fr));max-width:850px">'
    + "".join(
        "<div class=grid__item><div class=team__item>"
        "<div class=team__image>"
        f'<img src={IMG}/{photo} width=543 height=724 style="height:auto" '
        f'alt="{name}" />'
        f"<h3>{name}</h3></div>"
        f"<h6 class=bordered-header>{role}</h6>"
        "</div></div>"
        for name, role, photo in TEAM_MEMBERS
    )
    + "</div></div>",
    alt=True,
)

# 7. Quality: an eyebrow-led two-column block, not an orphaned paragraph.
CERTS = row(
    intro_two_col(
        "Quality",
        "Checked against the order and the application",
        [
            "Manufacturing, inspection and dispatch are carried out under an "
            "ISO 9001:2015 quality management system covering the manufacture and "
            "export of magnetic equipment.",
            "Units are checked against both the order requirements and the "
            "application before they leave the works, and we keep spares, "
            "servicing and re-magnetising available long afterwards.",
        ],
    )
)

# The CTA row is a sibling of content-wrapper, not a child, so the </div>
# closing content-wrapper falls inside the replaced region and must be re-emitted.
NEW_MAIN_BODY = (
    # The Quality block (CERTS) was dropped: it read as an odd trailing slab.
    # The client logo strip is appended separately by add_client_logos.py.
    INTRO + STORY + STATS + PROCESS + CONTROL + TEAM + "</div>"
)

# From the banner <picture> through to the CTA row, exclusive.
BODY_RE = re.compile(
    r'(<div class="row row--breadcrumbs">.*?</div></div></div>)'  # keep breadcrumbs
    r".*?"
    r'(<div class="row row--action">)',                           # keep the CTA
    re.DOTALL,
)
PIC_RE = re.compile(r"<picture>.*?</picture>", re.DOTALL)
TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
DESC_RE = re.compile(r'<meta name=description content="[^"]*">')


def main() -> None:
    text = PAGE.read_text(encoding="utf-8")
    before = len(text)

    text, n_pic = PIC_RE.subn(BANNER, text, count=1)
    text, n_body = BODY_RE.subn(
        lambda m: m.group(1) + NEW_MAIN_BODY + m.group(2), text, count=1
    )
    text = TITLE_RE.sub("<title>About Us | Santosh Magnetic Works</title>", text)
    text = DESC_RE.sub(
        '<meta name=description content="Santosh Magnetic Works has designed, '
        'machined and tested magnetic separation, filtration, lifting and '
        'workholding equipment in Mumbai since 1978. ISO 9001:2015 certified.">',
        text,
    )

    if not (n_pic and n_body):
        print(f"FAILED: banner={n_pic} body={n_body}")
        return

    PAGE.write_text(text, encoding="utf-8")
    print(f"ok  company/about-us/index.html  {before} -> {len(text)} bytes")

    m = re.search(r"<main>.*</main>", text, re.DOTALL)
    seg = m.group(0)
    traces = re.findall(
        r"Eclipse|Sheffield|McAllorum|Dave Smith|Andy Reeve|Rachael|Latham|"
        r"ISO14001|ISO 14001|ATEX|100 Years|Case Studies|swiper-wrapper></div>",
        seg,
    )
    print(f"Eclipse traces left in <main>: {len(traces)}  {sorted(set(traces))}")
    print(f"empty carousels left: {len(re.findall(r'<div class=swiper-wrapper>\s*</div>', seg))}")
    for h in re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", seg, re.DOTALL):
        print(f"  h{h[0]}: {re.sub(r'<[^>]+>', '', h[1]).strip()[:80]}")


if __name__ == "__main__":
    main()
