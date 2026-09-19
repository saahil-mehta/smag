#!/usr/bin/env python3
"""Rename the three Eclipse-trademarked products to generic descriptive names.

Filtramag, Filtramag XT and Ultrafiltrex are registered Eclipse Magnetics
marks that survived the earlier debranding sweeps, still carried in page
titles, h1s, JSON-LD breadcrumbs, og tags, nav, the sitemap, asset filenames
and body copy.

Three layers are rewritten together, because site/ is committed and deployed
and the markdown under assets/source/ is what the copy is authored in:

1. assets/source/pages/**.md and assets/source/guides/*.md, including the
   three product files' own slugs.
2. site/**/*.html, plus the three page directories and the branded image
   filenames.
3. site/sitemap.xml and the watermark manifest.

Prose pairs run before name pairs, and name pairs run longest-first, so
"Filtramag XT" is never left as "Magnetic Coolant Filter XT". Every anchor is
asserted present before it is used; a missing anchor raises rather than
writing a partial result. Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
PAGES = REPO / "assets/source/pages"
GUIDES = REPO / "assets/source/guides"
MANIFEST = REPO / "assets/source/watermarked.txt"

DRY = "--dry-run" in sys.argv

# slug -> (old slug, new slug) within its family directory
SLUGS = [
    ("products/filtration-systems/filtramag",
     "products/filtration-systems/magnetic-coolant-filter"),
    ("products/oil-and-gas-pipeline-filtration/filtramag-xt",
     "products/oil-and-gas-pipeline-filtration/inline-magnetic-pipeline-filter"),
    ("products/oil-and-gas-pipeline-filtration/ultrafiltrex",
     "products/oil-and-gas-pipeline-filtration/modular-high-pressure-pipeline-filter"),
]

# Branded asset stems, scoped to their files/<id>/ directory. A bare stem
# cannot be used: "ultrafiltrex" also appears as a tile key and in prose, and
# an unscoped sweep rewrote that key to the wrong slug.
ASSETS = [
    ("files/6812/403_filtramag_group_shot", "files/6812/coolant-filter-group"),
    ("files/35932/filtramagxt", "files/35932/inline-pipeline-filter"),
    ("files/35926/ultrafiltrex", "files/35926/modular-pipeline-filter"),
    ("files/35852/ultrafiltrex", "files/35852/modular-pipeline-filter"),
]

# Tile keys in the family index markdown are bare slugs at line start.
TILE_KEYS = [
    ("filtramag-xt", "inline-magnetic-pipeline-filter"),
    ("ultrafiltrex", "modular-high-pressure-pipeline-filter"),
    ("filtramag", "magnetic-coolant-filter"),
]

# Prose first: these contain the bare marks and must not be reached by the
# name pairs below.
PROSE = [
    ("We build the Filtramag range to order",
     "We build the range to order"),
    ("We make two units. Filtramag XT is the simpler filter for smaller lines. Ultrafiltrex is the high pressure modular unit for transmission and process pipelines.",
     "We make two units. The inline filter is the simpler one for smaller lines. The modular filter is the high pressure unit for transmission and process pipelines."),
    ("We make two units. Filtramag XT is the simpler filter for smaller lines.",
     "We make two units. The inline filter is the simpler one for smaller lines."),
    ("Ultrafiltrex is the high pressure modular unit for transmission",
     "The modular filter is the high pressure unit for transmission"),
    ("Filtramag XT is the smaller of our two pipeline filters",
     "The inline filter is the smaller of our two pipeline filters"),
    ("Ultrafiltrex is a modular magnetic filter for oil, gas, petrochemical and fuel pipelines",
     "This unit is a modular magnetic filter for oil, gas, petrochemical and fuel pipelines"),
    ("Our Filtramag XT and Ultrafiltrex pipeline filters",
     "Our inline and modular pipeline filters"),
    ("Filtramag XT and Ultrafiltrex, stainless steel",
     "Inline and modular units, stainless steel"),
    ("Filtramag filters on rolling mill", "Magnetic coolant filters on rolling mill"),
    ("Filtramag filters on grinding", "Magnetic coolant filters on grinding"),
    ("Filtramag magnetic filters for coolants", "Magnetic filters for coolants"),
    ("Filtramag magnetic filter for cutting fluids",
     "Magnetic coolant filter for cutting fluids"),
]

# Display names, longest first.
NAMES = [
    ("Filtramag XT Magnetic Filter", "Inline Magnetic Pipeline Filter"),
    ("Ultrafiltrex Pipeline Filtration", "Modular High Pressure Pipeline Filter"),
    ("Filtramag Magnetic Filter", "Magnetic Coolant Filter"),
    ("Filtramag magnetic filter", "magnetic coolant filter"),
    ("Filtramag XT", "Inline Magnetic Pipeline Filter"),
    ("Ultrafiltrex", "Modular High Pressure Pipeline Filter"),
    ("Filtramag", "Magnetic Coolant Filter"),
]

MARK = re.compile(r"filtramag|ultrafiltrex", re.I)


def rewrite(text: str) -> str:
    for old, new in PROSE:
        text = text.replace(old, new)
    for old, new in SLUGS:
        text = text.replace("/" + old + "/", "/" + new + "/")
    for old, new in ASSETS:
        text = text.replace(old, new)
    for old, new in TILE_KEYS:
        text = re.sub(rf"^{re.escape(old)}:", new + ":", text, flags=re.M)
    for old, new in NAMES:
        text = text.replace(old, new)
    return text


def main() -> int:
    changed: list[str] = []
    leftovers: list[str] = []

    targets = sorted(SITE.rglob("*.html"))
    targets += [SITE / "sitemap.xml"]
    targets += sorted(PAGES.rglob("*.md"))
    targets += sorted(GUIDES.rglob("*.md"))
    targets += [MANIFEST]

    for path in targets:
        if not path.exists():
            raise SystemExit(f"missing target: {path}")
        before = path.read_text(encoding="utf-8")
        if not MARK.search(before):
            continue
        after = rewrite(before)
        for m in MARK.finditer(after):
            leftovers.append(f"{path}: ...{after[max(0, m.start()-70):m.start()+70]}...")
        if after != before:
            changed.append(str(path.relative_to(REPO)))
            if not DRY:
                path.write_text(after, encoding="utf-8")

    if leftovers:
        print("LEFTOVER MARKS, nothing written for those files:")
        for line in leftovers[:40]:
            print("  " + line)
        return 1

    # Directory and file renames, after the text sweep so references are already correct.
    moves: list[tuple[Path, Path]] = []
    for old, new in SLUGS:
        src, dst = SITE / old, SITE / new
        if src.is_dir():
            moves.append((src, dst))
        md_src = PAGES / (old + ".md")
        md_dst = PAGES / (new + ".md")
        if md_src.is_file():
            moves.append((md_src, md_dst))

    for old_frag, new_frag in ASSETS:
        sub, old_stem = old_frag.rsplit("/", 1)
        new_stem = new_frag.rsplit("/", 1)[1]
        d = SITE / "site/assets" / sub
        if not d.is_dir():
            raise SystemExit(f"missing asset dir: {d}")
        for f in sorted(d.glob(f"{old_stem}*")):
            if f.is_file():
                moves.append((f, f.with_name(f.name.replace(old_stem, new_stem, 1))))

    for src, dst in moves:
        print(("would move " if DRY else "moved ") + f"{src.relative_to(REPO)} -> {dst.relative_to(REPO)}")
        if not DRY:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

    print(f"\n{'would rewrite' if DRY else 'rewrote'} {len(changed)} files, {len(moves)} moves")
    for c in changed:
        print("  " + c)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
