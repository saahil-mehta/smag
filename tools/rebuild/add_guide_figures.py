#!/usr/bin/env python3
"""Place photographs and line diagrams in the guide sources.

Each entry names a guide, a section heading, and a figure line in the
markdown figure syntax build_guides.py renders:

    ![Caption](photo:<brochure still>)    a SMAG photograph, captioned
    ![Caption](diagram:<name>)            assets/source/diagrams/<name>.svg

The figure goes after the first paragraph of that section. A figure that
is already in the source is left alone, so the script can be re-run.
Photos are only placed where the still shows what the caption says; the
pipeline and coolant filter guides have no matching SMAG still and carry
diagrams only.

Run with --dry-run to report without writing. Run build_guides.py after.
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path("/Users/saahil/Documents/GitHub/smag/assets/source/guides")
DRY = "--dry-run" in sys.argv

FIGURES = [
    # line diagrams: the mechanism guides
    ("how-magnetic-filtration-works", "How are the particles caught?",
     "![Liquid flows around the magnetic rods. Iron particles are pulled onto the rods and the clean liquid flows on.](diagram:filter-flow)"),
    ("guide-to-magnetic-separation", "How does it work?",
     "![A grid of magnetic rods in a hopper. The product falls between the rods and the iron stays on them.](diagram:hopper-grid)"),
    ("factors-to-consider-when-choosing-a-magnetic-chuck", "3. Which pole pitch?",
     "![A small part needs to sit across more than one pole to be held firmly.](diagram:chuck-pole-pitch)"),
    ("what-is-a-pot-magnet", "How the steel cup works",
     "![The steel cup brings the field to the working face, where it closes through the steel.](diagram:pot-field)"),
    ("key-considerations", "2. Is the plate thick enough?",
     "![A thin plate cannot carry the whole field, so the lifter holds less.](diagram:lifter-plate)"),
    ("how-black-powder-forms", "How does black powder form?",
     "![Black powder forms on the pipe wall, travels with the flow and is held in a magnetic filter.](diagram:black-powder)"),
    # SMAG photographs
    ("are-all-metals-magnetic", "What this means on a production line",
     "![A SMAG neodymium separator rod in a sealed stainless steel tube.](photo:neodymium-magnetic-rod-01)"),
    ("are-all-stainless-steels-magnetic", "Choosing a separator for stainless contamination",
     "![A stainless cased magnetic rod cartridge.](photo:magnetic-rod-01)"),
    ("critical-control-points-in-food-processing", "Step 3: fit a control at each point",
     "![A SMAG double drawer housing for an enclosed transfer line.](photo:double-drawer-housing-ss-01)"),
    ("enhancing-safety-in-lifting", "How a magnetic lifter works",
     "![A SMAG Maxx permanent magnetic lifter. The handle turns the hold on and off.](photo:permanent-magnetic-lifter-01)"),
    ("factors-to-consider-when-choosing-a-magnetic-chuck", "1. What shape is the machine table?",
     "![A SMAG rectangular permanent magnetic chuck for a surface grinder.](photo:rectangular-magnetic-chuck-02)"),
    ("factors-to-consider-when-choosing-a-magnetic-chuck", "5. How will you demagnetise?",
     "![The SMAG Maxx-Demag table top demagnetiser.](photo:table-top-demagnetiser-01)"),
    ("guide-to-magnet-materials", "Neodymium (NdFeB)",
     "![SMAG neodymium disc magnets.](photo:ndfeb-disc-magnets-01)"),
    ("guide-to-magnet-materials", "Alnico",
     "![A SMAG alnico power magnet.](photo:alnico-power-magnet-01)"),
    ("guide-to-magnetic-separation", "What types are there?",
     "![A SMAG deep field magnetic plate separator for conveyors and chutes.](photo:deep-field-plate-01)"),
    ("hidden-costs-of-traditional-steel-lifting", "Idle cranes",
     "![A Maxx lifter stays on the crane hook between lifts.](photo:permanent-magnetic-lifter-02)"),
    ("how-magnetic-filtration-works", "What is inside the filter?",
     "![Magnetic rods of this kind sit inside the filter housing.](photo:magnetic-rod-01)"),
    ("magnetic-filters-in-comparison-to-traditional-filters", "How a magnetic filter works",
     "![A SMAG inline magnetic liquid trap.](photo:magnetic-liquid-trap-inline-01)"),
    ("minimising-product-recalls-in-the-food-industry", "Control 2: remove metal at every stage",
     "![A SMAG housed liquid trap for syrup, oil and sauce lines.](photo:magnetic-liquid-trap-housed-01)"),
    ("reducing-the-risk-of-metal-contamination-in-food-processing", "Step 3: check the finished product",
     "![A SMAG magnetic sampling probe for spot checks on sacks and bins.](photo:magnetic-sampling-rod-01)"),
    ("types-of-filtration-for-cnc-machines", "Magnetic filters",
     "![Neodymium magnetic rods of the kind used in a SMAG magnetic filter.](photo:neodymium-magnetic-rod-01)"),
    ("what-is-a-pot-magnet", "Shallow or deep",
     "![SMAG alnico pot magnets.](photo:pot-magnets-group-01)"),
    ("where-are-magnets-used", "Cleaning up",
     "![A SMAG magnetic sweeper picks up swarf, nails and screws from the floor.](photo:magnetic-floor-sweeper-01)"),
    ("where-are-magnets-used", "Measuring magnets",
     "![A gauss meter measures the strength of a magnet.](photo:gauss-meter-with-hand)"),
    ("why-magnetic-lifters-are-more-efficient-than-chains-and-slings", "Choosing a lifter",
     "![A SMAG Maxx permanent magnetic lifter.](photo:permanent-magnetic-lifter-03)"),
    ("why-magnetic-separation-and-metal-detection-is-vital-for-haccp-supplier-audits", "Sampling and verification",
     "![A gauss meter reading checks each magnet against its certificate.](photo:gauss-meter-with-hand)"),
    ("workholding-tips", "Installing a chuck",
     "![A SMAG circular permanent magnetic chuck.](photo:round-magnetic-chuck-02)"),
]


def place(text: str, heading: str, fig: str) -> str | None:
    lines = text.split("\n")
    try:
        h = lines.index(f"## {heading}")
    except ValueError:
        raise SystemExit(f"heading not found: {heading!r}")
    i = h + 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines) and lines[i].strip() and not lines[i].startswith("## "):
        i += 1  # end of the first block after the heading
    return "\n".join(lines[:i] + ["", fig] + lines[i:])


def main() -> int:
    done = added = 0
    for slug, heading, fig in FIGURES:
        p = SRC / f"{slug}.md"
        s = p.read_text(encoding="utf-8")
        if fig in s:
            done += 1
            continue
        s = place(s, heading, fig)
        added += 1
        if not DRY:
            p.write_text(s, encoding="utf-8")
    print(f"  {added} figures placed, {done} already present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
