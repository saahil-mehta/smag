#!/usr/bin/env python3
"""Make the company number, +91 93245 87891, the main call number.

Client decision of 5 Oct 2026. The header call button, footer and closing
action band move from +91 99201 43922 to the company number. The contact
page lists the numbers in the client's order: 93245 87891, 93243 15562,
99201 43922, 82861 93555.

English pages only. Run `make i18n-extract`, translate the header button's
new aria-label, then `make i18n`.
"""
from __future__ import annotations

from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
LANGS = {"hi", "mr", "gu", "kn", "te", "ml", "ta"}

OLD_TEL, NEW_TEL = "tel:+919920143922", "tel:+919324587891"
OLD_SHOWN, NEW_SHOWN = "+91 99201 43922", "+91 93245 87891"

BROCHURE_LINE = '<p><i class="fas fa-phone fa-fw"></i> <a href="tel:+919324315562">+91 93243 15562</a>'
OLD_LINE = f'<p><i class="fas fa-phone fa-fw"></i> <a href="{OLD_TEL}">{OLD_SHOWN}</a>'


def main() -> None:
    pages = [p for p in sorted(SITE.rglob("*.html"))
             if p.relative_to(SITE).parts[0] not in LANGS]

    changed = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        new = text.replace(OLD_TEL, NEW_TEL).replace(OLD_SHOWN, NEW_SHOWN)
        if new != text:
            page.write_text(new, encoding="utf-8")
            changed += 1

    contact = SITE / "contact-us/index.html"
    text = contact.read_text(encoding="utf-8")
    if text.count(BROCHURE_LINE) != 1:
        raise SystemExit(f"contact: expected one 93243 15562 line, found {text.count(BROCHURE_LINE)}")
    contact.write_text(text.replace(BROCHURE_LINE, BROCHURE_LINE + OLD_LINE), encoding="utf-8")

    left = [p.relative_to(SITE) for p in pages
            if p != contact and OLD_SHOWN in p.read_text(encoding="utf-8")]
    print(f"{changed} pages moved to {NEW_SHOWN}; {OLD_SHOWN} kept third on the contact page")
    if left:
        raise SystemExit(f"old number still on: {left[:5]}")


if __name__ == "__main__":
    main()
