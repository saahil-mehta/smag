#!/usr/bin/env python3
"""Split the catalogue into work files a translator can take one at a time.

Writes assets/source/i18n/work/<group>-NN.json, each a list of
{"id", "en", "page"} in the order the segments first appear, cut at about
1,600 words so a part is a comfortable single sitting. A translator writes
assets/source/i18n/<lang>/<group>-NN.json as {"id": "translation"}.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/saahil/Documents/GitHub/smag/assets/source/i18n")
WORDS = 1600


def main() -> int:
    cat = json.loads((ROOT / "catalogue.json").read_text(encoding="utf-8"))
    work = ROOT / "work"
    work.mkdir(exist_ok=True)
    for old in work.glob("*.json"):
        old.unlink()
    for group in ("site", "guides"):
        parts, cur, words = [], [], 0
        for e in (e for e in cat if e["group"] == group):
            cur.append({"id": e["id"], "en": e["en"], "page": e["page"]})
            words += len(e["en"].split())
            if words >= WORDS:
                parts.append(cur)
                cur, words = [], 0
        if cur:
            parts.append(cur)
        for n, part in enumerate(parts, 1):
            (work / f"{group}-{n:02d}.json").write_text(
                json.dumps(part, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  {group}: {len(parts)} parts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
