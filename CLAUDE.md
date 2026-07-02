# Project: Santosh Magnetic Works

Static marketing site for Santosh Magnetic Works (SMAG), a Mumbai manufacturer of magnetic separation and holding equipment since 1978.

## Principles

- KISS, DRY, YAGNI. Reliability and simplicity first.
- Root-cause thinking. No hacky fixes.
- Small, verified increments. One focused change at a time.
- Use `make` targets. The `Makefile` is the entry point.
- Preserve user changes. Never revert unrelated edits.

## Layout

- `site/` — the working copy of the site (static HTML/CSS/JS), edited toward the SMAG build.
- `reference-mirror/` — pristine reference, do not edit.
- `make serve-site` / `make serve-mirror` — preview each locally.

## Conventions

- UK English. No emojis. No em dashes.
- Conventional commits (`type(scope): subject`), lowercase, imperative. One change per commit. Commit only when asked.
- Plain, direct wording. Say what is uncertain.
