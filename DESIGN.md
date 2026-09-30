---
name: Santosh Magnetic Works
description: The Works Catalogue, SMAG's range book of plates on white with their readings beside them.
colors:
  ink: "#16181A"
  ink-2: "#33383D"
  muted: "#5B6268"
  rule: "#D9DDE0"
  steel: "#F2F4F5"
  paper: "#FFFFFF"
  red: "#E20026"
  red-deep: "#B8001F"
typography:
  display:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "clamp(2.5rem, 1.6rem + 3.4vw, 4.75rem)"
    fontWeight: 600
    lineHeight: 1.02
    letterSpacing: "-0.028em"
  headline:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "clamp(2.25rem, 1.5rem + 2.7vw, 4rem)"
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: "-0.024em"
  section:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "clamp(1.75rem, 1.35rem + 1.5vw, 2.625rem)"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "clamp(1.25rem, 1.05rem + 0.7vw, 1.625rem)"
    fontWeight: 600
    lineHeight: 1.22
    letterSpacing: "-0.01em"
  plate-title:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "1.3125rem"
    fontWeight: 600
    lineHeight: 1.24
    letterSpacing: "-0.012em"
  reading:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "clamp(1.375rem, 1.1rem + 0.9vw, 1.875rem)"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.03em"
    fontFeature: "\"tnum\" 1, \"lnum\" 1"
  body:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "18px"
    fontWeight: 450
    lineHeight: 1.62
  index:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "0.8125rem"
    fontWeight: 500
    lineHeight: 1.62
  label:
    fontFamily: "Noto Sans, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 600
    letterSpacing: "0.08em"
  tagline:
    fontFamily: "Noto Serif, Georgia, serif"
    fontWeight: 700
    lineHeight: 1.1
rounded:
  none: "0px"
spacing:
  gutter-sm: "15px"
  gutter: "30px"
  plate-gap: "24px"
  caption: "28px"
  band: "3.2em"
components:
  button-primary:
    backgroundColor: "{colors.red}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "0.97em 2.563em 1.15em 1.475em"
    typography: "{typography.index}"
  button-primary-hover:
    backgroundColor: "{colors.red-deep}"
    textColor: "{colors.paper}"
  plate:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "20px 28px 28px"
  plate-caption-action:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    padding: "17px 28px"
  thumb-index-link:
    textColor: "{colors.muted}"
    typography: "{typography.index}"
    padding: "15px 0 13px"
  thumb-index-link-current:
    textColor: "{colors.ink}"
  input:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
  action-band:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    padding: "3.2em 0"
  action-call:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    padding: "0.9em 1.35em"
  action-whatsapp:
    backgroundColor: "{colors.red}"
    textColor: "{colors.paper}"
    padding: "0.9em 1.35em"
---

# Design System: Santosh Magnetic Works

## Overview

**Creative North Star: "The Works Catalogue"**

The site is SMAG's own range book. Each product sits as a framed plate on a white page, and its specification is set as ruled readings beside or below it. Hierarchy comes from the size of the type and from thin rules; colour does almost no structural work. White pages alternate with cool steel bands, ink carries the text and every rule that matters, and red appears where the buyer acts.

The system is a layer over an inherited theme stylesheet. The theme keeps layout mechanics (container, rows, grids, breakpoints); `site/site/assets/css/smag.css` and the "smag:" appendix of the theme stylesheet own the look. Density is moderate: generous section padding, tight ruled lists inside it. Motion is quiet and exact, with one exponential ease-out curve, and it switches off entirely under reduced motion.

Pinned by the brand: the S-MAG red and logo, Noto Sans as the type family, the copy, and SMAG's own photography. Design work changes presentation only.

**Key Characteristics:**
- White and steel grounds, ink type, 1px rules, square corners throughout.
- Red is kept for actions: the primary button, WhatsApp, and interaction states.
- Specifications read as label and value rows, with an ink rule at the head and hairline rules between rows.
- A thumb-index of the six families marks where the reader is on family and product pages.
- Every page ends on an ink band with call and WhatsApp.

## Colors

One brand red over a cool grey neutral family, with ink as the working dark.

### Primary
- **S-MAG Red** (red): the primary button, the WhatsApp action in header and action band, the text caret, text selection, the focus ring, and the required-field asterisk. It never marks section heads, bullets, chevrons, tags or carousel dots.
- **Pressed Red** (red-deep): hover state of every red action.

