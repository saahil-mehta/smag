#!/usr/bin/env python3
"""Retire the Eclipse Free Quote page and send its callers to Contact Us.

/free-quote/ was an Eclipse shell around an iframe of /form-builder/quote/,
a ProcessWire form endpoint the crawl never captured and that a static host
cannot serve. The page rendered a heading over an empty frame. SMAG's
enquiry form lives on /contact-us/ (refurb_contact.py), so every link to
the quote page, including the sticky "Get a FREE Quote" call-to-action on
77 pages, now points there with a plainer label. The quote page and the
form-builder leftovers are deleted.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
DROP = ["free-quote", "form-builder"]
SWAPS = [
    ("href=/free-quote/", "href=/contact-us/"),
    ("<span>Get a FREE Quote</span>", "<span>Get a quote</span>"),
]


def main() -> None:
    dry = "--dry-run" in sys.argv
    files = 0
    for page in sorted(SITE.rglob("*.html")):
        if any(str(page).startswith(str(SITE / d)) for d in DROP):
            continue
        text = orig = page.read_text(encoding="utf-8")
        for old, new in SWAPS:
            text = text.replace(old, new)
        if text != orig:
            files += 1
            if not dry:
                page.write_text(text, encoding="utf-8")
    print(f"{'DRY RUN: ' if dry else ''}{files} pages repointed")
    for d in DROP:
        p = SITE / d
        if p.exists():
            print(f"  {'would delete' if dry else 'deleted'} {d}/")
            if not dry:
                shutil.rmtree(p)
    left = sum("free-quote" in p.read_text(encoding="utf-8")
               for p in SITE.rglob("*.html"))
    print(f"residual free-quote references: {left}")


if __name__ == "__main__":
    main()
