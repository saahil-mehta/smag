#!/usr/bin/env python3
"""Restore the Pipeline Filtration family that an earlier sweep removed.

Brings back from the pristine mirror:
  products/oil-and-gas-pipeline-filtration/
    index.html, filtramag-xt/, ultrafiltrex/,
    pipeline-contamination-and-black-powder-formation/
(ditch-magnets and bespoke-solutions stay out of the range)

Because site/ chrome has since been rebranded, each restored page gets its
<header> and <footer> transplanted from a current site page, then the global
cleanup scripts are re-run (they are idempotent) to strip trackers,
testimonials, hreflang rows and Eclipse copy tells from the restored bodies.

The family is then wired back in everywhere: the nav dropdown and the footer
product column on every page, the sitemap page, and the family's own index
grid trimmed to the kept products. Known-missing hero images are repointed at
renditions the mirror does hold.

Run with --dry-run to report without writing (the cleanup re-runs are skipped
in that mode).
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
FAM = "products/oil-and-gas-pipeline-filtration"
KEEP = ["filtramag-xt", "ultrafiltrex",
        "pipeline-contamination-and-black-powder-formation"]
DONOR = SITE / "products/filtration-systems/index.html"

NAV_LIFT = ('<li><a href=/products/lifting-and-handling/ '
            'data-text="Lifting &amp; Handling"> '
            '<span>Lifting &amp; Handling</span> </a>')
NAV_PIPE = ('<li><a href=/products/oil-and-gas-pipeline-filtration/ '
            'data-text="Pipeline Filtration"> '
            '<span>Pipeline Filtration</span> </a>')
FOOT_LIFT = ('<li><a href=/products/lifting-and-handling/>'
             'Lifting &amp; Handling</a>')
FOOT_PIPE = ('<li><a href=/products/oil-and-gas-pipeline-filtration/>'
             'Pipeline Filtration</a>')
SITEMAP_LIFT_END = "</ul>"  # inserted after the lifting block, see below
SITEMAP_PIPE = (
    '<li>&raquo; <a href=/products/oil-and-gas-pipeline-filtration/>'
    "Pipeline Filtration</a><ul>"
    '<li class=no-child>&raquo; <a href=/products/oil-and-gas-pipeline-'
    "filtration/filtramag-xt/>Filtramag XT Magnetic Filter</a>"
    '<li class=no-child>&raquo; <a href=/products/oil-and-gas-pipeline-'
    "filtration/ultrafiltrex/>Ultrafiltrex Pipeline Filtration</a>"
    '<li class=no-child>&raquo; <a href=/products/oil-and-gas-pipeline-'
    "filtration/pipeline-contamination-and-black-powder-formation/>"
    "How Is Black Powder Formed?</a></ul>"
)

# hero renditions the mirror never fetched -> ones it did
IMG_FIXES = [
    (re.compile(r"/site/assets/files/35932/filtramagxt-1\.590x548"
                r"(?:\.\d+x0)?\.jpg"),
     "/site/assets/files/35932/filtramagxt.355x205.jpg"),
    (re.compile(r"/site/assets/files/35932/filtramagxt-1\.1000x0\.jpg"),
     "/site/assets/files/35932/filtramagxt.355x205.jpg"),
    (re.compile(r"/site/assets/files/35926/ultrafiltrex-1\.590x548"
                r"(?:\.\d+x0)?\.jpg"),
     "/site/assets/files/35852/ultrafiltrex.637x481.jpg"),
    (re.compile(r"/site/assets/files/35926/ultrafiltrex-1\.1000x0\.jpg"),
     "/site/assets/files/35852/ultrafiltrex.637x481.jpg"),
]
MISSING_IMG = "/site/assets/files/35951/shutterstock_588495665-1.400x0-is.jpg"

GRID_OPEN = '<div class="grid grid--product-category">'
TILE_OPEN = "<div class=grid__item>"


def element(text: str, open_pat: str) -> tuple[int, int]:
    m = re.search(open_pat, text)
    if not m:
        return -1, -1
    end = find_element_end(text, m.start())
    return (m.start(), end) if end else (-1, -1)


def transplant(text: str, donor: str, tag: str) -> str:
    s, e = element(text, rf"<{tag}\b")
    ds, de = element(donor, rf"<{tag}\b")
    if s < 0 or ds < 0:
        raise SystemExit(f"could not locate <{tag}> for transplant")
    return text[:s] + donor[ds:de] + text[e:]


def strip_img_tag(text: str, src: str) -> str:
    while src in text:
        i = text.find(src)
        a = text.rfind("<img", 0, i)
        e = text.find(">", i)
        if a < 0 or e < 0:
            break
        text = text[:a] + text[e + 1:]
    return text


def main() -> None:
    dry = "--dry-run" in sys.argv
    donor = DONOR.read_text(encoding="utf-8")

    dst = SITE / FAM
    src = MIRROR / FAM
    print(f"restore {FAM}/ (index + {', '.join(KEEP)})")
    if not dry:
        if dst.exists():
            shutil.rmtree(dst)
        dst.mkdir(parents=True)
        shutil.copy2(src / "index.html", dst / "index.html")
        for k in KEEP:
            shutil.copytree(src / k, dst / k)

        # chrome transplant + image fixes on the restored pages
        for page in sorted(dst.rglob("*.html")):
            text = page.read_text(encoding="utf-8")
            text = transplant(text, donor, "header")
            text = transplant(text, donor, "footer")
            for pat, repl in IMG_FIXES:
                text = pat.sub(repl, text)
            text = strip_img_tag(text, MISSING_IMG)
            page.write_text(text, encoding="utf-8")

        # trim the family index grid to the kept products
        page = dst / "index.html"
        text = page.read_text(encoding="utf-8")
        i = text.find(GRID_OPEN)
        end = find_element_end(text, i)
        grid = text[i:end]
        tiles: dict[str, str] = {}
        for m in re.finditer(re.escape(TILE_OPEN), grid):
            te = find_element_end(grid, m.start())
            tile = grid[m.start():te]
            a = re.search(rf"href=/{re.escape(FAM)}/([a-z0-9-]+)/", tile)
            if a:
                tiles[a.group(1)] = tile
        kept = [tiles[s] for s in KEEP if s in tiles]
        print(f"  index grid: kept {len(kept)} of {len(tiles)} tiles")
        text = text[:i] + GRID_OPEN + "".join(kept) + "</div>" + text[end:]
        page.write_text(text, encoding="utf-8")

    # wire the family into every page's nav + footer, and the sitemap
    navs = feet = 0
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        orig = text
        if NAV_PIPE not in text and NAV_LIFT in text:
            navs += text.count(NAV_LIFT)
            text = text.replace(NAV_LIFT, NAV_LIFT + NAV_PIPE)
        if FOOT_PIPE not in text and FOOT_LIFT in text:
            feet += text.count(FOOT_LIFT)
            text = text.replace(FOOT_LIFT, FOOT_LIFT + FOOT_PIPE)
        if text != orig and not dry:
            page.write_text(text, encoding="utf-8")
    print(f"nav items added: {navs}, footer items added: {feet}")

    smap = SITE / "sitemap/index.html"
    text = smap.read_text(encoding="utf-8")
    if "oil-and-gas-pipeline-filtration/>Pipeline Filtration</a><ul>" not in \
            text.replace("\n", ""):
        anchor = re.search(
            r"<li>&raquo; <a href=/products/lifting-and-handling/>", text)
        if anchor:
            end = text.find("</ul>", anchor.start()) + len("</ul>")
            text = text[:end] + SITEMAP_PIPE + text[end:]
            print("sitemap: pipeline block inserted")
            if not dry:
                smap.write_text(text, encoding="utf-8")

    # re-run the idempotent global cleanups over the restored pages
    if not dry:
        here = Path(__file__).resolve().parent
        for script in ["strip_trackers.py", "remove_sections.py",
                       "remove_testimonials.py", "copy_edit.py"]:
            print(f"-- re-running {script}")
            subprocess.run([sys.executable, str(here / script)], check=True,
                           capture_output=True)


if __name__ == "__main__":
    main()
