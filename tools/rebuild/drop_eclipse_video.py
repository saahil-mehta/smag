#!/usr/bin/env python3
"""Remove the Eclipse video that survived the debrand.

  - home page: the hero slide that autoplayed Eclipse's company video
    (SMAG's own lifter clip on the first slide stays; its master is in
    assets/source/hero-lifter-master.mp4)
  - filtration index: the YouTube embed of the Autofiltrex overview, an
    Eclipse product SMAG does not sell, together with the CNC-filter text
    block beside it
  - the eight orphaned Eclipse mp4 files under files/ (about 130 MB)

The mirror never held any product gifs: two were referenced on the old
grid pages and neither file was fetched, so there is nothing to keep.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
ECLIPSE_MP4 = ("company_video_final.mp4", "banner_video_-_ule_lifter_1700px_x_675px.mp4")


def remove_container(text: str, needle: str, container_re: str) -> tuple[str, int]:
    """Remove the innermost `container_re` element that contains `needle`."""
    i = text.find(needle)
    if i < 0:
        return text, 0
    best = None
    for m in re.finditer(container_re, text[:i]):
        end = find_element_end(text, m.start())
        if end and end > i and (best is None or m.start() > best[0]):
            best = (m.start(), end)
    if not best:
        raise ValueError(f"no container for {needle}")
    return text[: best[0]] + text[best[1]:], 1


def main() -> None:
    dry = "--dry-run" in sys.argv
    home = SITE / "index.html"
    text = home.read_text(encoding="utf-8")
    text, n = remove_container(text, "company_video_final.mp4",
                               r'<div class="?swiper-slide\b[^>]*>')
    print(f"home: {n} video slide removed")
    if not dry and n:
        home.write_text(text, encoding="utf-8")

    filt = SITE / "products/filtration-systems/index.html"
    text = filt.read_text(encoding="utf-8")
    text, n = remove_container(text, "youtube-nocookie.com/embed",
                               r'<div class="?row\b[^>]*>')
    print(f"filtration: {n} YouTube row removed")
    if not dry and n:
        filt.write_text(text, encoding="utf-8")

    files = [p for p in SITE.rglob("*.mp4") if p.name in ECLIPSE_MP4]
    size = sum(p.stat().st_size for p in files) / 1e6
    print(f"{len(files)} Eclipse mp4 files ({size:.0f} MB) {'would be' if dry else ''} deleted")
    if not dry:
        for p in files:
            p.unlink()
    left = sum(1 for p in SITE.rglob("*.html")
               if re.search(r"youtube|vimeo|company_video|ule_lifter",
                            p.read_text(encoding="utf-8")))
    print(f"pages still referencing Eclipse video: {left}")


if __name__ == "__main__":
    main()
