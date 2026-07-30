#!/usr/bin/env python3
"""Refurbish the contact page for SMAG.

Four changes to <main>:

  1. Banner image: Eclipse's Sheffield photo -> SMAG's own factory-team shot,
     cropped to the two ratios the <picture> element asks for.
  2. Intro copy rewritten for SMAG.
  3. The form: Eclipse's <iframe src=/form-builder/contact_us/> is a
     ProcessWire endpoint that cannot exist on static hosting. Replaced with a
     real inline form posting to Web3Forms, reusing the access key from SMAG's
     own pre-takedown contact page (commit 6e952db^). Built with the mirror's
     native Inputfield classes so it inherits the site's existing form styling
     rather than needing new CSS.
  4. Locations: Eclipse's four offices -> SMAG's single Mumbai works, with all
     three phone numbers, email, WhatsApp and a directions link.

Applied to both copies of the page (contact-us.html and contact-us/index.html),
which differ only in their Cloudflare email obfuscation keys.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

PAGES = ["contact-us.html", "contact-us/index.html"]

EMAIL = "queries@santoshmagneticworks.com"
PHONES = [
    ("+91 99201 43922", "+919920143922"),
    ("+91 93243 15562", "+919324315562"),
    ("+91 82861 93555", "+918286193555"),
]
WHATSAPP = "https://wa.me/919920143922"
DIRECTIONS = "https://share.google/9DQHs89BFmkKijKhb"
INDIAMART = "https://www.indiamart.com/santosh-magnetic-works/"
WEB3FORMS_KEY = "54d3356e-73b2-40ba-ac62-a74fdb5e9032"

BANNER = (
    '<picture> '
    '<source src=/site/assets/images/contact-banner.jpg '
    'media="(min-width: 768px)" '
    'alt="The Santosh Magnetic Works team at our Mumbai works">\n'
    '<source src=/site/assets/images/contact-banner-mobile.jpg '
    'alt="The Santosh Magnetic Works team at our Mumbai works">\n'
    '<img src=/site/assets/images/contact-banner-mobile.jpg width=640 height=834 '
    'alt="The Santosh Magnetic Works team at our Mumbai works" /></picture>'
)

INTRO = (
    '<div class=row><div class="row__inner row__intro content content--text_2">'
    "<h2>Tell us what you need to separate, filter, lift or hold.</h2>"
    "<p>Send us the details and we will come back to you with a recommendation "
    "and a quotation. If it is urgent, call or message us on WhatsApp using the "
    "numbers alongside, and you will reach someone at the works."
    "</div></div>"
)


def field(fid, name, label, kind="text", required=False, extra=""):
    """One Inputfield row in the mirror's native structure."""
    cls = f"Inputfield Inputfield_{fid} Inputfield{kind}"
    if required:
        cls += " InputfieldStateRequired"
    req_attr = " required" if required else ""
    inp_cls = '"required InputfieldMaxWidth"' if required else "InputfieldMaxWidth"
    if kind == "Textarea":
        control = (
            f'<textarea class={inp_cls} id=Inputfield_{fid} name={name} '
            f"rows=6{req_attr}></textarea>"
        )
    elif kind == "Select":
        control = (
            f'<select class={inp_cls} id=Inputfield_{fid} name={name}{req_attr}>'
            f"{extra}</select>"
        )
    else:
        itype = {"Email": "email", "Text": "text"}.get(kind, "text")
        if fid == "phone":
            itype = "tel"
        control = (
            f'<input type={itype} class={inp_cls} id=Inputfield_{fid} '
            f'name={name} maxlength=2048{req_attr}{extra}>'
        )
    return (
        f"<div class='{cls}' id=wrap_Inputfield_{fid}>"
        f"<label class=InputfieldHeader for=Inputfield_{fid}>{label}</label>"
        f"<div class=InputfieldContent>{control}</div></div>"
    )


LOCATION_OPTS = (
    "<option value disabled selected>Select...</option>"
    '<option value="Mumbai">Mumbai</option>'
    '<option value="Rest of India">Rest of India</option>'
    '<option value="International">International (export)</option>'
)
ENQUIRY_OPTS = (
    "<option value disabled selected>Select...</option>"
    '<option value="Magnetic separation">Magnetic separation</option>'
    '<option value="Magnetic filtration">Magnetic filtration</option>'
    '<option value="Lifting and handling">Lifting and handling</option>'
    '<option value="Workholding">Workholding</option>'
    '<option value="Spares or servicing">Spares or servicing</option>'
    '<option value="Something else">Something else</option>'
)

