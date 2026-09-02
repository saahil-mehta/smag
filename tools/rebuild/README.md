# Rebuild scripts

Transformations applied to `site/`, the local working copy of the Eclipse
Magnetics mirror, as it is reworked into the SMAG site.

`site/` is committed and deployed as the web root since 2 Sep 2026. These
scripts remain the record of how it was derived from the mirror.

They are also a recovery path, but a **machine-local** one, and that limit is
worth stating plainly. `site/` is reproducible as *pristine mirror + these
scripts in order*, and that has already rescued the working copy twice after a
bad sweep. But `reference-mirror/` is git-ignored too, for the same third-party
reason, so it exists only on this machine. If this machine is lost, the scripts
have nothing to replay against, and the mirror would have to be re-fetched with
no guarantee the source site still matches.

Nothing here should be treated as a backup of `site/` itself.

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
| `prune_industries.py` | trims industries to the eight sectors SMAG serves |
| `prune_catalogue.py` | trims each product family to SMAG's range, rebuilds the listing grids, renames the Eclipse-branded housed-grid slug |
| `restore_pipeline.py` | restores the Pipeline Filtration family from the mirror with transplanted SMAG chrome, wires it into nav, footer and sitemap |
| `build_smag_product_pages.py` | authors the nine SMAG product pages (eight separation, one lifter) from the brochure inventory and stills in `assets/source/brochure-stills/` |
| `scrub_dead_links.py` | removes every internal link to a page that does not exist (partial-crawl leftovers and pruned range) |
| `restore_home_hero.py` | reinstates the home hero slide the first scrub pass removed |
| `fix_missing_media.py` | SMAG brochure photos onto the workholding pages, repoints or drops broken gallery slides, strips dead img/source tags |
| `add_home_industries.py` | Industries We Serve row on the home page, tiles harvested from /industries/ |
| `fix_double_title.py` | collapses doubled "\| Santosh Magnetic Works" title suffixes |
| `swap_domain.py` | every absolute eclipsemagnetics.com URL (canonical, JSON-LD, og tags, in-copy links) to santoshmagneticworks.com |
| `remove_eclipse_pages.py` | deletes video hub, webinars, quality-standards, EDM landing, Brexit guide, the ATEX certifications page and every Eclipse PDF; hosts SMAG's own brochures at files/smag/ |
| `strip_datasheets.py` | removes every Eclipse datasheet link, writes SMAG brochure data into the Technical Data / Models tabs, rebuilds /brochures/ around SMAG's own PDFs |
| `debrand_copy.py` | removes Sesotec/distributor/staff sections and ATEX claims, rewrites the century-of-history copy to SMAG's 1978 story, swaps every remaining brand mention |
| `watermark_catalogue_images.py` | S-MAG mark on every product gallery and family-grid image site-wide (manifest in assets/source/watermarked.txt) |
| `scrub_image_branding.py` | replaces Eclipse-stamped product photos with SMAG stills, renames eclipse-named asset files, fills empty galleries and tiles, deletes orphaned Eclipse imagery |
| `flatten_nav.py` | header and mobile drawer become Products (six families), Industries, Guides, About Us, Contact Us; search removed; Bespoke dropped from the footer. Run again after `repair_tools_pages.py` |
| `drop_services_bespoke.py` | deletes the Services pages, the Bespoke Magnet Design family, ten off-range guides and the guide pagination stubs; removes their sitemap blocks |
| `repair_tools_pages.py` | rebuilds the seven Stock Magnets & Tools pages that a failed gallery replace had duplicated onto themselves, and gives them the product header (breadcrumbs, gallery, h1, quote button) |
| `scrub_dead_links.py` (again) | now also relativises absolute santoshmagneticworks.com links before checking them, and removes a dead call-to-action wrapper |
| `build_guides.py` | renders the twelve guides from `assets/source/guides/*.md`, rebuilds the guides index and the home carousel, updates sitemap titles |
| `strip_trackers.py` (again) | now also removes the Cloudflare challenge and email-obfuscation loaders |
| `drop_free_quote.py` | retires the empty Free Quote iframe page; the sticky call-to-action points at Contact Us |
| `flatten_nav.py` (again) | also removes the sticky call-to-action bar and appends the menu centring rule to the theme CSS |
| `drop_eclipse_video.py` | removes the Eclipse company video slide, the Autofiltrex YouTube row and eight orphaned Eclipse mp4 files |
| `drop_family_subpages.py` | deletes the eleven Eclipse educational and service sub-pages inside the families and the Case Studies sub-nav anchor |
| `rewrite_copy.py` | renders every family, product and industry page's copy from `assets/source/pages/*.md`; tile blurbs applied site-wide from the family Tiles sections |
| `copy_edit.py` (again) | home hero straplines, the redundant tagline row, cookie policy third-party section |
| `prepare_deploy.py` | final step before publishing: prunes unreferenced assets, strips the CMS generator meta, writes robots.txt, sitemap.xml, favicons, 404.html, CNAME and .nojekyll |

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

**Guard every `find()`.** `text[:i] + new + text[end:]` with `i == -1` and `end is None` is `text[:-1] + new + text`, which duplicates the whole page. That is how seven tools pages grew a second `<body>` below their footer. Raise when an anchor is missing; never slice on an unchecked index.

Verify every sweep by diffing against `reference-mirror/` and classifying each
deletion, not by counting tags.
