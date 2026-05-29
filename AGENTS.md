# AGENTS.md

Durable operating notes for coding agents in `smag`.

Keep this file small. It should describe invariants, boundaries, and judgement, not mirror current tool settings, package versions, command lists, or temporary plans.

## How To Use This File

- Read `CLAUDE.md` first. It is canonical for output style, commit policy, engineering stance, and project context.
- Use current code, README, Makefile, and `_partials/README.md` as implementation context. Prefer live code over stale documentation.
- If this file and `CLAUDE.md` disagree, follow `CLAUDE.md`, then apply the stricter engineering constraint.
- Update this file only for rules expected to remain true as the repo evolves.
- Avoid adding temporary plan state, tool-specific behaviour, model-specific tuning, or duplicate command documentation.

## Engineering Stance

- Read surrounding code before changing it.
- Prefer root-cause fixes over surface patches.
- Keep changes small, bisectable, and scoped to the request.
- Preserve user changes. Never revert unrelated edits.
- Avoid new abstractions until they remove real duplication or match an established local pattern.
- Follow existing entry points and local conventions rather than inventing parallel workflows.

## Static Site Boundaries

- Edit `_partials/` for shared navbar or footer changes, then run `make build` and commit regenerated pages.
- Edit `assets/` for shared styling, animation, image, and navigation behaviour.
- Treat Framer-exported HTML as fragile. Prefer scoped CSS or partial edits over broad generated-markup rewrites.
- Keep local assets local where practical. External CDN content should be considered temporary unless intentionally retained.
- GitHub Pages serves from the repository root, so paths must work without a bundler.

## App And UI Work

- Keep the site focused on Santosh Magnetic Works and industrial magnetic equipment.
- Use the existing visual system, typography, image treatment, navigation, animation, and button patterns unless the task explicitly changes them.
- Make visible changes responsive across desktop and mobile.
- Check for clipping, overlap, unwanted seams, unreadable contrast, broken wrapping, and excessive layout shift.
- Preserve clear hierarchy. Large display type should support the product story, not obscure inspection of machinery or calls to action.
- User-facing copy should be concise, factual, and brand-appropriate.

## Validation And Handoff

- Run the narrowest useful validation for the files changed.
- Use documented project entry points instead of ad hoc commands where they exist.
- For visual work, inspect the affected page in a browser when feasible.
- If validation cannot run, state why and name the next best check.
- Before handoff, confirm changed files, validation, known risks, and any follow-up that blocks correctness.
- Keep final notes concise and grounded in file paths.
