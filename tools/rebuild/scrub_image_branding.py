#!/usr/bin/env python3
"""Scrub Eclipse branding out of the catalogue imagery.

Several Eclipse product photos carry the Eclipse name cast into or labelled
on the product itself (alnico horseshoe and pot magnets stamped ECLIPSE
SHEFFIELD ENGLAND, the demagnetiser and chuck labels, the sweeper and
liquid-trap label strips), which no amount of painting can fix. Three moves:

1. The affected product pages get galleries built from SMAG's own brochure
   stills (several of these pages had empty galleries anyway, because the
   mirror never fetched their heroes). The neodymium pages get their clean,
   unbranded photos promoted into the empty galleries.
2. Every remaining reference to a branded rendition (family-grid tiles,
   related-product cards, guide cards) is repointed at the SMAG tile
   rendition site-wide, and the branded files are deleted.
3. Assets whose FILENAME contains "eclipse" (the family banner images and
   the grid magnet photo, all visually unbranded) are renamed with the
   brand token dropped, and every reference updated.

The watermark manifest is updated so the deleted files drop out of it.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_smag_product_pages as build  # noqa: E402
from fix_missing_media import replace_gallery  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
MANIFEST = REPO / "assets/source/watermarked.txt"
SMAG = "/site/assets/images/smag"

# page -> [(master stem | existing url, alt)]
GALLERIES = {
    "products/magnetic-tools-and-standard-magnets/alnico-power-magnets": [
        ("alnico-power-magnet-01",
         "Cast alnico power magnet with threaded mounting hole"),
        ("alnico-power-magnet-02",
         "Cast alnico power magnets in a range of sizes"),
    ],
    "products/magnetic-tools-and-standard-magnets/alnico-deep-pot-magnets": [
        ("alnico-power-magnet-03",
         "Cast alnico deep pot magnets, mixed sizes"),
    ],
    "products/magnetic-tools-and-standard-magnets/alnico-shallow-pot-magnets": [
        ("shallow-pot-magnet-01",
         "Shallow pot magnets showing face and back"),
        ("shallow-pot-magnet-02",
         "Pot magnets including a threaded boss fitting"),
        ("pot-magnets-group-01",
         "Countersunk pot magnets in mixed sizes"),
    ],
    "products/magnetic-tools-and-standard-magnets/magnetic-sweeper": [
        ("magnetic-floor-sweeper-01",
         "Magnetic floor sweeper collecting swarf and pins"),
        ("magnetic-floor-sweeper-02",
         "Push-type magnetic floor sweeper"),
    ],
    "products/magnetic-tools-and-standard-magnets/neodymium-disc-magnets": [
        ("ndfeb-disc-magnets-01",
         "Stack of nickel plated neodymium disc magnets"),
    ],
    "products/magnetic-tools-and-standard-magnets/neodymium-block-magnets": [
        ("/site/assets/files/8471/neodymium-block-magnets-1.355x205.jpg",
         "Nickel plated neodymium block magnet"),
    ],
    "products/magnetic-tools-and-standard-magnets/neodymium-channel-magnet": [
        ("/site/assets/files/10002/neodymium-channel-magnet.355x205.jpg",
         "Neodymium channel magnets in a range of lengths"),
    ],
    "products/magnetic-separation-and-metal-detection/"
    "deep-field-magnetic-plate-separator": [
        ("magnetic-plate-magnet-01",
         "Encapsulated deep field plate magnet"),
    ],
    "products/magnetic-separation-and-metal-detection/"
    "high-intensity-liquid-filter-separator": [
        ("magnetic-liquid-trap-inline-01",
         "In-line magnetic liquid trap dismantled, showing the flanged "
         "body and rod clusters"),
        ("magnetic-liquid-trap-housed-01",
         "Housed high-intensity magnetic liquid trap with flanged "
         "connections"),
    ],
}

# branded image bases -> SMAG tile rendition that replaces every reference
URL_SWAPS = {
    "/site/assets/files/2592/alnico_power_magnets":
        f"{SMAG}/alnico-power-magnet-01.tile.jpg",
    "/site/assets/files/2650/alnico_shallow_pot_magnets":
        f"{SMAG}/shallow-pot-magnet-01.tile.jpg",
    "/site/assets/files/2703/alnico_deep_pot_magnets":
        f"{SMAG}/alnico-power-magnet-03.tile.jpg",
    "/site/assets/files/8226/group_sweepers":
        f"{SMAG}/magnetic-floor-sweeper-01.tile.jpg",
    "/site/assets/files/7527/liquid_filter_expanded":
        f"{SMAG}/magnetic-liquid-trap-inline-01.tile.jpg",
    "/site/assets/files/11196/da955-uk_table_top_demagnetiser":
        f"{SMAG}/table-top-demagnetiser-01.tile.jpg",
    "/site/assets/files/11228/ax47-p_rectangular_premier_chuck":
        f"{SMAG}/rectangular-magnetic-chuck-01.tile.jpg",
    "/site/assets/files/3422/chuck_premier_rectangular_cut_web":
        f"{SMAG}/rectangular-magnetic-chuck-02.tile.jpg",
    "/site/assets/files/36584/eruc1545":
        f"{SMAG}/rectangular-magnetic-chuck-03.tile.jpg",
}

# filename stems carrying the brand token, image content itself unbranded
RENAMES = {
    "eclipse_-_grid_magnet": "grid_magnet",
    "foreign_object_removal-eclipse_magnetics": "foreign_object_removal",
    "lifting_and_handling_tools_-_eclipse_magnetics":
        "lifting_and_handling_tools",
    "magnetic-filtration-eclipse-magnetics-": "magnetic-filtration",
    "magnetic-tools-eclipse-magnetics-": "magnetic-tools",
    "bespoke-magnets-eclipse-magnetics": "bespoke-magnets",
}

SRCSET_RE = re.compile(r'\s*srcset="([^"]*)"')


def pseudo_img(url: str) -> dict:
    return {"hero": url, "hero_w": 355, "hero_h": 205,
            "zoom": url, "thumb": url, "tile": url}


def dedupe_srcsets(text: str) -> tuple[str, int]:
    n = 0
    for m in reversed(list(SRCSET_RE.finditer(text))):
        urls = {c.strip().split(" ")[0] for c in m.group(1).split(",")
                if c.strip()}
        if len(urls) == 1:
            text = text[: m.start()] + text[m.end():]
            n += 1
    return text, n


def main() -> None:
    dry = "--dry-run" in sys.argv

    for rel, specs in GALLERIES.items():
        page = SITE / rel / "index.html"
        text = page.read_text(encoding="utf-8")
        imgs = [pseudo_img(s) if s.startswith("/") else build.renditions(s)
                for s, _ in specs]
        text = replace_gallery(text, imgs, [alt for _, alt in specs])
        print(f"gallery ({len(specs)}): {rel}")
        if not dry:
            page.write_text(text, encoding="utf-8")

    # product tiles whose image div ended up empty (hero never crawled):
    # the family grid tile and any related-product tiles, site-wide
    tile_imgs = {
        "magnetic-separation-and-metal-detection/"
        "deep-field-magnetic-plate-separator":
            ("magnetic-plate-magnet-01.tile.jpg",
             "Encapsulated deep field plate magnet"),
        "magnetic-separation-and-metal-detection/magnetic-strip-separator":
            ("hand-magnet-easy-clean-01.tile.jpg",
             "Hand-held easy-clean magnetic separator"),
        "magnetic-separation-and-metal-detection/underflow-magnet":
            ("suspension-magnet-01.tile.jpg",
             "Encapsulated plate magnet with lifting eye bolts"),
    }
    filled = 0
    for page in sorted(SITE.rglob("*.html")):
        text = orig = page.read_text(encoding="utf-8")
        for slug, (img, alt) in tile_imgs.items():
            text = re.sub(
                rf"(href=/products/{re.escape(slug)}/ class=alt-swap>)"
                r"<div class=image></div>",
                rf'\1<div class=image><img src={SMAG}/{img} width=355 '
                rf'height=205 alt="{alt}" /></div>', text)
        if text != orig:
            filled += 1
            if not dry:
                page.write_text(text, encoding="utf-8")
    print(f"empty product tiles filled on {filled} page(s)")

    swapped = renamed_refs = 0
    for page in sorted(SITE.rglob("*.html")):
        text = orig = page.read_text(encoding="utf-8")
        for base, new in URL_SWAPS.items():
            pat = re.compile(re.escape(base) + r"[^\s\"'>),]*")
            text, n = pat.subn(new, text)
            swapped += n
        for old, new in RENAMES.items():
            renamed_refs += text.count(old)
            text = text.replace(old, new)
        text, _ = dedupe_srcsets(text)
        if text != orig and not dry:
            page.write_text(text, encoding="utf-8")
    print(f"references swapped: {swapped}, renamed refs: {renamed_refs}")

    deleted = renamed = 0
    for base in URL_SWAPS:
        d = SITE / Path(base.lstrip("/")).parent
        stem = Path(base).name
        for f in d.glob(f"{stem}*"):
            if not dry:
                f.unlink()
            deleted += 1
    for old, new in RENAMES.items():
        for f in SITE.rglob(f"*{old}*"):
            if not f.is_file():
                continue
            if not dry:
                f.rename(f.with_name(f.name.replace(old, new)))
            renamed += 1
    print(f"files deleted: {deleted}, files renamed: {renamed}")

    # orphaned eclipse-named files nothing references any more
    refs: set[str] = set()
    for page in SITE.rglob("*.html"):
        refs.update(re.findall(r"/site/assets/[^\s\"'>),]+",
                               page.read_text(encoding="utf-8")))
    orphans = 0
    for f in (SITE / "site/assets").rglob("*"):
        if f.is_file() and "eclipse" in f.name.lower():
            url = "/site/assets/" + str(f.relative_to(SITE / "site/assets"))
            if url not in refs:
                if not dry:
                    f.unlink()
                orphans += 1
    print(f"orphaned eclipse-named files deleted: {orphans}")

    if not dry and MANIFEST.exists():
        entries = MANIFEST.read_text(encoding="utf-8").split()
        keep = []
        for e in entries:
            if any(e.startswith(b) for b in URL_SWAPS):
                continue
            for old, new in RENAMES.items():
                e = e.replace(old, new)
            keep.append(e)
        MANIFEST.write_text("\n".join(sorted(set(keep))) + "\n",
                            encoding="utf-8")
        print("watermark manifest updated")


if __name__ == "__main__":
    main()
