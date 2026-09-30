# Translating the SMAG site

Santosh Magnetic Works (SMAG) is a Mumbai manufacturer of magnetic
separators, filters, lifters, workholding chucks and stock magnets, in
business since 1978. The readers are plant owners, maintenance engineers,
purchase managers and shop floor supervisors in Indian factories: food,
plastics, steel, chemicals, sugar, pharma, oil and gas. Many of them read
their own language more easily than English, and all of them use English
trade words every day.

The site is translated into Hindi (hi), Marathi (mr), Gujarati (gu), Kannada
(kn), Telugu (te), Malayalam (ml) and Tamil (ta).

## Voice

Write the way a senior sales engineer at SMAG would explain the product to a
customer across the table, in that customer's language. It should read as if
it was first written in that language.

- **Everyday spoken register.** Use the words people in a factory actually
  say. Avoid Sanskritised, Persianised or textbook "pure" vocabulary that a
  plant manager would have to stop and decode. Hindi: चुंबक is fine where
  people say it, but "मैग्नेट" is what most buyers say for the product; use the
  word a buyer would type into a search box.
- **Short sentences, one idea each.** The English is already written this way.
  Keep sentence breaks where they are unless the language needs a join.
- **Plain and direct.** No flourishes, no marketing gloss added in
  translation, no rhetorical questions that are not in the English.
- **Consistent.** One translation per term, on every page. Decide your terms
  first (see Glossary) and keep to them.
- **Polite, neutral address.** Use the respectful plural/formal "you" form
  that businesses use with customers (Hindi आप, Marathi आपण/तुम्ही as fits the
  sentence, Gujarati આપ/તમે, Kannada ನೀವು, Telugu మీరు, Malayalam നിങ്ങൾ,
  Tamil நீங்கள்). Never the intimate form.
- **Do not add** "X, not Y" contrasts, and do not add explanations of your own.
  Never use the em dash (—). Use a comma, a full stop, a colon or brackets.

## What stays in Latin letters

- The company and mark: Santosh Magnetic Works, S-MAG, SMAG.
- Product and model names: Maxx, Maxx-300, Maxx-Demag, Filtramag, Filtramag XT,
  Ultrafiltrex, and any other capitalised model or series name.
- Grades, standards and codes: NdFeB, N35, N52, SS 304, 316, LM-6, ISO 9001,
  HACCP, BRC, IP65, CNC, GSTIN, PDF.
- Units and numbers exactly as written: mm, kg, gauss, °C, bar, inch, 6,000 kg,
  25.4 mm, 7,000 to 13,500 gauss. Keep Western digits (0-9). Do not convert
  units or reformat numbers.
- Phone numbers, email addresses, street addresses, URLs, WhatsApp,
  IndiaMART, Google Business.
- Client company names (Britannia, Castrol, Reliance and so on).

Common technical nouns that Indian engineers say in English (magnet, filter,
separator, chuck, lifter, grid, rod, housing, hopper, chute, conveyor,
coolant, pipeline, sieve, probe, sweeper, gauss meter, demagnetiser) should be
written **in your script as people say them** (Hindi: मैग्नेटिक सेपरेटर,
फ़िल्टर, चक, ग्रिड, रॉड, हॉपर). Use a native word only where it is the one
people really use (for example Hindi लोहा for iron, स्टील for steel, पाइप).
Material names people know in English (neodymium, alnico, ferrite, stainless
steel) are written in your script too.

## Placeholders

Segments can contain placeholders such as `{1}`, `{/1}` and `{2/}`. They stand
for links, bold text and line breaks. Rules:

- Keep every placeholder, exactly as written, the same number of times.
- `{1}` ... `{/1}` wrap words (usually a link or a bold label). Put your
  translation of those words between them. You may move the pair to where the
  words fall in your sentence, since word order differs from English.
- `{2/}` is a line break or an image. Keep it in the same place in the flow.
- Do not add placeholders that are not there.

Example: `See our guides on {1}critical control points{/1} and {3}supplier
audits{/3}` becomes, in Hindi, `हमारी गाइड {1}क्रिटिकल कंट्रोल पॉइंट्स{/1} और
{3}सप्लायर ऑडिट{/3} पर देखें`.

## Special segments

- Page titles end in ` | Santosh Magnetic Works`. Translate the part before
  the bar and keep ` | Santosh Magnetic Works` as it is.
- Headings are short labels. Translate them as labels.
- Image descriptions (alt text) and captions: translate plainly.
- Technical data rows such as `{1}Mounting:{/1} bolt-on or hinged frames`:
  translate the label and the value, keep numbers and codes.
- A segment that is only a name, code, number or brand: copy it unchanged.
- Navigation and button labels (Products, Industries, Guides, About Us,
  Contact Us, Get in touch, Explore product, Play, Pause): short and common,
  the way a well-made Indian business site in your language labels them.
- The footer line "Developed by Saahil Mehta": keep the name in Latin.

## Glossary

Before translating, write `assets/source/i18n/<lang>/glossary.md`: a table of
the recurring terms (product families, product names that are descriptive,
industries, recurring verbs such as "clean", "fit", "hold", "lift", units of
the cycle) with the one translation you will use. Keep it to the terms that
recur. The guides translator for your language will use the same file later.
