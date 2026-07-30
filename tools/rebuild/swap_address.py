#!/usr/bin/env python3
"""Replace the Eclipse footer postal address with SMAG's, across site/.

Five regional variants exist (UK, FR, North America, CN, DE); all five are
replaced with the single Mumbai address. The UK variant also carries
Eclipse's registered company number in the same element, so SMAG's GSTIN
takes its place.

Reversible: every page is otherwise byte-identical to reference-mirror/.
"""
from __future__ import annotations

import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

NEW = (
    "Santosh Magnetic Works<br>"
    "026 / 177, Sarita Indl Estate, A Wing<br>"
    "Prabhat Complex, Near Toll Plaza<br>"
    "W E Highway, Dahisar East<br>"
    "Mumbai, Maharashtra 400068<br>"
    "India<br><br>"
    "GSTIN 27ABDFS2378H1ZY"
)

OLD = [
    # UK, incl. registered company number
    "Eclipse Magnetics Ltd<br>Atlas Way<br>Sheffield<br>S4 7QQ<br>UK<br><br>"
    "Registered Company Number: 531327",
    # Germany: UK premises, localised country label
    "Eclipse Magnetics Ltd<br>Atlas Way<br>Sheffield<br>S4 7QQ<br>"
    "Vereinigtes Königreich",
    # France
    "Eclipse Magnetics Ltd<br>BP7 59239<br>Thumeries<br>France",
    # North America
    "Eclipse Magnetics North America<br>442 Millen Road, Unit 9<br>"
    "Stoney Creek, ON<br>L8E 6H2",
    # China
    "宝禾易克仪器（上海）有限"
    "公司<br>上海市闵行区梅陇镇<br>"
    "澄建路178号8号楼<br>201108",
]


def main() -> None:
    counts = {o: 0 for o in OLD}
    files = 0

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (not utf-8): {page.relative_to(SITE)}")
            continue

        original = text
        for old in OLD:
            n = text.count(old)
            if n:
                text = text.replace(old, NEW)
                counts[old] += n

        if text != original:
            page.write_text(text, encoding="utf-8")
            files += 1

    print(f"{files} files rewritten\n")
    for old, n in counts.items():
        print(f"  {n:>4}  {old.split('<br>')[0][:44]}")
    print(f"  {sum(counts.values()):>4}  total")

    left = sum(
        p.read_text(encoding="utf-8", errors="replace").count(frag)
        for p in SITE.rglob("*.html")
        for frag in ("Atlas Way", "531327", "Thumeries", "Millen Road")
    )
    # Expected non-zero: contact pages and the privacy/terms pages carry the
    # Eclipse address in body copy, which is a separate job from the footer.
    print(f"\nremaining Eclipse address fragments outside the footer: {left}")


if __name__ == "__main__":
    main()
