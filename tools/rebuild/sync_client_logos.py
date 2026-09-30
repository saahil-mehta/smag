#!/usr/bin/env python3
"""Keep the client logo strips in step with assets/logos/.

A logo added to assets/logos/ is copied to the site and placed in the home
and About strips in alphabetical order, sized by polish_ux.py's equal-area
rule so no logo shouts over its neighbours. Run after tidy_logo_strip.py.

With 31 logos no column count gives full rows, so "+ many more" becomes the
32nd cell and the grid runs 8, 4 or 2 columns: full rows at every width.
Re-running changes nothing.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from polish_ux import CLIENTS, SITE, logo_heights  # noqa: E402

SRC = Path("/Users/saahil/Documents/GitHub/smag/assets/logos")
PAGES = [SITE / "index.html", SITE / "company/about-us/index.html"]
NAMES = {"supreme": "Supreme"}
STRIP = re.compile(r"<div class=clients-strip>(.*?)</div>(?:<p class=clients-more>[^<]*</p>)?", re.S)
IMG = re.compile(r"<img [^>]*src=/site/assets/images/clients/([^ >]+)[^>]*>")
MORE = "<span class=clients-more>+ many more</span>"
STYLE = re.compile(r"<style id=smag-clients-css>.*?</style>", re.S)
CSS = (
    "<style id=smag-clients-css>"
    ".clients-strip{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));"
    "gap:36px 32px;align-items:center;justify-items:center}"
    ".clients-strip img{height:60px;width:auto;max-width:100%;object-fit:contain}"
    ".clients-more{font-weight:600;color:#6b6770;white-space:nowrap}"
    "@media(max-width:1180px){.clients-strip{grid-template-columns:repeat(4,minmax(0,1fr));gap:36px 40px}}"
    "@media(max-width:540px){.clients-strip{grid-template-columns:repeat(2,minmax(0,1fr));gap:26px 20px}}"
    "</style>"
)


def main() -> int:
    for src in SRC.iterdir():
        if src.suffix.lower() in (".png", ".svg") and not (CLIENTS / src.name).exists():
            shutil.copyfile(src, CLIENTS / src.name)
    heights = logo_heights()
    for page in PAGES:
        s = page.read_text(encoding="utf-8")
        m = STRIP.search(s)
        tags = {g.group(1): g.group(0) for g in IMG.finditer(m.group(1))}
        for name in heights:
            if name not in tags:
                stem = name.rsplit(".", 1)[0]
                alt = NAMES.get(stem, stem.replace("-", " ").title())
                tags[name] = f'<img src=/site/assets/images/clients/{name} alt="{alt}" loading=lazy decoding=async>'
        imgs = [re.sub(r' style="height:\d+px"', "", tags[n]).replace("<img ", f'<img style="height:{heights[n]}px" ', 1)
                for n in sorted(tags)]
        s = s[:m.start()] + "<div class=clients-strip>" + "".join(imgs) + MORE + "</div>" + s[m.end():]
        s = STYLE.sub(CSS, s, count=1)
        page.write_text(s, encoding="utf-8")
        print(f"  {page.relative_to(SITE)}: {len(imgs)} logos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
