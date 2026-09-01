#!/usr/bin/env python3
"""Repair the image gaps the partial mirror crawl left behind.

The mirror fetched listing-tile renditions (355x205) for most products but
skipped many page-size renditions (590x548, 1000x0), so several kept pages
have always had broken galleries. Three repairs, in order:

1. Workholding pages get real SMAG photographs from the works' brochures
   (chucks and the Maxx-Demag demagnetiser) in place of the never-fetched
   Eclipse images: the right pictures for this site anyway.
2. On the other product pages, each broken gallery slide is repointed at the
   largest surviving rendition of the same photograph if one exists,
   otherwise the slide (and its thumbnail) is dropped.
3. Site-wide, any remaining <img> whose file is missing is removed, and
   srcset/data-zoom entries pointing at missing files are pruned.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_sections import find_element_end  # noqa: E402
import build_smag_product_pages as build  # noqa: E402

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

# workholding page -> [(master stem, alt text)]
SMAG_GALLERIES = {
    "products/workholding-systems/rectangular-premier-chuck": [
        ("rectangular-magnetic-chuck-01",
         "Rectangular permanent magnetic chuck with operating lever"),
        ("rectangular-magnetic-chuck-02",
         "Fine pole rectangular magnetic chuck"),
    ],
    "products/workholding-systems/rectangular-universal-chuck": [
        ("rectangular-magnetic-chuck-03",
         "Rectangular magnetic chuck with transverse poles"),
    ],
    "products/workholding-systems/circular-premier-chuck": [
        ("round-magnetic-chuck-01",
         "Circular permanent magnetic chuck with concentric poles"),
        ("round-magnetic-chuck-03",
         "Circular magnetic chuck showing the pole pattern"),
    ],
    "products/workholding-systems/circular-universal-chuck": [
        ("round-magnetic-chuck-02",
         "Circular magnetic chuck with radial poles and operating spanner"),
    ],
    "products/workholding-systems/table-top-demagnetiser": [
        ("table-top-demagnetiser-01",
         "Maxx-Demag table top demagnetiser"),
    ],
}

GALLERY_OPEN = ('<div class="product__gallery swiper-container '
                'gallery-swiper-container">')
THUMBS_OPEN = "<div class=product__thumbnails>"
SLIDE_OPEN = '<div class="product__image swiper-slide">'

SIZE_RE = re.compile(r"\.\d+x\d+(?:-crop[^.]*)?(?:\.\d+x0)?$")


def exists(url: str) -> bool:
    return (SITE / url.lstrip("/")).exists()


def best_substitute(url: str) -> str | None:
    """Largest surviving rendition of the same photo, or None."""
    p = SITE / url.lstrip("/")
    stem = SIZE_RE.sub("", p.stem)
    stem = re.sub(r"-1$", "", stem)
    if not p.parent.exists():
        return None
    cands = []
    for f in p.parent.iterdir():
        fstem = SIZE_RE.sub("", f.stem)
        if fstem in (stem, stem + "-1") and f.suffix.lower() in (
                ".jpg", ".jpeg", ".png", ".webp"):
            cands.append(f)
    if not cands:
        return None
    biggest = max(cands, key=lambda f: f.stat().st_size)
    return "/" + str(biggest.relative_to(SITE))


def replace_gallery(text: str, imgs: list[dict], alts: list[str]) -> str:
    i = text.find(GALLERY_OPEN)
    end = find_element_end(text, i)
    slides = "".join(build.slide(im, alt) for im, alt in zip(imgs, alts))
    gallery = (GALLERY_OPEN
               + f'<div class="product__images swiper-wrapper">{slides}</div>'
               "<button class=prev></button><button class=next></button>"
               "</div>")
    text = text[:i] + gallery + text[end:]
    j = text.find(THUMBS_OPEN)
    if j >= 0:
        tend = find_element_end(text, j)
        thumbs = ""
        if len(imgs) > 1:
            thumbs = (THUMBS_OPEN
                      + "".join(build.thumb(im, n + 1)
                                for n, im in enumerate(imgs))
                      + "</div>")
        text = text[:j] + thumbs + text[tend:]
    elif len(imgs) > 1:
        pass  # no thumbnail strip on this page; slides still swipe
    return text


def repair_slides(text: str) -> tuple[str, int, int]:
    """Repoint or drop broken gallery slides. Returns fixed, dropped."""
    fixed = dropped = 0
    out = []
    pos = 0
    for m in re.finditer(re.escape(SLIDE_OPEN), text):
        if m.start() < pos:
            continue
        end = find_element_end(text, m.start())
        slide = text[m.start():end]
        src = re.search(r"<img src=([^ >]+)", slide)
        if not src or exists(src.group(1)):
            continue
        sub = best_substitute(src.group(1))
        out.append((m.start(), end, slide, sub))
        pos = end
    for start, end, slide, sub in reversed(out):
        if sub:
            new = re.sub(r"(<img )src=[^ >]+( srcset=\"[^\"]*\")?",
                         rf"\1src={sub}", slide)
            new = re.sub(r"data-zoom=[^ >]+", f"data-zoom={sub}", new)
            text = text[:start] + new + text[end:]
            fixed += 1
        else:
            text = text[:start] + text[end:]
            dropped += 1
    return text, fixed, dropped


def prune_thumbs(text: str) -> tuple[str, int]:
    n = 0
    for m in reversed(list(re.finditer(
            r"<a href=# data-img=\d+><div style=\"background-image:"
            r"url\('([^']+)'\)\"></div></a>", text))):
        if not exists(m.group(1)):
            sub = best_substitute(m.group(1))
            if sub:
                text = (text[:m.start()]
                        + m.group(0).replace(m.group(1), sub)
                        + text[m.end():])
            else:
                text = text[:m.start()] + text[m.end():]
            n += 1
    return text, n


def clean_imgs(text: str) -> tuple[str, int]:
    """Remove <img> tags whose src is missing; prune dead srcset entries."""
    n = 0
    for m in reversed(list(re.finditer(r"<img\s[^>]*>", text))):
        tag = m.group(0)
        src = re.search(r'src=(?:"([^"]+)"|([^\s>]+))', tag)
        if not src:
            continue
        url = src.group(1) or src.group(2)
        if not url.startswith("/") or exists(url):
            # prune dead srcset candidates on live images
            ss = re.search(r'srcset="([^"]*)"', tag)
            if ss:
                keep = [c for c in ss.group(1).split(",")
                        if exists(c.strip().split(" ")[0])]
                newss = ",".join(keep)
                if newss != ss.group(1):
                    newtag = (tag.replace(ss.group(0), f'srcset="{newss}"')
                              if keep else tag.replace(ss.group(0), ""))
                    text = text[:m.start()] + newtag + text[m.end():]
                    n += 1
            continue
        sub = best_substitute(url)
        if sub:
            newtag = re.sub(r'src=(?:"[^"]+"|[^\s>]+)', f"src={sub}", tag)
            newtag = re.sub(r'\s*srcset="[^"]*"', "", newtag)
            text = text[:m.start()] + newtag + text[m.end():]
        else:
            text = text[:m.start()] + text[m.end():]
        n += 1
    return text, n


def clean_sources(text: str) -> tuple[str, int]:
    """Remove <source> tags whose file is missing; drop emptied <picture>s.

    Some banner directories were never crawled at all, so there is nothing
    to substitute; the banner then degrades to its styled text-only form.
    """
    n = 0
    for m in reversed(list(re.finditer(r"<source\s[^>]*>", text))):
        src = re.search(r'src=(?:"([^"]+)"|([^\s>]+))', m.group(0))
        if not src:
            continue
        url = src.group(1) or src.group(2)
        if not url.startswith("/site/") or exists(url):
            continue
        text = text[:m.start()] + text[m.end():]
        n += 1
    text, empties = re.subn(r"<picture>\s*</picture>", "", text)
    return text, n + empties


def main() -> None:
    dry = "--dry-run" in sys.argv

    for rel, specs in SMAG_GALLERIES.items():
        page = SITE / rel / "index.html"
        text = page.read_text(encoding="utf-8")
        imgs = [build.renditions(stem) for stem, _ in specs]
        text = replace_gallery(text, imgs, [alt for _, alt in specs])
        print(f"SMAG gallery ({len(specs)} photos): {rel}")
        if not dry:
            page.write_text(text, encoding="utf-8")

    totals = [0, 0, 0, 0]
    for page in sorted(SITE.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        new, f1, d1 = repair_slides(text)
        new, t1 = prune_thumbs(new)
        new, c1 = clean_imgs(new)
        new, s1 = clean_sources(new)
        c1 += s1
        if new == text:
            continue
        totals[0] += f1
        totals[1] += d1
        totals[2] += t1
        totals[3] += c1
        print(f"  slides fixed {f1}, dropped {d1}, thumbs {t1}, "
              f"imgs {c1}: {page.relative_to(SITE)}")
        if not dry:
            page.write_text(new, encoding="utf-8")
    print(f"\nslides repointed {totals[0]}, slides dropped {totals[1]}, "
          f"thumbs {totals[2]}, imgs cleaned {totals[3]}")


if __name__ == "__main__":
    main()
