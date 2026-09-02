#!/usr/bin/env python3
"""Delete the Eclipse educational and service sub-pages inside the product
families, and the sub-nav items that pointed at them.

These pages (a guide to magnetic separation, how filtration works, why
magnetic filters, sector expertise with Eclipse's client list, custom
solutions built around FEA modelling and site audits, "our package",
testing and validation, typical applications with a global distributor
network, useful workholding tips written for Eclipse's AX chuck range, and
the black powder explainer) carried Eclipse's offer, not SMAG's. Saahil
agreed on 2 Sep 2026 that they go. Custom work is now a line in each
family intro, and the twelve guides cover the educational ground.

Also removes the "#case-studies" sub-nav anchor (the section was deleted
long ago) so the family sub-nav is Overview | Products.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
DROP = [
    "products/filtration-systems/how-magnetic-filters-work",
    "products/filtration-systems/why-magnetic-filters",
    "products/filtration-systems/sector-expertise",
    "products/filtration-systems/custom-solutions",
    "products/magnetic-separation-and-metal-detection/magnetic-separation",
    "products/magnetic-separation-and-metal-detection/site-survey",
    "products/magnetic-separation-and-metal-detection/what-we-offer",
    "products/magnetic-separation-and-metal-detection/custom-solutions",
    "products/magnetic-tools-and-standard-magnets/typical-applications",
    "products/workholding-systems/useful-workholding-tips",
    "products/oil-and-gas-pipeline-filtration/pipeline-contamination-and-black-powder-formation",
]
CASE_LI = re.compile(r"<li><a href=[^ >]*#case-studies[^>]*>\s*Case Studies\s*</a>")


def main() -> None:
    dry = "--dry-run" in sys.argv
    n = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        new, k = CASE_LI.subn("", text)
        if k:
            n += 1
            if not dry:
                page.write_text(new, encoding="utf-8")
    print(f"case-studies sub-nav item removed from {n} pages")
    for d in DROP:
        p = SITE / d
        if p.exists():
            print(f"  {'would delete' if dry else 'deleted'} {d}/")
            if not dry:
                shutil.rmtree(p)
        else:
            print(f"  missing {d}/")
    print(f"{len(list(SITE.rglob('*.html')))} pages remain")


if __name__ == "__main__":
    main()
