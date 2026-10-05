#!/usr/bin/env python3
"""Bold address labels and Google Maps links, in the footer and on Contact Us.

Client request of 5 Oct 2026. "Factory" and "Registered Office" are set in
<strong> (smag.css gives them full bold; the theme's strong is 500), and each
address opens a Google Maps search for itself in a new tab. Run after
update_contact_details.py.

English pages only. Run `make i18n-extract`, carry the address translations
over to their new ids, then `make i18n`.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote_plus

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
LANGS = {"hi", "mr", "gu", "kn", "te", "ml", "ta"}

FACTORY = ("026 / 117, Sarita Indl Estate, A Wing", "Prabhat Complex, Near Toll Plaza",
           "W E Highway, Dahisar East", "Mumbai, Maharashtra 400068")
OFFICE = ("205, Devraj Mall, Hari Shankar Joshi Road", "Opp. Madhuram Hall, Maratha Colony",
          "Dahisar East, Mumbai, Maharashtra 400068")

FACTORY_QUERY = "Santosh Magnetic Works, Sarita Industrial Estate, Dahisar East, Mumbai 400068"
OFFICE_QUERY = "Devraj Mall, Hari Shankar Joshi Road, Dahisar East, Mumbai 400068"


def maps(query: str) -> str:
    return f"https://www.google.com/maps/search/?api=1&amp;query={quote_plus(query)}"


def link(query: str, body: str) -> str:
    return f'<a href="{maps(query)}" target=_blank rel="noopener noreferrer">{body}</a>'


FOOTER_OLD = (
    "<strong>Factory</strong><br>" + "<br>".join(FACTORY) + "<br>India<br><br>"
    "<strong>Registered Office</strong><br>" + "<br>".join(OFFICE) + "<br>India<br><br>"
)
FOOTER_NEW = (
    "<strong>Factory</strong><br>" + link(FACTORY_QUERY, "<br>".join(FACTORY) + "<br>India") + "<br><br>"
    "<strong>Registered Office</strong><br>" + link(OFFICE_QUERY, "<br>".join(OFFICE) + "<br>India") + "<br><br>"
)

CONTACT_OLD = (
    "<p>Factory<address>" + ", ".join(FACTORY) + ", India</address>"
    "<p>Registered Office<address>" + ", ".join(OFFICE) + ", India</address>"
)
CONTACT_NEW = (
    "<p><strong>Factory</strong><address>" + link(FACTORY_QUERY, ", ".join(FACTORY) + ", India") + "</address>"
    "<p><strong>Registered Office</strong><address>" + link(OFFICE_QUERY, ", ".join(OFFICE) + ", India") + "</address>"
)


def main() -> None:
    pages = [p for p in sorted(SITE.rglob("*.html"))
             if p.relative_to(SITE).parts[0] not in LANGS]

    contact = SITE / "contact-us/index.html"
    text = contact.read_text(encoding="utf-8")
    if text.count(CONTACT_OLD) != 1:
        raise SystemExit(f"contact: expected one address block, found {text.count(CONTACT_OLD)}")
    contact.write_text(text.replace(CONTACT_OLD, CONTACT_NEW), encoding="utf-8")

    footers = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        if FOOTER_OLD in text:
            page.write_text(text.replace(FOOTER_OLD, FOOTER_NEW), encoding="utf-8")
            footers += 1
    missed = [p.relative_to(SITE) for p in pages
              if "<strong>Factory</strong><br>026" in p.read_text(encoding="utf-8")]
    print(f"{footers} footers linked, contact page linked")
    if missed:
        raise SystemExit(f"unlinked footer on: {missed[:5]}")


if __name__ == "__main__":
    main()
