#!/usr/bin/env python3
"""Replace the Eclipse privacy and cookie pages with SMAG boilerplate.

The page chrome (header, footer, CSS, contact CTA) is left exactly as found so
the pages stay native to the site; only the <title>, meta description and the
first content block are rewritten.

Content is written against what the site demonstrably does: a contact form,
enquiry email and phone lines, GST registration implying statutory retention,
and outbound links to WhatsApp, IndiaMART and Google. Trackers were stripped
first, so the "no analytics or advertising cookies" statement is true as at
the date below.

Every locale copy gets the same English text. That is a stopgap: it is better
than leaving Eclipse's text in place, and it can be translated or deleted once
the fate of the locale trees is decided.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")
UPDATED = "28 July 2026"

COMPANY = "Santosh Magnetic Works"
EMAIL = "queries@santoshmagneticworks.com"
ADDRESS = (
    "026 / 177, Sarita Indl Estate, A Wing, Prabhat Complex, Near Toll Plaza, "
    "W E Highway, Dahisar East, Mumbai, Maharashtra 400068, India"
)
GSTIN = "27ABDFS2378H1ZY"

PRIVACY_PAGES = [
    "information/privacy-policy/index.html",
    "en-us/information/privacy-policy/index.html",
    "cn/information/privacy-policy/index.html",
    "de/informationen/datenschutzerklarung/index.html",
    "fr/informations/politique-confidentialite/index.html",
]
COOKIE_PAGES = [
    "information/cookie-policy/index.html",
    "cn/information/cookie-policy/index.html",
]

PRIVACY_BODY = f"""<h1>Privacy Policy</h1>
<p><em>Last updated {UPDATED}.</em>
<p>This policy explains what personal data {COMPANY} collects, why we collect
it, and what you can ask us to do with it. We have kept it short and specific
to this website rather than generic.
<h3>Who we are</h3>
<p>{COMPANY} manufactures magnetic separation, lifting and work-holding
equipment in Mumbai. For the purposes of the Digital Personal Data Protection
Act 2023, we are the Data Fiduciary for the data described here.
<p>{COMPANY}<br>{ADDRESS}<br>GSTIN {GSTIN}<br>
<a href="mailto:{EMAIL}">{EMAIL}</a>
<h3>What we collect</h3>
<p>We collect only what you send us:
<ul>
<li>Details you submit through an enquiry form on this website, typically your
name, company, email address, telephone number and your message.</li>
<li>Details you send us directly by email, telephone or WhatsApp.</li>
<li>Order and transaction records where you buy from us, including the
information we are required to record for GST and tax purposes.</li>
</ul>
<p>We do not run analytics or advertising on this website, so we do not build
a profile of your browsing. We do not buy personal data from third parties and
we do not sell yours.
<h3>Why we use it</h3>
<ul>
<li>To answer your enquiry and prepare quotations.</li>
<li>To supply, deliver and support the equipment you order.</li>
<li>To keep the accounting, tax and statutory records we are obliged to keep.</li>
<li>To contact you about an order you have placed with us.</li>
</ul>
<p>We will not add you to a marketing list on the strength of an enquiry alone.
<h3>Who we share it with</h3>
<p>We share personal data only where it is necessary, and only with:
<ul>
<li>Couriers and transporters, to deliver your order.</li>
<li>Our bank and payment processors, to take payment.</li>
<li>Our accountants and auditors, for statutory compliance.</li>
<li>Government authorities, where the law requires it.</li>
</ul>
<h3>How long we keep it</h3>
<p>Enquiries that do not lead to an order are kept only as long as they are
useful in answering you. Order, invoice and tax records are kept for the period
Indian tax and company law requires, currently eight years, after which they
are deleted or destroyed.
<h3>Your rights</h3>
<p>You may ask us to give you a copy of the personal data we hold about you,
correct it if it is wrong or incomplete, or erase it where we are not required
to keep it. You may also withdraw a consent you have given, and nominate
another person to exercise these rights on your behalf.
<p>To make a request, or to raise a complaint about how we have handled your
data, write to <a href="mailto:{EMAIL}">{EMAIL}</a> and mark it for the
attention of our Grievance Officer. We will acknowledge and respond within the
period required by law. If you are not satisfied with our response, you may
complain to the Data Protection Board of India.
<h3>Cookies</h3>
<p>This website does not use cookies for analytics or advertising. See our
<a href="/information/cookie-policy/">Cookie Policy</a> for the detail.
<h3>Security</h3>
<p>We apply reasonable safeguards to the data we hold and limit access to staff
who need it to do their work. No transmission over the internet can be
guaranteed completely secure, so please do not send us sensitive information by
email that you would not want read in transit.
<h3>Changes</h3>
<p>If we change this policy we will update the date at the top of this page."""

COOKIE_BODY = f"""<h1>Cookie Policy</h1>
<p><em>Last updated {UPDATED}.</em>
<p>Cookies are small files a website can store on your device. This page sets
out what this website does and does not use them for.
<h3>What we do not use</h3>
<p>We do not use analytics cookies, advertising cookies, or third-party
tracking of any kind on this website. There is no Google Analytics, no tag
manager, no advertising pixel and no session recording. That is why you are not
asked to accept cookies when you arrive.
<h3>What we do use</h3>
<p>Only cookies that are strictly necessary for the website to work, for
example remembering a preference you have set during your visit. These are not
used to identify you or to follow you between websites, and they are removed
when their purpose ends.
<h3>Content from other services</h3>
<p>A few pages include content served by others, and those services may set
their own cookies if you interact with them:
<ul>
<li>Product videos are embedded from YouTube in privacy-enhanced mode, which
does not set tracking cookies unless you play the video.</li>
<li>Interactive 3D product views are served by an external viewer.</li>
</ul>
<p>Our WhatsApp, IndiaMART and Google Business links are ordinary links. They
set nothing until you choose to follow them, at which point the privacy policy
of that service applies.
<h3>Controlling cookies</h3>
<p>You can block or delete cookies in your browser settings at any time. Doing
so will not stop you using this website, though a preference you had set may
not be remembered.
<h3>Changes</h3>
<p>If we change this policy we will update the date at the top of this page.
<h3>Contact</h3>
<p>Any questions about this policy can go to
<a href="mailto:{EMAIL}">{EMAIL}</a>."""

# First content block: <div class=row><div class=row__inner> ... </div></div>
BLOCK_RE = re.compile(
    r"(<main><div class=\"content-wrapper[^\"]*\"><div class=row><div class=row__inner>)"
    r".*?"
    r"(</div></div></div>)",
    re.DOTALL,
)
TITLE_RE = re.compile(r"<title>.*?</title>", re.DOTALL)
DESC_RE = re.compile(r'<meta name=description content="[^"]*">')


def rewrite(rel: str, body: str, title: str, desc: str) -> None:
    page = SITE / rel
    if not page.exists():
        print(f"  MISSING  {rel}")
        return
    text = page.read_text(encoding="utf-8")

    new, n = BLOCK_RE.subn(lambda m: m.group(1) + body + m.group(2), text)
    if not n:
        print(f"  NO CONTENT BLOCK MATCHED  {rel}")
        return

    new = TITLE_RE.sub(f"<title>{title} | {COMPANY}</title>", new)
    new = DESC_RE.sub(f'<meta name=description content="{desc}">', new)

    page.write_text(new, encoding="utf-8")
    print(f"  ok  {rel}  ({len(text)} -> {len(new)} bytes)")


def main() -> None:
    print("privacy pages:")
    for rel in PRIVACY_PAGES:
        rewrite(
            rel,
            PRIVACY_BODY,
            "Privacy Policy",
            f"What personal data {COMPANY} collects, why, and how to ask us to "
            "correct or erase it.",
        )
    print("\ncookie pages:")
    for rel in COOKIE_PAGES:
        rewrite(
            rel,
            COOKIE_BODY,
            "Cookie Policy",
            f"{COMPANY} uses no analytics or advertising cookies. What we do "
            "use, and how to control it.",
        )

    print("\nEclipse traces left in these pages:")
    for rel in PRIVACY_PAGES + COOKIE_PAGES:
        p = SITE / rel
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        main_only = re.search(r"<main>.*</main>", t, re.DOTALL)
        seg = main_only.group(0) if main_only else t
        hits = len(re.findall(r"Eclipse|Spear|Jackson|Sheffield", seg))
        print(f"  {hits:>3}  {rel}")


if __name__ == "__main__":
    main()
