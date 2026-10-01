#!/usr/bin/env python3
"""Point every guide card at the photo its source names, one photo per guide.

The image: line in assets/source/guides/<slug>.md names a still in
assets/source/brochure-stills/. This renders that still as the guide's card
on /resources/guides/ (and as its home carousel slide when home: true) with
build_guides.card(), then swaps the card's img src in the built pages. It
only touches card images, so the later passes on those pages (design layer,
language menu) stay as they are. It stops if two guides name the same photo.

Stills named scene-*.png are generated scenes (Codex, Oct 2026) for guides
with no matching SMAG photograph: pipeline, coolant and chain lifting.

Run with --dry-run to report without writing. Then make i18n.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_guides as G  # noqa: E402

DRY = "--dry-run" in sys.argv
INDEX = G.GUIDES / "index.html"


def swap(text: str, slug: str, url: str, width: int) -> str:
    card = re.compile(rf"(<a href=/resources/guides/{slug}/>.*?<img src=)(\S+)( width={width} )", re.S)
    found = card.search(text)
    if not found:
        raise ValueError(f"no {width}px card for {slug}")
    return text[:found.start(2)] + url + text[found.end(2):]


def main() -> None:
    guides = [G.load(p) for p in sorted(G.SRC.glob("*.md"))]
    shared = [s for s, n in Counter(g["image"] for g in guides).items() if n > 1]
    if shared:
        raise SystemExit(f"photo used by more than one guide: {', '.join(shared)}")
    index, home = INDEX.read_text(encoding="utf-8"), G.HOME.read_text(encoding="utf-8")
    new_index, new_home = index, home
    for g in guides:
        stem, slug = g["image"], g["slug"]
        if f"/{stem}.card.jpg" not in new_index.split(f"/resources/guides/{slug}/>", 1)[1][:400]:
            print(f"{slug}: card -> {stem}")
            if not DRY:
                new_index = swap(new_index, slug, G.card(stem, "card", 315, 247), 315)
        if g["home"] and f"/{stem}.home.jpg" not in new_home.split(f"/resources/guides/{slug}/>", 1)[1][:400]:
            print(f"{slug}: home slide -> {stem}")
            if not DRY:
                new_home = swap(new_home, slug, G.card(stem, "home", 350, 370), 350)
    if not DRY:
        if new_index != index:
            INDEX.write_text(new_index, encoding="utf-8")
        if new_home != home:
            G.HOME.write_text(new_home, encoding="utf-8")


if __name__ == "__main__":
    main()