### Neutral
- **Works Ink** (ink): headings, body text, the heading rule of every reading list and table, the current thumb-index mark, hover border of plates, the action band ground, tags and gallery arrows.
- **Graphite** (ink-2): section intro paragraphs and reading values in the statistics register.
- **Steel Grey** (muted): secondary text, plate descriptions, breadcrumbs, spec labels, idle index links, list markers.
- **Hairline** (rule): every 1px border: plates, header underline, dropdown panels, form fields, row separators, footer rule.
- **Steel Band** (steel): alternate section ground and menu item hover.
- **Paper** (paper): the page, plates and form fields.

### Named Rules
**The Red Is For Acting Rule.** Red marks only what the buyer can do (button, WhatsApp) and the states of doing it (focus, caret, selection, required). Bullets are square and grey, chevrons and carousel arrows are filtered to ink, tags are ink, hero dots are white.

**The Ink Rule Heads The List Rule.** A reading list, specification table, guide list or statistics register opens with a 1px ink rule; the rows below it are separated by 1px hairlines.

## Typography

**Display Font:** Noto Sans (self-hosted variable, weights 100 to 900, sans-serif fallback)
**Body Font:** Noto Sans
**Tagline Font:** Noto Serif Bold Italic, used only for "Leaders In Magnetic Engineering" under the logo

**Character:** One family doing all the work through scale contrast: heavy, tightly tracked headings over a light 450 body. Numerals in tables, spec lists and readings are tabular and lining.

### Hierarchy
- **Display** (600, clamp to 4.75rem, 1.02): inner-page titles, set in ink on white above the framed banner photograph. The home hero title steps down to clamp(2.5rem, 1.7rem + 2.6vw, 4.25rem), white over the film, at most 11.5em wide.
- **Headline** (600, clamp to 4rem, 1.05): the product page title and other h1s. Guide titles use clamp(2rem, 1.4rem + 2.4vw, 3.25rem).
- **Section** (600, clamp to 2.625rem, 1.1): section heads, preceded by a 1px hairline across the column. Guide body h2s use clamp(1.5rem, 1.2rem + 1.1vw, 2rem).
- **Title** (600, clamp to 1.625rem, 1.22): h3. Plate and family tile titles are fixed at 1.3125rem.
- **Reading** (600, clamp to 1.875rem, 1.2, tabular): the figure in each statistics register row.
- **Body** (450; 14.5px, 16px from 550px, 18px from 1024px; 1.62): paragraphs and lists. Intros cap at 62ch, guide and product prose at 68ch.
- **Index** (500, 0.8125rem): thumb-index, subnav, breadcrumbs.
- **Label** (600, 0.75rem, 0.08em, uppercase, Steel Grey): footer column heads and team role lines.

### Named Rules
**The Scale Not Bar Rule.** Section heads are marked by size and a hairline above; the theme's red bar before headings is removed.

**The No Kicker Rule.** Nothing sits above a heading. The build hides kicker lines above h2s and moves the About banner's label below its heading.

## Layout

The theme's container is 1334px wide with 15px side gutters, 30px from 550px. Sections are rows with 5.8em vertical padding (4em inside tabbed product content); the statistics register and the action band use 3.2em. Breakpoints are 550px, 768px, 1024px, 1280px and 1400px, mobile first.

Plates sit in grids with a 24px gap. Plate captions pad 20px 28px 28px; spec rows pad 14px 0 with a 28px column gap on a two-column label and value grid (label column minmax(9em, 34%)), capped at 860px. The statistics register uses a label column of minmax(7em, 22%) with a 32px gap.

The home first viewport is the hero film at its own 1224 by 720 proportion, clamp(560px, 58.8vw, 100svh) tall from 768px and max(520px, 78svh) below, with the title and its button stacked low-left 64px above the foot and a scroll cue centred at the bottom. Inner pages set the breadcrumb, then the title on white, then the banner photograph framed inside the column (4:3 on mobile, 16:7 from 550px, 1334:440 from 1024px).

Product specifications are never hidden behind tabs: every panel shows in sequence, and the tabs become anchors that jump to them. Wide tables scroll inside the panel with the model column sticky and the right edge fading while columns remain.

