# SMAG content redesign

Date: 2026-06-16
Owner: Saahil Mehta

Turn the reskinned-but-template-copy site into a real Santosh Magnetic Works
site using verified content from the source pack (`~/Downloads/s-magnetic`).
Structural QA already done; this is the content + information-architecture pass.

## Decisions (confirmed with user)

- Founded: **1978** (keep; IndiaMART's "1983" is the firm record, 1978 is used site-wide).
- **Delete** Packages, Projects and Blog entirely (pages, sub-pages, all links, metadata).
- **New Products page**: single rich catalogue, grouped by family, each product with
  description, key specs, applications, a uniform engineering mockup, and an
  "Enquire" CTA (price on request, links to contact).
- No fabricated testimonials/clients. Home uses a real trust strip
  (4.7 stars, 23 reviews, ISO, Made in India, since 1978).

## Information architecture

Nav: Home (logo) · About · Services · Products · Contact (button).
Delete from nav/footer: Packages, Projects, Blog.

## Verified facts (source: IndiaMART pages, brand kit, proforma)

- Mumbai partnership firm; manufacturer with in-house factory and testing.
- Brand mark on products: "Smag"; Made in India; ISO certified; 4.7/5 from 23 reviews.
- Tagline: Power. Precision. Performance.
- Contact: 117 Sarita Industrial Estate, Dahisar East, Mumbai 400068;
  +91 99201 43922; santosh_magnetic@hotmail.com.

## Product catalogue (real, from source)

- **Separators**: Overband Magnetic Separator (tramp iron off conveyors; power
  plants, bulk handling); Suspension / Suspended Plate Magnet; High Power Magnetic
  Plates; Hand Magnetic Separator; Rare-Earth (NdFeb) high-intensity separators.
- **Lifters**: Permanent Magnet Lifter (lever on/off, no power; plates, blocks, round bar).
- **Chucks**: Permanent Magnetic Chuck; Round Permanent Magnetic Chuck (to 600 mm);
  Electro-Permanent Magnetic Chuck (N35, surface grinding); Electromagnetic
  Rectangular Chuck; Heavy-Duty Multicoil Electromagnetic Chuck.
- **Grills**: Hopper Magnetic Grill (ferrite, N45, dia 250 mm, rod 38 mm; fine iron
  from free-flowing powders/granules; food, pharma, plastics, chemicals).
- **Filters**: Precision and Industrial Magnetic Filters (ferrous from liquids,
  coolants, slurries; inline).
- **V-Blocks**: Magnetic V-Block (magnetic clamping for inspection, marking, drilling).
- **Sweepers**: Floor Magnetic Sweeper (72 in, semi-auto; nails, shavings, debris).
- **Tool racks**: Magnetic Tool Holder Rack.
- **Magnets**: Ferrite (hard/sintered/rod), Neodymium/NdFeb (disc, pot, hooks),
  Rare-Earth, Shallow Pot Magnet, Alnico; Demagnetizer (230 V AC); Mini Magnetic Collector.

## Page plans

- **Home**: magnetics copy; replace green "services/testimonials/latest-news"
  blocks with product highlights + real trust strip; CTA to enquire. Remove the
  latest-news section (linked deleted blogs) and any projects showcase.
- **About**: tighten with verified facts.
- **Services**: standard + custom manufacturing, duty-matched selection, in-house
  testing/QA, supply, after-sales, export.
- **Products (new)**: single catalogue page (see above).
- **Contact**: already done in the QA pass.

## Mockups

Uniform SVG engineering illustrations, one consistent style, red accent. Produce
2-3 sample styles for user to choose before building the full set.

## Phases

1. **1a Structural cleanup**: delete the 3 page sets; update nav.html, footer.html,
   animations.js drawer/current-link; fix in-body links on index.html; rebuild;
   verify no broken links.
2. **1b Copy reframe**: Services and About to magnetics; Home sections (services
   preview, testimonials -> trust strip, remove latest-news).
3. **2 Products page + mockups**: sample mockups -> approval -> build catalogue.

Each phase: build -> verify (links, build idempotency, render) -> commit.
