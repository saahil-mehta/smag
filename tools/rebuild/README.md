# Rebuild scripts

Transformations applied to `site/`, the local working copy of the Eclipse
Magnetics mirror, as it is reworked into the SMAG site.

`site/` is git-ignored (it still contains substantial third-party content), so
these scripts are the only version-controlled record of the work. They are also
the recovery path: `site/` is reproducible as **pristine mirror + these scripts
in order**, which has already rescued the working copy twice after a bad sweep.

## Order

`rebuild_site.sh` restores every HTML file from `reference-mirror/` and replays
the first group. The rest were applied on top, in roughly this order:

| Script | What it does |
| --- | --- |
| `swap_logo.py` | Eclipse logo asset and alt text to the SMAG mark |
| `swap_address.py` | five regional postal addresses to the Mumbai works |
| `swap_contact_social.py` | email, phone, and the social column |
| `swap_lower_bar.py` | copyright, agency credit, accreditation badges |
| `drop_legal_links.py` | removes Extranet Terms and Conditions of Purchase |
| `write_policies.py` | SMAG privacy and cookie policy content |
| `strip_trackers.py` | removes 3,208 tracker blocks (GTM, LinkedIn, OptiMonk, ActiveCampaign, Baidu) |
| `remove_sections.py` | deletes the locale trees, case studies, news, partner login |
| `remove_testimonials.py` | removes 57 Eclipse testimonial carousels |
| `refurb_contact.py` | rebuilds the contact page and its enquiry form |
| `refurb_about.py` | rebuilds the About page from the site's own components |
| `prep_badges.py` | ISO 9001 and Make in India footer badges |
| `add_client_logos.py` | client logo strip on home and About |
| `tidy_logo_strip.py` | re-lays that strip as a grid so no row is orphaned |
| `home_products_heading.py` | removes Industry Focus, adds the Product Families heading |
| `build_product_tiles.py` | watermarks and sizes the six product-family tiles |
| `wire_product_tiles.py` | rebuilds the product grid as six real families |
| `copy_edit.py` | removes AI tells from the copy |

## Two lessons the hard way

**Bound element removal by depth walk, never by a closing-tag literal.** A regex
cannot match a `<div>` that contains nested `<div>`s. `.*?</div>` stops at the
first inner close and an unbounded `.*` runs to the end of the document. Three
separate sweeps here corrupted markup that way, once destroying the footer across
318 pages. `find_element_end` in `remove_sections.py` is the pattern to copy.

**Terminate slug alternations with `/` or `\b`.** `/fr` matched `/free-quote/`
and silently deleted the Free Quote CTA from 187 pages. `metal-detection` also
appears inside `magnetic-separation-and-metal-detection`, which would have taken
968 valid links with it.

Verify every sweep by diffing against `reference-mirror/` and classifying each
deletion, not by counting tags.
