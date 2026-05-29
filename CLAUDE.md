# Project: Santosh Magnetic Works

Static marketing site for Santosh Magnetic Works (SMAG), a Mumbai manufacturer of magnetic separation and holding equipment since 1978.

<must_follow>
- Reliability and simplicity. KISS, DRY, YAGNI.
- Root-cause thinking. Avoid hacky fixes.
- Small increments: make one focused change, verify it, then move on.
- Use `make` targets where they exist. `Makefile` is the project entry point.
- Preserve user changes. Never revert unrelated edits.
- `.gitignore` by intent, not by extension.
</must_follow>

<debugging>
## Debugging Philosophy

The principle sticks, the stack drifts. These hold for any debugging task in any system.

- **Evidence outranks assertion, regardless of source.** A hypothesis grounded in observation holds against verbal claims, including the user's, memory, and confident documentation. Claims describe a model of state; the live system is state. When a claim contradicts a strong prior, verify cheaply instead of pivoting.

- **Look before you theorise.** When something is opaque, fetching the next layer of detail is almost always cheaper than constructing a story that explains the visible symptom. Pull the log, dump the state, run the diff first, then build the narrative.

- **Keep observation and explanation separate.** The user's symptoms are data and should be taken as given. The user's causal explanation is a hypothesis on equal footing with any other.

- **Boring causes outnumber dramatic ones.** A failure pattern that feels complex usually decomposes into many identical small failures, or one root presenting at many surfaces. Reach for the boring explanation first.

- **Described state drifts from applied state.** Written state, such as docs or config comments, can diverge from runtime state. When correctness depends on which is true, query the live system.

- **A fix without a confirmed root cause is a guess wearing a uniform.** Shipping a guess is sometimes acceptable when the cost is low, but call it a guess. Guard the difference between evidence and plausibility.
</debugging>

## Stack Pointers

- Static HTML exported from Framer and reskinned locally.
- Shared chrome lives in `_partials/`.
- `tools/build.py` assembles marker-bounded partial sections into pages.
- Custom site behaviour and polish live under `assets/`.
- GitHub Pages serves the repository root.

Read current code, README, Makefile, and partial documentation before changing generated-looking HTML.

## Commit Policy

Conventional commits: `<type>(<scope>): <subject>`, lowercase and imperative.

Types: `feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert`.

- One logical change per commit. Bisectable.
- Never bundle unrelated changes.
- Do not co-author or attribute.

## Output Policy

- UK English.
- No emojis.
- No em dashes. Use commas, parentheses, colons, or new sentences.
- Plain, direct wording.
- Say what is uncertain when evidence is missing.
- Keep final notes concise and grounded in file paths.