## Elevation & Depth

The system is flat. Depth comes from the steel and white band alternation, 1px rules, and the ink action band. The theme's dropdown shadow is removed. The only shadow-like values are functional: a 1px inset hairline on the sticky table column (a rule drawn as a shadow), a text shadow under the logo tagline over the hero film, and a dark gradient scrim over the hero film so the white title reads.

### Named Rules
**The Flat Plate Rule.** Plates, panels and menus carry no drop shadow. A plate answers hover by darkening its border from Hairline to Ink.

## Shapes

Square corners everywhere: buttons, plates, inputs, gallery arrows and the header contact buttons all set radius 0. Borders are 1px, in Hairline at rest and Ink for emphasis or state; index and tab markers are 2px ink underlines. The one rounded form is the S-MAG logo pill, a fixed brand asset.

## Components

### Buttons
Plain red slabs with a small arrow that leads.
- **Shape:** square (0).
- **Primary:** S-MAG Red, white text, weight 600, 0.889em, padding 0.97em 2.563em 1.15em 1.475em with the arrow in the right padding.
- **Hover / Focus:** background eases to Pressed Red over 0.18s and the arrow moves 3px right; pressing drops the button 1px. Focus shows a 2px outline 3px out, ink on red buttons.
- **Caption action:** inside a plate the button becomes a transparent ink row under a hairline, its arrow filtered to ink and nudging 4px on plate hover.

### Plates
The signature container: a product or family shown face out on white.
- **Corner Style:** square.
- **Background:** Paper, with the product still multiplied onto it and brightened slightly so near-white photo grounds merge with the plate.
- **Border:** 1px Hairline, Ink on hover; the image eases forward 4% over 0.8s.
- **Internal Padding:** image area 32px 32px 8px at 272px tall; caption 20px 28px 28px with a Steel Grey description.

### Readings
Specification lists, tables, the statistics register and the family guide list share one form: an ink rule on top, hairline rules between rows, label in Steel Grey weight 500, value in ink, tabular numerals. Table heads are ink on transparent with an ink underline; the first column is weight 500 and never wraps.

### Inputs / Fields
- **Style:** 1px Hairline border, Paper ground, square.
- **Focus:** border turns Ink with no outline; hover turns it Steel Grey. The caret is red.
- **Labels:** weight 500, 0.8889em, ink; required fields carry a red asterisk.

### Navigation
- **Header:** logo lockup with its serif tagline, main nav at weight 500, and call and WhatsApp on the right. Nav links draw a 1px underline from the left over 0.4s. Dropdowns are hairline-bordered panels that ease down 6px as they open; items hover to Steel Band. The sticky header slides down on arrival. Below 1280px the call and WhatsApp actions collapse to 40px square icons.
- **Thumb-index:** a scrolling row of the six families under the header on family and product pages, Index type in Steel Grey. Hover and the current family draw a 2px ink underline; the current link turns ink.
- **Breadcrumbs:** Index type in Steel Grey, the current page in ink, placed above the page title.

### Action Band
Every page ends on a Works Ink band: the invitation in white at clamp(1.375rem, 1.1rem + 1.1vw, 2rem), then a call button outlined in 45% white and a red WhatsApp button, both square, weight 600. Focus outlines here are white.

## Do's and Don'ts

### Do:
- **Do** keep red to the primary button, WhatsApp, and the focus, caret, selection and required states.
- **Do** mark hierarchy with type scale and 1px rules; head every reading list or table with an ink rule.
- **Do** keep every corner square and every border 1px, Hairline at rest and Ink for state.
- **Do** use the single ease `cubic-bezier(.16, 1, .3, 1)` for every transition and animation, and switch motion off under reduced motion.
- **Do** end every page with the ink action band carrying call and WhatsApp.
- **Do** set figures with tabular, lining numerals.

### Don't:
- **Don't** colour bullets, chevrons, tags, section markers or carousel dots red.
- **Don't** put drop shadows on plates, panels or menus.
- **Don't** place kickers or labels above headings.
- **Don't** hide specifications behind tabs; tabs jump to panels that are all shown.
- **Don't** use parallax or scroll-linked effects; scroll reveals apply only to grids of plates, tiles, portraits and the guide list, never to text, specifications or the action band.
- **Don't** use Noto Serif anywhere except the logo tagline.
