#!/usr/bin/env python3
"""Trim each product family to the range SMAG actually makes.

Per family this script:
  - harvests the listing tiles for the kept products from index.html and its
    pagination/filter-variant files (before anything is deleted)
  - deletes the dropped product directories and the pagination/filter files
  - rebuilds the family index grid with only the kept tiles, in the agreed
    order, and removes the now-dead pager and search/filter form
  - removes the rows that promoted the eclipsemagnetics.shop store

It also renames housed-easy-clean-grid-magnets-from-eclipse-magnetics/ to
housed-easy-clean-grid-magnet-separator/ and updates every reference.

Lifting & Handling is cleared of the Eclipse range here; its SMAG range is
added by a later script from the works' own brochures. Links elsewhere that
point at deleted pages are handled by scrub_dead_links.py at the end of the
chain, once the new pages exist.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end, remove_enclosing_row  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
PRODUCTS = SITE / "products"

# family -> (kept product slugs in grid order, kept support pages, dropped dirs)
FAMILIES: dict[str, tuple[list[str], list[str], list[str]]] = {
    "magnetic-separation-and-metal-detection": (
        [
            "housed-easy-clean-grid-magnets-from-eclipse-magnetics",
            "high-intensity-liquid-filter-separator",
            "magnetic-grids-for-sieves",
            "magnetic-separation-grids",
            "easy-clean-magnetic-grid-separator",
            "deep-field-magnetic-plate-separator",
        ],
        ["magnetic-separation", "what-we-offer", "site-survey",
         "certifications", "custom-solutions"],
        [
            "auto-rota-shuttle", "auto-shuttle-double-row",
            "housed-separating-drum", "magnetic-drum-metal-separator",
            "magnetic-head-roller", "magnetic-overband-separator",
            "pneumag-magnetic-separator", "rota-grid-separator",
        ],
    ),
    "filtration-systems": (
        ["filtramag"],
        ["how-magnetic-filters-work", "why-magnetic-filters",
         "custom-solutions", "sector-expertise"],
        ["autofiltrex", "automag-am32-skid", "automag-skid",
         "micromag", "micromag-hp50", "micromag-hp80"],
    ),
    "magnetic-tools-and-standard-magnets": (
        [
            "magnetic-sweeper", "alnico-power-magnets",
            "neodymium-block-magnets", "neodymium-disc-magnets",
            "neodymium-channel-magnet", "alnico-shallow-pot-magnets",
            "alnico-deep-pot-magnets",
        ],
        ["typical-applications"],
        [
            "alnico-button-magnets", "alnico-pocket-magnets",
            "energise-to-release-electromagnet", "find-a-stockist",
            "magnetic-swarf-wand", "marker-magnets",
            "quick-holding-clamp-switchable", "rectangular-premier-chuck",
        ],
    ),
    "workholding-systems": (
        [
            "rectangular-premier-chuck", "rectangular-universal-chuck",
            "circular-premier-chuck", "circular-universal-chuck",
            "table-top-demagnetiser",
        ],
        ["useful-workholding-tips"],
        ["chuck-blocks", "radial-pole-premier-chuck",
         "supermill-magnetic-chuck"],
    ),
    "lifting-and-handling": (
        [],  # SMAG range added later from the works' brochures
        [],
        [
            "baking-tray-handling-system", "magnetic-palletiser",
            "optimag-e-electronically-activated-handling-system",
            "optimag-p-magnetic-handling-system", "sector-expertise",
            "service-maintenance", "sheet-steel-separator",
            "ultralift-e", "ultralift-plus", "ultralift-tp-magnetic-lifter",
        ],
    ),
}

RENAME = (
    "housed-easy-clean-grid-magnets-from-eclipse-magnetics",
    "housed-easy-clean-grid-magnet-separator",
)

GRID_OPEN = '<div class="grid grid--product-category">'
TILE_OPEN = "<div class=grid__item>"


def listing_files(fam_dir: Path) -> list[Path]:
    files = [fam_dir / "index.html"]
    files += sorted(fam_dir.glob("page*.html"))
    files += sorted(fam_dir.glob("index.html?*.html"))
    return [f for f in files if f.exists()]


def harvest_tiles(fam: str, fam_dir: Path) -> dict[str, str]:
    """slug -> tile html, first occurrence across the listing files."""
    tiles: dict[str, str] = {}
    href_re = re.compile(rf"href=/products/{re.escape(fam)}/([a-z0-9-]+)/")
    for f in listing_files(fam_dir):
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(re.escape(TILE_OPEN), text):
            end = find_element_end(text, m.start())
            if not end:
                continue
            tile = text[m.start():end]
            a = href_re.search(tile)
            if a and a.group(1) not in tiles:
                tiles[a.group(1)] = tile
    return tiles


def remove_element(text: str, open_re: str) -> tuple[str, int]:
    removed = 0
    while True:
        m = re.search(open_re, text)
        if not m:
            return text, removed
        end = find_element_end(text, m.start())
        if not end:
            return text, removed
        text = text[: m.start()] + text[end:]
        removed += 1


def rebuild_index(fam: str, keep: list[str], tiles: dict[str, str],
                  dry: bool) -> None:
    page = PRODUCTS / fam / "index.html"
    text = page.read_text(encoding="utf-8")

    i = text.find(GRID_OPEN)
    if i < 0:
        print(f"  !! no product grid found on {fam}/index.html")
        return
    end = find_element_end(text, i)
    kept = [tiles[s] for s in keep if s in tiles]
    missing = [s for s in keep if s not in tiles]
    if missing:
        print(f"  !! no tile harvested for {fam}: {missing}")
    text = text[:i] + GRID_OPEN + "".join(kept) + "</div>" + text[end:]

    text, pagers = remove_element(text, r"<ul class=MarkupPagerNav\b")
    text, filters = remove_element(text, r"<div class=category-search>")
    print(f"  {fam}/index.html: {len(kept)} tiles kept, "
          f"{pagers} pager(s), {filters} filter form(s) removed")
    if not dry:
        page.write_text(text, encoding="utf-8")


def main() -> None:
    dry = "--dry-run" in sys.argv

    for fam, (keep, _support, drop) in FAMILIES.items():
        fam_dir = PRODUCTS / fam
        print(f"== {fam}")
        tiles = harvest_tiles(fam, fam_dir)

        for slug in drop:
            d = fam_dir / slug
            if d.exists():
                print(f"  delete dir  {slug}/")
                if not dry:
                    shutil.rmtree(d)
            else:
                print(f"  (already gone: {slug})")
        for f in list(fam_dir.glob("page*.html")) + \
                list(fam_dir.glob("index.html?*.html")):
            print(f"  delete file {f.name}")
            if not dry:
                f.unlink()

        rebuild_index(fam, keep, tiles, dry)

    # rename the Eclipse-branded slug
    old, new = RENAME
    src = PRODUCTS / "magnetic-separation-and-metal-detection" / old
    dst = PRODUCTS / "magnetic-separation-and-metal-detection" / new
    if src.exists():
        print(f"rename {old} -> {new}")
        if not dry:
            src.rename(dst)
    refs = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        if old not in text and "eclipsemagnetics.shop" not in text:
            continue
        n = text.count(old)
        text = text.replace(old, new)
        text, rows = remove_enclosing_row(text, "eclipsemagnetics.shop")
        if n or rows:
            refs += n
            print(f"  {n} slug refs, {rows} shop rows: {page.relative_to(SITE)}")
        if not dry:
            page.write_text(text, encoding="utf-8")
    print(f"slug references updated: {refs}")


if __name__ == "__main__":
    main()
