# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **Buyers and procurement staff** at Indian plants: comparing suppliers, checking what SMAG makes, its specifications, brochures, ISO 9001 and GST details before making contact.
- **Export customers**: overseas buyers deciding whether SMAG can supply them.

Not everyone who lands on the site reads English comfortably. Plant engineers and shop-floor staff do visit, but they are not the primary audience.

## Product Purpose

The marketing site for Santosh Magnetic Works (SMAG, mark "S-MAG"), a Mumbai manufacturer of magnetic separation, filtration, lifting and workholding equipment since 1978. It exists to turn a buyer's first look into a conversation with the works.

Success is a **phone call or WhatsApp message** to the works. The enquiry form, email and brochure downloads are secondary routes.

## Positioning

- **Made in its own works.** Designed, machined and tested in-house at Dahisar East, Mumbai, since 1978, so build quality and delivery dates stay in SMAG's hands.
- **After-sales for years.** Spares, servicing and re-magnetising long after the sale.
- **A client roster of known names** (Britannia, ITC, Parle, Reliance, Castrol, Finolex and others; logos in `site/site/assets/images/clients/`).

## Operating Context

- Six product families: Magnetic Filtration, Magnetic Separation, Stock Magnets & Tools, Workholding Systems, Lifting & Handling, Pipeline Filtration. Eight industries: food, sugar, pharmaceutical, chemical, virgin and recycled plastic, steel, oil and gas, aerospace. Twelve guides.
- Contact routes: phone and WhatsApp (+91 93245 87891, the company number; Contact Us also lists +91 93243 15562, +91 99201 43922 and +91 82861 93555), queries@santoshmagneticworks.com, the enquiry form on /contact-us/ (posts to Web3Forms), IndiaMART listing, Google business profile.
- Printed brochures served as PDFs from /brochures/.
- Buyers typically need specifications, compliance details (ISO 9001:2015, GSTIN 27ABDFS2378H1ZY) and a way to reach a person.

## Capabilities and Constraints

- Static HTML/CSS/JS in `site/`, deployed to GitHub Pages at santoshmagneticworks.com (currently in maintenance mode; see `.github/workflows/pages.yml`). No build step and no server-side code.
- The site was derived from a mirror of another manufacturer's site and rebranded; `reference-mirror/` is a pristine reference that must never be edited or deployed. Changes are made by scripts in `tools/rebuild/`, recorded in its README.
- Copy for families, products and industries renders from `assets/source/pages/*.md`; guides from `assets/source/guides/*.md`.
- **Multilingual copy is the next workstream.** Translations must be simple, everyday vernacular, cohesive with the English, and not formal or "pure" language. Target languages are not yet chosen.
- Open product facts awaiting the client: roles for Deepak, Santosh and Mandar Ingle; lifter name (brochure "neoLIFT" vs site "Maxx"); several spec conflicts; drawer housings, V-blocks, tool racks and horseshoe magnets are mentioned without product pages.

## Brand Commitments

- Name: Santosh Magnetic Works; short form SMAG; logo mark "S-MAG" (red pill, `site/site/assets/images/logo.svg`).
- Tagline: "Leaders In Magnetic Engineering", set under the logo.
- Voice: plain, direct trade writing in UK English. Short sentences, one idea each, common words, one name per product, units written the same way every time. No em dashes, no emojis, no contrastive "X, not Y" constructions, no meta-commentary, no "from X to Y" range formula.
- Photography of the family, the team and the hero video is SMAG's own.
- Pinned for design work (30 Sep 2026): the S-MAG red and logo, Noto Sans as the type family, every word of the current copy, and the existing photography. Design rounds change presentation only.
- The site must never read as cold or sterile, as flashy (heavy scroll effects, parallax), as hiding the call and WhatsApp routes, or as burying specifications.

## Evidence on Hand

- Family portraits: `assets/source/supplied/team/`; team and works photos under `site/site/assets/images/`.
- Hero video: `site/site/assets/images/hero-lifter.mp4` (SMAG's own footage).
- Product stills: `assets/source/brochure-stills/`, `assets/source/product-stills/`.
- Brochures: `assets/source/brochures/`, served from `site/site/assets/files/smag/`.
- Client logos: `site/site/assets/images/clients/`.
- **Unverified, do not repeat or extend without a source:** "300+ manufacturers", "4.7 / 5 across 23 reviews", the lifter "three year guarantee", the pipeline filter's "up to 90 bar" and its sampling and training service.
- **Absent, do not fabricate:** testimonials, case studies, certifications beyond ISO 9001:2015, prices.
- About 23 banner and industry images are still stock scenery inherited from the mirror and are due for replacement.

## Product Principles

1. Every page leads a buyer to a person: call or WhatsApp is always one step away.
2. Show proof SMAG actually has (the works, the family, the clients, the specifications) and claim nothing it cannot back.
3. Write for a reader whose first language may not be English, and for a translator.
4. One name per product and one fact per claim, the same everywhere.

## Accessibility & Inclusion

- Visitors may not read English well; the copy must translate cleanly, and translated pages will follow.
- Many buyers browse on phones; phone and WhatsApp contact must work well on mobile.
