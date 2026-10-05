#!/usr/bin/env python3
"""Client corrections of 5 Oct 2026 to the contact details and the About team.

- Factory unit number 026 / 177 becomes 026 / 117 (the ISO certificate also
  reads Unit No 117).
- The registered office at Devraj Mall is added below the factory address,
  in the footer, on the contact page and in the privacy policy.
- WhatsApp links move to the company WhatsApp number, +91 93245 87891. The
  call numbers stay as they are.
- The About team names get the salutation "Mr.".

English pages only. Run `make i18n-extract`, translate the new segments,
then `make i18n` to carry the change into the language copies.
"""
from __future__ import annotations

from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
LANGS = {"hi", "mr", "gu", "kn", "te", "ml", "ta"}

FACTORY_LINES = (
    "026 / 117, Sarita Indl Estate, A Wing",
    "Prabhat Complex, Near Toll Plaza",
    "W E Highway, Dahisar East",
    "Mumbai, Maharashtra 400068",
)
OFFICE_LINES = (
    "205, Devraj Mall, Hari Shankar Joshi Road",
    "Opp. Madhuram Hall, Maratha Colony",
    "Dahisar East, Mumbai, Maharashtra 400068",
)

FOOTER_OLD = (
    "<p class=address>Santosh Magnetic Works<br>"
    "026 / 177, Sarita Indl Estate, A Wing<br>Prabhat Complex, Near Toll Plaza<br>"
    "W E Highway, Dahisar East<br>Mumbai, Maharashtra 400068<br>India<br><br>"
)
FOOTER_NEW = (
    "<p class=address>Santosh Magnetic Works<br><br>"
    "<strong>Factory</strong><br>" + "<br>".join(FACTORY_LINES) + "<br>India<br><br>"
    "<strong>Registered Office</strong><br>" + "<br>".join(OFFICE_LINES) + "<br>India<br><br>"
)

POLICY_OLD = (
    "<p>Santosh Magnetic Works<br>026 / 177, Sarita Indl Estate, A Wing, Prabhat Complex, "
    "Near Toll Plaza, W E Highway, Dahisar East, Mumbai, Maharashtra 400068, India<br>"
)
POLICY_NEW = (
    "<p>Santosh Magnetic Works<br>"
    "Factory: " + ", ".join(FACTORY_LINES) + ", India<br>"
    "Registered Office: " + ", ".join(OFFICE_LINES) + ", India<br>"
)

CONTACT_OLD = (
    "<p><strong>Santosh Magnetic Works</strong><address>026 / 177, Sarita Indl Estate, "
    "A Wing, Prabhat Complex, Near Toll Plaza, W E Highway, Dahisar East, Mumbai, "
    "Maharashtra 400068, India</address>"
)
CONTACT_NEW = (
    "<p><strong>Santosh Magnetic Works</strong>"
    "<p>Factory<address>" + ", ".join(FACTORY_LINES) + ", India</address>"
    "<p>Registered Office<address>" + ", ".join(OFFICE_LINES) + ", India</address>"
)

WHATSAPP_OLD = "https://wa.me/919920143922"
WHATSAPP_NEW = "https://wa.me/919324587891"
CONTACT_WA_OLD = f'<a href="{WHATSAPP_OLD}" target=_blank rel="noopener noreferrer">Message us on WhatsApp</a>'
CONTACT_WA_NEW = f'<a href="{WHATSAPP_NEW}" target=_blank rel="noopener noreferrer">+91 93245 87891</a>'

TEAM = ("Sushil", "Rahul", "Santosh", "Mandar", "Vijay", "Deepak")


def replace_once(text: str, old: str, new: str, where: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{where}: expected one {old[:60]!r}, found {text.count(old)}")
    return text.replace(old, new)


def main() -> None:
    pages = [p for p in sorted(SITE.rglob("*.html"))
             if p.relative_to(SITE).parts[0] not in LANGS]

    contact = SITE / "contact-us/index.html"
    text = contact.read_text(encoding="utf-8")
    text = replace_once(text, CONTACT_OLD, CONTACT_NEW, "contact")
    text = replace_once(text, CONTACT_WA_OLD, CONTACT_WA_NEW, "contact")
    contact.write_text(text, encoding="utf-8")

    policy = SITE / "information/privacy-policy/index.html"
    text = policy.read_text(encoding="utf-8")
    policy.write_text(replace_once(text, POLICY_OLD, POLICY_NEW, "privacy policy"), encoding="utf-8")

    about = SITE / "company/about-us/index.html"
    text = about.read_text(encoding="utf-8")
    for name in TEAM:
        text = replace_once(text, f"<h3>{name} Ingle</h3>", f"<h3>Mr. {name} Ingle</h3>", "about")
    about.write_text(text, encoding="utf-8")

    footers = links = 0
    for page in pages:
        text = page.read_text(encoding="utf-8")
        new = text.replace(FOOTER_OLD, FOOTER_NEW)
        footers += text.count(FOOTER_OLD)
        links += new.count(WHATSAPP_OLD)
        new = new.replace(WHATSAPP_OLD, WHATSAPP_NEW)
        if new != text:
            page.write_text(new, encoding="utf-8")

    left = [p.relative_to(SITE) for p in pages
            if "026 / 177" in (t := p.read_text(encoding="utf-8")) or WHATSAPP_OLD in t]
    print(f"{footers} footers, {links} WhatsApp links, contact page, privacy policy, About team")
    if left:
        raise SystemExit(f"old details still on: {left[:5]}")


if __name__ == "__main__":
    main()
