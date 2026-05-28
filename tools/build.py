#!/usr/bin/env python3
"""SMAG static site build: assemble HTML pages from _partials/.

Source files are the HTML pages at the repo root and under nested
directories (blogs/, projects/, package/). Each page contains marker
pairs like

    <!-- @nav -->...<!-- @/nav -->

whose contents are replaced by the file _partials/nav.html on every
build. Markers are kept so the next build still finds them.

Path placeholders {{ROOT}} in partials are rewritten per page based on
directory depth, so a partial containing

    <a href="{{ROOT}}index.html">

resolves to href="index.html" at the repo root and href="../index.html"
inside blogs/, projects/, or package/.

Run via `make build`. Idempotent: a second run produces no diff.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PARTIALS_DIR = REPO / "_partials"
SKIP_DIRS = {"_partials", "framer-reference", "tools", "node_modules", ".git"}

MARKER_RE = re.compile(
    r"(<!--\s*@([a-z][a-z0-9_-]*)\s*-->)(.*?)(<!--\s*@/\2\s*-->)",
    re.DOTALL,
)


def page_prefix(path: Path) -> str:
    return "../" * (len(path.relative_to(REPO).parts) - 1)


def load_partial(name: str) -> str:
    p = PARTIALS_DIR / f"{name}.html"
    if not p.exists():
        sys.exit(f"build: missing partial {p}")
    return p.read_text(encoding="utf-8").rstrip("\n")


def build_page(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    prefix = page_prefix(path)

    def sub(m: re.Match) -> str:
        open_tag, name, _old, close_tag = m.group(1, 2, 3, 4)
        body = load_partial(name).replace("{{ROOT}}", prefix)
        return f"{open_tag}{body}{close_tag}"

    rewritten = MARKER_RE.sub(sub, original)
    if rewritten != original:
        path.write_text(rewritten, encoding="utf-8")
        return True
    return False


def iter_pages() -> list[Path]:
    pages: list[Path] = []
    for p in REPO.rglob("*.html"):
        rel = p.relative_to(REPO)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        pages.append(p)
    return sorted(pages)


def main() -> None:
    pages = iter_pages()
    changed = [p for p in pages if build_page(p)]
    print(f"build: {len(pages)} pages scanned, {len(changed)} updated")


if __name__ == "__main__":
    main()
