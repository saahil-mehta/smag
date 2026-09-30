#!/usr/bin/env python3
"""Collect every translatable segment of the English site into one catalogue.

Writes assets/source/i18n/catalogue.json: one entry per distinct segment, in
the order it first appears, with the page it first appears on and how many
pages use it. Translators work from this file; build.py reads it back.

Pages are grouped so the work can be split: "site" is everything a buyer
reads (home, products, industries, about, contact, sitemap, 404), "guides" is
the 22 guides. The two policies stay in English.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import segments as S  # noqa: E402

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
OUT = REPO / "assets/source/i18n/catalogue.json"
SKIP = ("information/",)
LANGS = ("hi", "mr", "gu", "kn", "te", "ml", "ta")


def pages() -> list[Path]:
    out = []
    for p in sorted(SITE.rglob("*.html")):
        rel = p.relative_to(SITE).as_posix()
        if rel.startswith(SKIP) or rel.split("/")[0] in LANGS or rel.startswith("site/"):
            continue
        out.append(p)
    return out


def group(rel: str) -> str:
    return "guides" if rel.startswith("resources/guides/") and rel != "resources/guides/index.html" else "site"


def page_segments(text: str):
    """Every (placeholder text, kind) on a page: body runs and attributes."""
    toks, found = S.segments(text)
    for a, b in found:
        yield S.segment_text(toks[a:b])[1]
    for kind, raw, name in toks:
        if kind == "tag" and not raw.startswith("</"):
            for _, v in S.attr_segments(raw):
                yield v.strip()


def main() -> int:
    cat: dict[str, dict] = {}
    for p in pages():
        rel = p.relative_to(SITE).as_posix()
        seen = set()
        for text in page_segments(p.read_text(encoding="utf-8")):
            k = S.key_of(text)
            if k in seen:
                continue
            seen.add(k)
            e = cat.setdefault(k, {"id": k, "en": text, "page": rel, "group": group(rel), "pages": 0})
            e["pages"] += 1
            if group(rel) == "site":
                e["group"] = "site"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(list(cat.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    for g in ("site", "guides"):
        es = [e for e in cat.values() if e["group"] == g]
        print(f"  {g:7s} {len(es):5d} segments {sum(len(e['en'].split()) for e in es):6d} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
