#!/usr/bin/env python3
"""Replace the Eclipse footer email/phone and Social column across site/.

Email/phone: 4 regional variants, all sharing one structure. The address is
Cloudflare-obfuscated with a per-page key, so this matches by pattern and
replaces with a plain mailto:, which also drops the page's dependence on
cloudflare-static/email-decode.min.js for the footer to read correctly.

Social: 5 variants (UK, en-us, fr, de, plus cn's empty "scan for WeChat"
column). Each page keeps its own heading, except cn where the heading names
WeChat specifically and no longer applies.

Icons use the locally bundled Font Awesome at site/assets/fontawesome, so
no new external request is introduced.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

EMAIL = "queries@santoshmagneticworks.com"
PHONE_DISPLAY = "+91 99201 43922"
PHONE_TEL = "+919920143922"
WHATSAPP = "https://wa.me/919920143922"
INDIAMART = "https://www.indiamart.com/santosh-magnetic-works/"
GOOGLE = "https://share.google/Yw1YuhYK5C84IgfGQ"

# --- email + phone -------------------------------------------------------

EMAIL_RE = re.compile(
    r'<p class=address><a href="/cdn-cgi/l/email-protection#[0-9a-f]+">'
    r'<i class="fas fa-envelope fa-lg fa-fw"></i> '
    r'<span class="__cf_email__" data-cfemail="[0-9a-f]+">'
    r'\[email&#160;protected\]</span></a><br> '
    r'<i class="fas fa-phone fa-lg fa-fw"></i> [^<]*'
)

EMAIL_NEW = (
    f'<p class=address><a href="mailto:{EMAIL}">'
    '<i class="fas fa-envelope fa-lg fa-fw"></i> '
    f'{EMAIL}</a><br> '
    f'<a href="tel:{PHONE_TEL}">'
    '<i class="fas fa-phone fa-lg fa-fw"></i> '
    f'{PHONE_DISPLAY}</a> '
)

# --- social column -------------------------------------------------------


def social(heading: str) -> str:
    return (
        f"<h6>{heading}</h6><ul>"
        f'<li><a href={WHATSAPP} target=_blank rel=noopener> '
        '<i class="fab fa-lg fa-fw fa-whatsapp"></i>\nWhatsApp </a>'
        f'<li><a href={INDIAMART} target=_blank rel=noopener> '
        '<i class="fas fa-lg fa-fw fa-store"></i>\nIndiaMART </a>'
        f'<li><a href={GOOGLE} target=_blank rel=noopener> '
        '<i class="fab fa-lg fa-fw fa-google"></i>\nGoogle Business </a>'
        "</ul>"
    )


SOCIAL_OLD = [
    # UK / global
    "<h6>Social</h6><ul><li><a href=https://www.facebook.com/EclipseMagnetics/ target=_blank> <i class=\"fab fa-lg fa-fw fa-facebook-f\"></i>\nFacebook </a><li><a href=https://www.linkedin.com/company/eclipse-magnetics-ltd/ target=_blank> <i class=\"fab fa-lg fa-fw fa-linkedin\"></i>\nLinkedIn </a><li><a href=https://www.youtube.com/@EclipseMagnetics target=_blank> <i class=\"fab fa-lg fa-fw fa-youtube\"></i>\nYouTube </a></ul>",
    # North America
    "<h6>Social</h6><ul><li><a href=https://www.facebook.com/EclipseMagneticsNA target=_blank> <i class=\"fab fa-lg fa-fw fa-facebook-f\"></i>\nFacebook </a><li><a href=https://x.com/EclipseMagNA target=_blank> <i class=\"fab fa-lg fa-fw fa-twitter\"></i>\nTwitter </a><li><a href=https://www.linkedin.com/company/eclipsetoolsna target=_blank> <i class=\"fab fa-lg fa-fw fa-linkedin\"></i>\nLinkedIn </a><li><a href=https://www.instagram.com/eclipsemagneticsna/ target=_blank> <i class=\"fab fa-lg fa-fw fa-instagram\"></i>\nInstagram </a></ul>",
    # France
    "<h6>Réseaux sociaux</h6><ul><li><a href=https://www.facebook.com/EclipseMagnetics/ target=_blank> <i class=\"fab fa-lg fa-fw fa-facebook-f\"></i>\nFacebook </a><li><a href=https://x.com/EclipseMagnetic target=_blank> <i class=\"fab fa-lg fa-fw fa-twitter\"></i>\nTwitter </a><li><a href=\"https://www.linkedin.com/company/eclipse-magnetics-ltd/?trk=top_nav_home\" target=_blank> <i class=\"fab fa-lg fa-fw fa-linkedin\"></i>\nLinkedIn </a></ul>",
    # Germany
    "<h6>Soziale Medien</h6><ul><li><a href=https://www.facebook.com/EclipseMagnetics/ target=_blank> <i class=\"fab fa-lg fa-fw fa-facebook-f\"></i>\nFacebook </a><li><a href=https://x.com/EclipseMagnetic target=_blank> <i class=\"fab fa-lg fa-fw fa-twitter\"></i>\nTwitter </a><li><a href=\"https://www.linkedin.com/company/eclipse-magnetics-ltd/?trk=top_nav_home\" target=_blank> <i class=\"fab fa-lg fa-fw fa-linkedin\"></i>\nLinkedIn </a></ul>",
    # China: "scan to add WeChat", empty list (QR never mirrored)
    "<h6>扫一扫，添加微信</h6><ul></ul>",
]

HEADING = {
    SOCIAL_OLD[0]: "Social",
    SOCIAL_OLD[1]: "Social",
    SOCIAL_OLD[2]: "Réseaux sociaux",
    SOCIAL_OLD[3]: "Soziale Medien",
    SOCIAL_OLD[4]: "社交媒体",
}


def main() -> None:
    emails = 0
    socials = {o: 0 for o in SOCIAL_OLD}
    files = 0

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (not utf-8): {page.relative_to(SITE)}")
            continue

        original = text

        text, n = EMAIL_RE.subn(EMAIL_NEW, text)
        emails += n

        for old in SOCIAL_OLD:
            k = text.count(old)
            if k:
                text = text.replace(old, social(HEADING[old]))
                socials[old] += k

        if text != original:
            page.write_text(text, encoding="utf-8")
            files += 1

    print(f"{files} files rewritten")
    print(f"\n  {emails:>4}  email/phone paragraphs")
    for old, n in socials.items():
        print(f"  {n:>4}  social: {HEADING[old]}  ({old[:34]}...)")
    print(f"  {sum(socials.values()):>4}  social total")

    leftovers = {}
    for frag in (
        "eclipsemagnetics.com",
        "114 225 0600",
        "facebook.com/EclipseMagnetics",
        "__cf_email__",
        "linkedin.com/company/eclipse",
        "youtube.com/@EclipseMagnetics",
    ):
        hits = sum(
            p.read_text(encoding="utf-8", errors="replace").count(frag)
            for p in SITE.rglob("*.html")
        )
        leftovers[frag] = hits

    print("\nremaining site-wide (footer and elsewhere):")
    for k, v in leftovers.items():
        print(f"  {v:>5}  {k}")


if __name__ == "__main__":
    main()
