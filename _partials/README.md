# `_partials/`

Shared HTML fragments assembled into the static pages by
`tools/build.py`. Each `.html` file here is referenced by name from a
marker pair in any page:

    <!-- @nav -->...injected content...<!-- @/nav -->

`_partials/nav.html` fills any `<!-- @nav --><!-- @/nav -->` pair,
`_partials/footer.html` (when added) fills `<!-- @footer -->` pairs,
and so on. The marker name and the partial filename match.

## Path placeholder

Pages live at the repo root or one level deep (`blogs/`, `projects/`,
`package/`). Relative paths in partials use the literal placeholder
`{{ROOT}}`, which the build rewrites per page:

| Page                                | `{{ROOT}}` becomes |
| ----------------------------------- | ------------------ |
| `index.html`                        | `` (empty)         |
| `blogs/ai-customer-engagement.html` | `../`              |

So `<a href="{{ROOT}}index.html">` resolves correctly from any depth.

## Workflow

1. Edit a file in `_partials/`.
2. Run `make build`.
3. Commit both the partial and the regenerated pages.

`make build` is idempotent: running twice produces no diff. Pages
without the relevant marker pair are skipped.

## Adding a new partial

1. Create `_partials/<name>.html`.
2. Put `<!-- @<name> --><!-- @/<name> -->` wherever you want it injected
   in any page.
3. Run `make build`.
