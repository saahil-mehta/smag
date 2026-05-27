# Santosh Magnetic Works

Static marketing site for Santosh Magnetic Works (SMAG), a Mumbai
manufacturer of magnetic separation and holding equipment since 1978.

Hosted on GitHub Pages, served from the repository root.

## Status

Work in progress. Branding, palette, and copy are being reskinned onto
the layout. Some sections still carry placeholder content.

## Known gaps

- Some images currently load from an external CDN and will be localised
  into this repo.
- The contact form is not yet wired to a handler.
- Custom domain (`santoshmagneticworks.com`) and email are stage 2,
  pending DNS setup.

## Local preview

```sh
make web          # serves on http://localhost:8000
```

Override the port with `make web PORT=9000`.

## Hosting

GitHub Pages, served from the repository root on the default branch.
`.nojekyll` disables the Jekyll build so files are served as-is.
