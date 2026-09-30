#!/usr/bin/env python3
"""Check a language's translations against the catalogue.

    check.py <lang> [<group>-NN ...]

For each work part named (default: every part that has a translation file)
it reports segments that are missing, placeholders that do not match the
English, numbers that went missing, em dashes, and segments that are mostly
Latin letters where the English was a sentence (likely left untranslated).
Exit status is 1 if anything is wrong.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/saahil/Documents/GitHub/smag/assets/source/i18n")
PH = re.compile(r"\{/?\d+/?\}")
NUM = re.compile(r"\d(?:[\d,.]*\d)?")
SCRIPT = {"hi": "ऀ-ॿ", "mr": "ऀ-ॿ", "gu": "઀-૿",
          "kn": "ಀ-೿", "te": "ఀ-౿", "ml": "ഀ-ൿ",
          "ta": "஀-௿"}


def main() -> int:
    lang, names = sys.argv[1], sys.argv[2:]
    native = re.compile(f"[{SCRIPT[lang]}]")
    if not names:
        names = sorted(p.stem for p in (ROOT / lang).glob("*-[0-9][0-9].json"))
    bad = 0
    for name in names:
        work = json.loads((ROOT / "work" / f"{name}.json").read_text(encoding="utf-8"))
        path = ROOT / lang / f"{name}.json"
        tr = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        problems = []
        for e in work:
            en, t = e["en"], tr.get(e["id"])
            if t is None:
                problems.append(f"missing  {e['id']}  {en[:60]!r}")
                continue
            if Counter(PH.findall(en)) != Counter(PH.findall(t)):
                problems.append(f"placeholders  {e['id']}  {PH.findall(en)} vs {PH.findall(t)}")
            lost = Counter(NUM.findall(en)) - Counter(NUM.findall(t))
            if lost:
                problems.append(f"numbers  {e['id']}  lost {sorted(lost)}")
            if "—" in t:
                problems.append(f"em dash  {e['id']}")
            words = re.findall(r"[A-Za-z]{2,}", PH.sub("", en))
            if len(words) >= 4 and not native.search(t):
                problems.append(f"untranslated?  {e['id']}  {t[:60]!r}")
        extra = set(tr) - {e["id"] for e in work}
        if extra:
            problems.append(f"unknown ids: {sorted(extra)[:5]}")
        print(f"{lang} {name}: {len(work) - sum(p.startswith('missing') for p in problems)}/{len(work)} done, "
              f"{len(problems)} problems")
        for p in problems[:40]:
            print("   ", p)
        bad += len(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
