#!/usr/bin/env python3
"""Copy edits for a plainer, less machine-written voice.

The vocabulary was already clean (no "seamless", "robust", "leverage"). What
gave it away was structural:

  - meta-commentary about the document itself ("We have kept it short and
    specific to this website rather than generic") which no business writes
  - announcing counts the reader can already see ("Six stages", "Three steps")
  - the "from X to Y" range formula
  - trust-strip boilerplate ("Trusted by", "A selection of")

Idempotent: every replacement is an exact string that disappears once applied.
"""
from __future__ import annotations

import re
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

EDITS: dict[str, list[tuple[str, str]]] = {
    "index.html": [
        # second hero slide carried Eclipse's filtration strapline
        ("<h1 class=regular>Sub-Micron Magnetic Filtration Systems</h1>"
         "<div class=c2a><a href=/products/filtration-systems/ class=button>"
         " Discover Filtration Solutions </a>",
         "<h1 class=regular>Separators, filters, lifters and chucks, made in Mumbai</h1>"
         "<div class=c2a><a href=/products/magnetic-separation-and-metal-detection/ class=button>"
         " See the separators </a>"),
        ("<h1 class=regular>The Industries We Serve</h1>"
         "<div class=c2a><a href=/industries/ class=button> Read More </a>",
         "<h1 class=regular>Built for food, plastics, steel, chemical and pharma lines</h1>"
         "<div class=c2a><a href=/industries/ class=button> See the industries </a>"),
        # Eclipse tagline row that repeated the Product Families intro and
        # ended in a colon; removed 2 Sep 2026 (redundancy flagged by Saahil)
        ('<div class="row row--alt tagline"><div class=row__inner><h4>We '
         "manufacture high quality magnets, supporting various industries "
         "with advanced magnetic technology and equipment. Explore our "
         "business key divisions:</h4></div></div>",
         ""),
        ("<h3 class=bordered-header>Trusted on production lines across India</h3>"
         "<p class=intro>A selection of the manufacturers who rely on our "
         "magnetic equipment.",
         "<h3 class=bordered-header>Running on production lines across India</h3>"
         "<p class=intro>Some of the manufacturers using our equipment."),
    ],
    "company/about-us/index.html": [
        ('<meta name=keywords content="Magnets. Magnet supplier, Magnetics , Magnetic systems , magnet manufacturer">', ""),
        ("The same three steps whether you need one stock magnet or a separator built around your line.",
         "The same three steps for one stock magnet and for a separator built around your line."),
    ],
    "products/filtration-systems/index.html": [
        ('alt="Filtramag+ Magnetic Filter"', 'alt="Filtramag magnetic filter"'),
    ],
    "contact-us/index.html": [
        # "not a call centre" is the kind of thing a works actually says.
        ("<p>Send us the details and we will come back to you with a "
         "recommendation and a quotation. If it is urgent, call or message us "
         "on WhatsApp using the numbers alongside, and you will reach someone "
         "at the works.",
         "<p>Send us the details and we will come back with a recommendation "
         "and a price. If it is urgent, call or WhatsApp the numbers alongside "
         "and someone at the works will pick up."),
    ],
    "information/privacy-policy/index.html": [
        # Meta-commentary about our own writing: the clearest tell of the lot.
        ("<p>This policy explains what personal data Santosh Magnetic Works "
         "collects, why we collect it, and what you can ask us to do with it. "
         "We have kept it short and specific to this website rather than "
         "generic.",
         "<p>This policy covers what personal data Santosh Magnetic Works "
         "collects, why, and what you can ask us to do with it."),
        ("<p>We will not add you to a marketing list on the strength of an "
         "enquiry alone.",
         "<p>An enquiry does not put you on a mailing list."),
        ("<p>Enquiries that do not lead to an order are kept only as long as "
         "they are useful in answering you. Order, invoice and tax records are "
         "kept for the period Indian tax and company law requires, currently "
         "eight years, after which they are deleted or destroyed.",
         "<p>Enquiries that do not turn into an order are kept only as long as "
         "they are useful in answering you. Order, invoice and tax records we "
         "keep for as long as Indian tax and company law requires, currently "
         "eight years, then delete or destroy them."),
        ("<p>We apply reasonable safeguards to the data we hold and limit "
         "access to staff who need it to do their work. No transmission over "
         "the internet can be guaranteed completely secure, so please do not "
         "send us sensitive information by email that you would not want read "
         "in transit.",
         "<p>We keep reasonable safeguards on the data we hold and limit access "
         "to the people who need it for their work. Nothing sent over the "
         "internet is ever completely secure, so please do not email us "
         "anything sensitive that you would mind being read in transit."),
    ],
    "information/cookie-policy/index.html": [
        # no embedded video or 3D viewers remain on the site
        ("<p>A few pages include content served by others, and those services may set\ntheir own cookies if you interact with them:\n<ul>\n<li>Product videos are embedded from YouTube in privacy-enhanced mode, which\ndoes not set tracking cookies unless you play the video.</li>\n<li>Interactive 3D product views are served by an external viewer.</li>\n</ul>\n",
         "<p>This site embeds no video players, maps or other third party content.\n"),
        ("<p>Cookies are small files a website can store on your device. This "
         "page sets out what this website does and does not use them for.",
         "<p>Cookies are small files a website can store on your device. Here "
         "is what this site uses them for."),
        ("<p>Only cookies that are strictly necessary for the website to work, "
         "for example remembering a preference you have set during your visit. "
         "These are not used to identify you or to follow you between "
         "websites, and they are removed when their purpose ends.",
         "<p>Only what the site needs to work, such as remembering a preference "
         "you set during your visit. These do not identify you, they do not "
         "follow you to other sites, and they go when their purpose ends."),
    ],
}


def main() -> None:
    for rel, pairs in EDITS.items():
        page = SITE / rel
        if not page.exists():
            print(f"  MISSING  {rel}")
            continue
        text = page.read_text(encoding="utf-8")
        applied = skipped = 0
        for old, new in pairs:
            # The generated pages wrap paragraphs across lines, so match on
            # whitespace-insensitive patterns rather than exact strings.
            pat = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
            if pat.search(text):
                text = pat.sub(lambda _: new, text, count=1)
                applied += 1
            elif re.search(r"\s+".join(re.escape(w) for w in new.split()), text):
                skipped += 1  # already applied
            else:
                print(f"  NO MATCH in {rel}: {old[:58]}...")
        page.write_text(text, encoding="utf-8")
        print(f"  {rel}: {applied} applied, {skipped} already done")


if __name__ == "__main__":
    main()
