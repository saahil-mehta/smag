#!/usr/bin/env python3
"""Remove the pages and files that are Eclipse's, with no SMAG equivalent.

Deletes:
  - video-hub/ and resources/webinars/  (recordings of Eclipse's own videos)
  - industry-quality-standards/         (Eclipse's ISO 14001 / PPAP / UK QC)
  - products/.../certifications/        (Eclipse's in-house ATEX and EHEDG
                                         certification story)
  - magnetic-filters-for-edm-machines/  (SEO landing page for the removed
                                         Micromag range)
  - resources/guides/some-common-questions-after-brexit/
  - every PDF under site/ except site/assets/files/smag/ (all are Eclipse
    datasheets and brochures)

Then hosts SMAG's own printed brochures (from the client's docs folder,
masters versioned under assets/source/brochures/) at /site/assets/files/smag/.
Links to everything deleted are removed by scrub_dead_links.py afterwards.
"""
from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
DOCS = Path("/Users/saahil/Downloads/s-magnetic/docs")
MASTERS = REPO / "assets/source/brochures"
HOSTED = SITE / "site/assets/files/smag"

DROP_DIRS = [
    "video-hub",
    "resources/webinars",
    "industry-quality-standards",
    "magnetic-filters-for-edm-machines",
    "resources/guides/some-common-questions-after-brexit",
    "products/magnetic-separation-and-metal-detection/certifications",
]

# source PDF in the client docs -> hosted name
BROCHURES = {
    "ROD FINAL.pdf": "smag-magnetic-rods-and-grills.pdf",
    "Lifter.pdf": "smag-neolift-magnetic-lifters.pdf",
    "Rare Earth (1).pdf": "smag-maxx-clean-rare-earth.pdf",
}


def main() -> None:
    for d in DROP_DIRS:
        p = SITE / d
        if p.exists():
            shutil.rmtree(p)
            print(f"deleted {d}/")
        else:
            print(f"(already gone: {d})")

    # stray filter-variant file in guides
    for f in SITE.glob("resources/guides/index.html?*.html"):
        f.unlink()
        print(f"deleted {f.name}")

    kept = removed = 0
    for pdf in SITE.rglob("*.pdf"):
        if HOSTED in pdf.parents:
            kept += 1
            continue
        pdf.unlink()
        removed += 1
    print(f"PDFs removed: {removed} (kept {kept} under files/smag/)")

    MASTERS.mkdir(parents=True, exist_ok=True)
    HOSTED.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in BROCHURES.items():
        src = DOCS / src_name
        master = MASTERS / dst_name
        if not master.exists():
            shutil.copy2(src, master)
        shutil.copy2(master, HOSTED / dst_name)
        print(f"hosted /site/assets/files/smag/{dst_name}")


if __name__ == "__main__":
    main()
