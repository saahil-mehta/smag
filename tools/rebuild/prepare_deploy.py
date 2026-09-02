#!/usr/bin/env python3
"""Make site/ a clean, self-contained web root for GitHub Pages.

  - deletes every asset no page or stylesheet references (1,374 Eclipse CMS
    files, about 104 MB, including the only images whose metadata still
    named Eclipse); Font Awesome webfonts are kept whole
  - removes the ProcessWire generator meta (Eclipse's CMS fingerprint)
  - writes robots.txt and sitemap.xml for santoshmagneticworks.com
  - generates the favicon set the pages already link to, from the SMAG
    logo (assets/logo.svg, assets/source/logo-mark.png, repo favicon.ico)
  - writes a 404 page in the site chrome, plus CNAME and .nojekyll

Idempotent. Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/Users/saahil/Documents/GitHub/smag")
SITE = REPO / "site"
DOMAIN = "https://santoshmagneticworks.com"
KEEP_PREFIX = ("site/assets/fontawesome/",)
KEEP_NAMES = {"robots.txt", "sitemap.xml", "CNAME", ".nojekyll", "404.html",
              "favicon.ico", "favicon.svg", "apple-touch-icon.png",
              "favicon-32x32.png", "favicon-16x16.png"}


def referenced() -> set[str]:
    refs: set[str] = set()
    for p in SITE.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        for m in re.finditer(r'(?:src|href|data-zoom|poster|content)=["\']?(/[^"\' >,)]+)', t):
            refs.add(m.group(1).split("?")[0].split("#")[0])
        for m in re.finditer(r'srcset="([^"]*)"', t):
            for c in m.group(1).split(","):
                u = c.strip().split(" ")[0]
                if u:
                    refs.add(u)
        for m in re.finditer(r"url\((/[^)]+)\)", t):
            refs.add(m.group(1))
    for c in SITE.rglob("*.css"):
        for m in re.finditer(r'url\(["\']?(/[^"\')]+)', c.read_text(encoding="utf-8", errors="replace")):
            refs.add(m.group(1).split("?")[0])
    return refs


def prune_orphans(dry: bool) -> None:
    refs = referenced()
    gone = size = 0
    for p in list(SITE.rglob("*")):
        if not p.is_file() or p.suffix == ".html":
            continue
        rel = p.relative_to(SITE).as_posix()
        if rel.startswith(KEEP_PREFIX) or p.name in KEEP_NAMES or "/" + rel in refs:
            continue
        gone += 1
        size += p.stat().st_size
        if not dry:
            p.unlink()
    if not dry:
        for d in sorted((d for d in SITE.rglob("*") if d.is_dir()), reverse=True):
            if not any(d.iterdir()):
                d.rmdir()
    print(f"orphan assets removed: {gone} ({size / 1e6:.0f} MB)")


def strip_generator(dry: bool) -> None:
    n = 0
    for p in SITE.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        new = re.sub(r"<meta name=generator content=ProcessWire>", "", t)
        if new != t:
            n += 1
            if not dry:
                p.write_text(new, encoding="utf-8")
    print(f"generator meta removed from {n} pages")


def write(path: Path, content: str | bytes, dry: bool) -> None:
    if dry:
        return
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def robots_and_sitemap(dry: bool) -> None:
    urls = []
    for p in sorted(SITE.rglob("index.html")):
        rel = p.parent.relative_to(SITE).as_posix()
        if rel in ("sitemap",) or rel.startswith("information"):
            continue
        urls.append(DOMAIN + ("/" if rel == "." else f"/{rel}/"))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write(SITE / "sitemap.xml", xml, dry)
    write(SITE / "robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n", dry)
    write(SITE / "CNAME", "santoshmagneticworks.com\n", dry)
    write(SITE / ".nojekyll", "", dry)
    print(f"sitemap.xml: {len(urls)} urls; robots.txt, CNAME, .nojekyll written")


def favicons(dry: bool) -> None:
    mark = REPO / "assets/source/logo-mark.png"
    if dry:
        print("favicons: would generate from logo-mark.png")
        return
    shutil.copy(REPO / "assets/logo.svg", SITE / "favicon.svg")
    shutil.copy(REPO / "favicon.ico", SITE / "favicon.ico")
    for name, px in (("apple-touch-icon.png", 180), ("favicon-32x32.png", 32), ("favicon-16x16.png", 16)):
        # the mark is wide (954 x 259): fit it to the width, pad to a square
        subprocess.run(["sips", "-s", "format", "png", "--resampleWidth", str(px),
                        "--padToHeightWidth", str(px), str(px), "--padColor", "FFFFFF",
                        str(mark), "--out", str(SITE / name)], check=True, capture_output=True)
    print("favicons: svg, ico, 180, 32, 16 written")


def not_found(dry: bool) -> None:
    donor = (SITE / "contact-us/index.html").read_text(encoding="utf-8")
    ms, me = donor.find("<main"), donor.find("</main>") + len("</main>")
    main = ('<main><div class="content-wrapper content-wrapper--no-testimonials">'
            '<div class=row><div class="row__inner content content--text_1">'
            "<div><h2 class=configurable-header>Page not found</h2></div>"
            "<div class=content__body><p>The page you asked for is not here. It may have moved "
            "when we rebuilt the site.<p>Try the <a href=/>home page</a>, the "
            "<a href=/products/magnetic-separation-and-metal-detection/>separation range</a> or the "
            "<a href=/sitemap/>sitemap</a>, or <a href=/contact-us/>ask us</a> and we will point you "
            "to the right place.</div></div></div></div></main>")
    page = donor[:ms] + main + donor[me:]
    page = re.sub(r"<title>[^<]*</title>", "<title>Page not found | Santosh Magnetic Works</title>", page)
    page = re.sub(r'(<meta name=description content=)"[^"]*"', r'\1"Page not found."', page)
    page = re.sub(r"<script type=application/ld\+json>.*?</script>", "", page, flags=re.S)
    page = page.replace("<head>", "<head><meta name=robots content=noindex>", 1) if "<head>" in page else page
    write(SITE / "404.html", page, dry)
    print("404.html written")


def main() -> None:
    dry = "--dry-run" in sys.argv
    strip_generator(dry)
    prune_orphans(dry)
    robots_and_sitemap(dry)
    favicons(dry)
    not_found(dry)
    total = sum(p.stat().st_size for p in SITE.rglob("*") if p.is_file()) / 1e6
    print(f"site/ is now {total:.0f} MB, {len(list(SITE.rglob('*.html')))} html files")


if __name__ == "__main__":
    main()
