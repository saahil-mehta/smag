#!/usr/bin/env python3
"""Strip Eclipse's third-party trackers from site/.

Removes whole <script> and <noscript> blocks whose contents match a known
tracker signature, plus bare tracking pixels. Everything is matched on the
block's own text, and the block patterns are anchored on their closing tags,
so a match can never run past the element it started in.

Kept deliberately:
  use.typekit.net   Adobe Fonts. A third-party request and Eclipse's kit, but
                    typography not tracking; removing it changes the design.
  facebook/twitter/linkedin.com links   outbound share links, inert until clicked.
  www.w3.org, schema.org                namespace and vocabulary URLs, never fetched.

Run with --dry-run to report without writing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = Path("/Users/saahil/Documents/GitHub/smag/site")

# Signature -> human label. A block matching any of these goes.
SIGS = {
    "googletagmanager": "Google Tag Manager",
    "GTM-": "Google Tag Manager",
    "diffuser-cdn.app-us1.com": "ActiveCampaign",
    "visitorGlobalObjectAlias": "ActiveCampaign",
    "activehosted.com": "ActiveCampaign",
    "_linkedin_partner_id": "LinkedIn Insight",
    "snap.licdn.com": "LinkedIn Insight",
    "px.ads.linkedin.com": "LinkedIn pixel",
    "365-bright-astute": "OptiMonk",
    "optimonk": "OptiMonk",
    "hm.baidu.com": "Baidu Analytics",
    "cookieyes": "CookieYes",
    # Cloudflare bot-challenge loader baked into the crawl; it injects a
    # hidden iframe and requests /cdn-cgi/, which 404s on the static host
    "cdn-cgi/challenge-platform": "Cloudflare challenge",
    "cloudflare-static/email-decode": "Cloudflare email obfuscation",
}

BLOCK_RES = [
    re.compile(r"<script\b[^>]*>.*?</script\s*>", re.DOTALL | re.I),
    re.compile(r"<noscript\b[^>]*>.*?</noscript\s*>", re.DOTALL | re.I),
]

# Tracking pixels sitting outside a noscript wrapper.
PIXEL_RE = re.compile(
    r"<img[^>]+(?:px\.ads\.linkedin\.com|hm\.baidu\.com)[^>]*>", re.I
)


def label_for(block: str) -> str | None:
    low = block.lower()
    for sig, name in SIGS.items():
        if sig.lower() in low:
            return name
    return None


def main() -> None:
    dry = "--dry-run" in sys.argv
    removed: dict[str, int] = {}
    pixels = 0
    files = 0

    for page in sorted(SITE.rglob("*.html")):
        try:
            text = page.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        original = text

        for block_re in BLOCK_RES:
            def sub(m):
                name = label_for(m.group(0))
                if name:
                    removed[name] = removed.get(name, 0) + 1
                    return ""
                return m.group(0)

            text = block_re.sub(sub, text)

        text, n = PIXEL_RE.subn("", text)
        pixels += n

        if text != original:
            files += 1
            if not dry:
                page.write_text(text, encoding="utf-8")

    print(f"{'DRY RUN: ' if dry else ''}{files} files affected\n")
    for name in sorted(removed, key=lambda k: -removed[k]):
        print(f"  {removed[name]:>5}  {name}")
    print(f"  {pixels:>5}  bare tracking pixels")
    print(f"  {sum(removed.values()) + pixels:>5}  total blocks removed")

    print("\nremaining references by host:")
    hosts = [
        "googletagmanager",
        "app-us1",
        "365-bright-astute",
        "licdn",
        "linkedin.com/px",
        "px.ads.linkedin",
        "hm.baidu.com",
        "activehosted",
        "optimonk",
        "GTM-",
        "use.typekit.net",
    ]
    for h in hosts:
        hits = sum(
            p.read_text(encoding="utf-8", errors="replace").count(h)
            for p in SITE.rglob("*.html")
        )
        note = "  (kept: fonts)" if "typekit" in h else ""
        print(f"  {hits:>5}  {h}{note}")


if __name__ == "__main__":
    main()
