# Rebuild scripts

Transformations applied to `site/`, the local working copy of the Eclipse
Magnetics mirror, as it is reworked into the SMAG site.

`site/` is git-ignored (it still contains substantial third-party content), so
these scripts are the only version-controlled record of the work.

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
