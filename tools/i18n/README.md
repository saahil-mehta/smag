# Languages

The site is published in English at `/` and in Hindi, Marathi, Gujarati,
Kannada, Telugu, Malayalam and Tamil at `/hi/`, `/mr/`, `/gu/`, `/kn/`,
`/te/`, `/ml/` and `/ta/`. The language pages are built from the English
pages: English stays the one source of layout and markup, and a translation
only ever replaces text.

| Step | Command | What it does |
|---|---|---|
| 1 | `make i18n-extract` | `extract.py` splits every English page (the policies aside) into segments and writes `assets/source/i18n/catalogue.json`; `split_work.py` cuts it into `work/site-NN.json` and `work/guides-NN.json` |
| 2 | translate | each language writes `assets/source/i18n/<lang>/<part>.json` as `{"id": "translation"}`, following `STYLE.md` and its own `glossary.md` |
| 3 | `make i18n-check` | `check.py` reports missing segments, changed placeholders, lost numbers, em dashes and likely untranslated text |
| 4 | `make i18n` | `build.py` writes `site/<lang>/`, adds hreflang alternates and the language menu to every page, and lists the language pages in `sitemap.xml` |

`segments.py` holds the splitting and the swap. A segment is a run of text
and inline tags between block boundaries; inline tags become `{1}`, `{/1}`,
`{2/}` placeholders so a translator can reorder a sentence around a link.
Readable attributes (alt, title, placeholder, aria-label, data-text, the
Play and Pause labels, meta descriptions) are segments too. A segment's id is
a hash of its English text, so the header and footer are translated once.

A page is published in a language once at least 97% of its segments are
translated. Links to pages not yet translated stay on the English page.

When English copy changes, re-run step 1. Segments whose English changed get
new ids and show up as missing in step 3; everything else carries over.

Fonts: `tools/rebuild/build_noto_webfonts.py --indic <dir>` builds Noto Sans
for the six scripts under the one 'Noto Sans' family, each with its own
unicode range, so a page downloads only the script it uses.