FORM = (
    '<div class=contact-detail__form>'
    '<form class="FormBuilderFrameworkBasic FormBuilder InputfieldFormWidths InputfieldForm" '
    'id=FormBuilder_enquiry name=enquiry method=post '
    'action="https://api.web3forms.com/submit">'
    f'<input type=hidden name=access_key value="{WEB3FORMS_KEY}">'
    '<input type=hidden name=subject value="New enquiry from the SMAG website">'
    '<input type=hidden name=from_name value="Santosh Magnetic Works website">'
    # Honeypot: bots fill it, people never see it.
    '<input type=checkbox name=botcheck style="display:none" tabindex="-1" '
    'aria-hidden="true">'
    "<div class=Inputfields>"
    + field("name", "Name", "Your name", "Text", required=True)
    + field("company", "Company", "Company")
    + field("email", "Email", "Email address", "Email", required=True)
    + field("phone", "Phone", "Phone number", "Text", required=True)
    + field("location", "Location", "Where are you based?", "Select",
            required=True, extra=LOCATION_OPTS)
    + field("enquiry", "Enquiry", "What is your enquiry about?", "Select",
            required=True, extra=ENQUIRY_OPTS)
    + field("message", "Message", "Tell us about the application", "Textarea",
            required=True)
    + '<div class="Inputfield Inputfield_submit InputfieldSubmit" id=wrap_submit>'
      "<div class=InputfieldContent>"
      '<button type=submit class=button>Send enquiry</button>'
      "</div></div>"
    "</div></form></div>"
)

phone_lines = "".join(
    f'<p><i class="fas fa-phone fa-fw"></i> <a href="tel:{tel}">{disp}</a>'
    for disp, tel in PHONES
)

LOCATIONS = (
    '<div class=contact-detail__locations>'
    '<h3 class=bordered-header>Our works</h3>'
    '<div class=locations__item><div>'
    "<p><strong>Santosh Magnetic Works</strong>"
    "<address>026 / 177, Sarita Indl Estate, A Wing, Prabhat Complex, "
    "Near Toll Plaza, W E Highway, Dahisar East, Mumbai, Maharashtra 400068, "
    "India</address></div><div>"
    + phone_lines
    + f'<p><i class="fab fa-whatsapp fa-fw"></i> '
      f'<a href="{WHATSAPP}" target=_blank rel="noopener noreferrer">'
      "Message us on WhatsApp</a>"
    + f'<p><i class="fas fa-envelope fa-fw"></i> '
      f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    + f'<p><i class="fas fa-store fa-fw"></i> '
      f'<a href="{INDIAMART}" target=_blank rel="noopener noreferrer">'
      "Our IndiaMART store</a>"
    + f'<p class=c2a><a href="{DIRECTIONS}" target=_blank '
      'rel="noopener noreferrer">Get directions</a>'
      "</div></div></div>"
)

BANNER_PIC_RE = re.compile(r"<picture>.*?</picture>", re.DOTALL)
INTRO_RE = re.compile(
    r'<div class=row><div class="row__inner row__intro content content--text_2">'
    r".*?</div></div>",
    re.DOTALL,
)
DETAIL_RE = re.compile(
    r'(<div class="row__inner contact-detail">).*?(</div></div></div></main>)',
    re.DOTALL,
)
TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
DESC_RE = re.compile(r'<meta name=description content="[^"]*">')


def main() -> None:
    for rel in PAGES:
        page = SITE / rel
        if not page.exists():
            print(f"  MISSING {rel}")
            continue
        text = page.read_text(encoding="utf-8")
        before = len(text)
        ok = True

        text, n = BANNER_PIC_RE.subn(BANNER, text, count=1)
        ok &= bool(n)
        text, n2 = INTRO_RE.subn(INTRO, text, count=1)
        ok &= bool(n2)
        text, n3 = DETAIL_RE.subn(
            lambda m: m.group(1) + FORM + LOCATIONS + m.group(2), text, count=1
        )
        ok &= bool(n3)

        text = TITLE_RE.sub(
            "<title>Contact Us | Santosh Magnetic Works</title>", text
        )
        text = DESC_RE.sub(
            '<meta name=description content="Contact Santosh Magnetic Works in '
            'Mumbai for magnetic separation, filtration, lifting and workholding '
            'equipment. Call, WhatsApp or send an enquiry.">',
            text,
        )

        if not ok:
            print(f"  FAILED to match all blocks in {rel} "
                  f"(banner={n} intro={n2} detail={n3})")
            continue

        page.write_text(text, encoding="utf-8")
        print(f"  ok  {rel}  {before} -> {len(text)} bytes")

    print("\nEclipse traces left in <main>:")
    for rel in PAGES:
        p = SITE / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<main>.*</main>", t, re.DOTALL)
        seg = m.group(0) if m else t
        hits = re.findall(
            r"Eclipse|Sheffield|Atlas Way|Thumeries|Millen|Shanghai|Bowers|"
            r"form-builder|cf_email",
            seg,
        )
        print(f"  {len(hits):>3}  {rel}  {sorted(set(hits))}")


if __name__ == "__main__":
    main()
