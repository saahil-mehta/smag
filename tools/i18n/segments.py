"""Split a built English page into translatable segments, and put translations back.

The pages are minified and leave out optional end tags, so they are read as a
stream of tags and text and never re-serialised: a translated page is the
English page with only its segments swapped, byte for byte everywhere else.

A segment is a run of text and inline tags between two block boundaries,
such as a paragraph with a link in it. Inline tags become numbered
placeholders, {1} and {/1} around text or {1/} for a void tag, so a
translator can move them with the words; the real tags go back in on output.
Attributes that people read (alt, title, placeholder, aria-label, a few meta
contents and the animation button labels) are segments of their own.

The key of a segment is its placeholder text, so the header, footer and any
sentence repeated across pages are translated once.
"""
from __future__ import annotations

import hashlib
import html
import re

TOKEN = re.compile(r"<!--.*?-->|<![^>]*>|</?[a-zA-Z][^>]*>|[^<]+|<", re.S)
TAG = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)", re.S)
INLINE = {"a", "strong", "b", "em", "i", "span", "br", "sup", "sub", "small",
          "abbr", "code", "u", "mark", "time", "tspan"}
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "area", "col", "embed"}
RAW = {"script", "style", "textarea"}
LETTER = re.compile(r"[A-Za-z]")
ATTRS = ("alt", "title", "placeholder", "aria-label", "data-text", "data-play", "data-pause")
META_NAMES = {"description", "og:title", "og:description", "twitter:title", "twitter:description"}
ATTR_RE = r'(\s{name}=)("[^"]*"|\'[^\']*\'|[^\s>]+)'

# Kept in Latin letters on every page: the pinned logo lockup, the company
# name as a mark, contact details and model codes are handled by translators.
KEEP = {"Leaders In Magnetic Engineering", "S-MAG"}


def key_of(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def tokens(page: str):
    """(kind, raw, name) for each token; kind is tag, text or other.

    Joined back together the raws are exactly the page."""
    out, pos, low = [], 0, page.lower()
    while pos < len(page):
        m = TOKEN.match(page, pos)
        raw = m.group(0)
        if raw.startswith("<!") or raw == "<":
            out.append(("other", raw, ""))
        elif raw.startswith("<"):
            name = TAG.match(raw).group(1).lower()
            out.append(("tag", raw, name))
            if name in RAW and not raw.startswith("</"):
                end = low.find(f"</{name}", m.end())
                end = len(page) if end < 0 else end
                if end > m.end():
                    out.append(("other", page[m.end():end], ""))
                pos = end
                continue
        else:
            out.append(("text", raw, ""))
        pos = m.end()
    return out


def _is_inline(tok) -> bool:
    kind, raw, name = tok
    return kind == "text" or (kind == "tag" and name in INLINE)


def encode(run) -> tuple[str, list[str]]:
    """Placeholder text for a run of inline tokens, and the tags it stands for."""
    parts, tags, stack = [], [], []
    for kind, raw, name in run:
        if kind == "text":
            parts.append(html.unescape(raw))
            continue
        tags.append(raw)
        n = len(tags)
        if raw.startswith("</"):
            opener = next((i for i in range(len(stack) - 1, -1, -1) if stack[i][0] == name), None)
            if opener is not None:
                parts.append(f"{{/{stack[opener][1]}}}")
                del stack[opener]
            else:
                parts.append(f"{{/{n}}}")
        elif name in VOID:
            parts.append(f"{{{n}/}}")
        else:
            stack.append((name, n))
            parts.append(f"{{{n}}}")
    return "".join(parts), tags


PH = re.compile(r"\{(/?)(\d+)(/?)\}")


def decode(text: str, run) -> str:
    """Translated placeholder text back to HTML, with the run's own tags."""
    _, tags = encode(run)
    opens = {}
    # map placeholder number to tag raw: open/void use their own index,
    # a close uses the index of its opener
    n = 0
    stack = []
    close_for = {}
    for kind, raw, name in run:
        if kind != "tag":
            continue
        n += 1
        if raw.startswith("</"):
            opener = next((i for i in range(len(stack) - 1, -1, -1) if stack[i][0] == name), None)
            if opener is not None:
                close_for[stack[opener][1]] = raw
                del stack[opener]
            else:
                close_for[n] = raw
        else:
            opens[n] = raw
            if name not in VOID:
                stack.append((name, n))
    out, pos = [], 0
    for m in PH.finditer(text):
        out.append(html.escape(text[pos:m.start()], quote=False))
        i = int(m.group(2))
        out.append(close_for.get(i, "") if m.group(1) else opens.get(i, ""))
        pos = m.end()
    out.append(html.escape(text[pos:], quote=False))
    return "".join(out)


def _units(toks, a: int, b: int):
    """Top-level pieces of an inline run: (start, end, is_element, has_letters)."""
    out, i = [], a
    while i < b:
        kind, raw, name = toks[i]
        if kind == "text":
            out.append((i, i + 1, False, bool(LETTER.search(html.unescape(raw)))))
            i += 1
            continue
        j, depth = i + 1, 0 if (name in VOID or raw.startswith("</")) else 1
        while depth and j < b:
            k2, r2, n2 = toks[j]
            if k2 == "tag" and n2 not in VOID:
                depth += -1 if r2.startswith("</") else 1
            j += 1
        text = html.unescape("".join(r for k, r, _ in toks[i:j] if k == "text"))
        out.append((i, j, True, bool(LETTER.search(text))))
        i = j
    return out


def _groups(toks, a: int, b: int):
    """Split an inline run where two elements meet with no words between them,
    so a row of links is one segment per link and a sentence with a link in
    it stays whole."""
    units = _units(toks, a, b)
    groups, cur = [], []
    for n, u in enumerate(units):
        is_el, letters = u[2], u[3]
        if not cur:
            if letters or is_el:
                cur = [u]
            continue
        prev = cur[-1]
        nxt = units[n + 1] if n + 1 < len(units) else None
        if is_el and prev[2]:
            groups.append(cur)
            cur = [u]
        elif not is_el and not letters and prev[2] and (nxt is None or nxt[2]):
            groups.append(cur)
            cur = []
        else:
            cur.append(u)
    if cur:
        groups.append(cur)
    for g in groups:
        s, e = g[0][0], g[-1][1]
        # peel wordless pieces (icons, separators, spaces) off both edges,
        # and a wrapper element that spans the whole group
        while True:
            us = _units(toks, s, e)
            while us and not us[0][3]:
                us.pop(0)
            while us and not us[-1][3]:
                us.pop()
            if not us:
                s = e
                break
            s, e = us[0][0], us[-1][1]
            if (len(us) == 1 and us[0][2] and e - s >= 2
                    and toks[e - 1][1].startswith(f"</{toks[s][2]}")):
                # the wrapper's contents may hold several pieces of their own
                yield from _groups(toks, s + 1, e - 1)
                s = e
            break
        if s < e:
            yield s, e


def segments(page: str):
    """The token list, and (start, end) token ranges of its segments."""
    toks = tokens(page)
    found = []
    i, in_svg, in_svg_text = 0, 0, 0
    while i < len(toks):
        kind, raw, name = toks[i]
        if kind == "tag" and name == "svg":
            in_svg += -1 if raw.startswith("</") else 1
        if kind == "tag" and in_svg and name == "text":
            in_svg_text = 0 if raw.startswith("</") else 1
        if (in_svg and not in_svg_text) or not _is_inline(toks[i]):
            i += 1
            continue
        j = i
        while j < len(toks) and _is_inline(toks[j]):
            j += 1
        for a, b in _groups(toks, i, j):
            if a >= b:
                continue
            text = encode(toks[a:b])[0].strip()
            if LETTER.search(text) and text not in KEEP:
                found.append((a, b))
        i = j
    return toks, found


def segment_text(run) -> tuple[str, str, str]:
    """(leading space, placeholder text, trailing space) of a run."""
    text, _ = encode(run)
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    return lead, text.strip(), trail


def attr_segments(raw: str):
    """(attribute name, value) pairs in one tag that people read."""
    name = TAG.match(raw).group(1).lower() if raw.startswith("<") else ""
    out = []
    names = list(ATTRS)
    if name == "meta":
        m = re.search(r'\s(?:name|property)=("?)([^"\s>]+)\1', raw)
        if m and m.group(2) in META_NAMES:
            names.append("content")
    if name == "input" and re.search(r"\stype=(\"?)(submit|button)\1", raw):
        names.append("value")
    for a in names:
        m = re.search(ATTR_RE.format(name=re.escape(a)), raw)
        if m:
            v = html.unescape(m.group(2).strip("\"'"))
            if LETTER.search(v) and v not in KEEP:
                out.append((a, v))
    return out


def set_attr(raw: str, attr: str, value: str) -> str:
    v = html.escape(value, quote=True)
    return re.sub(ATTR_RE.format(name=re.escape(attr)), lambda m: f'{m.group(1)}"{v}"', raw, count=1)


def translate(page: str, lookup) -> tuple[str, int, int]:
    """The page with every segment passed through lookup(text) -> str | None.

    Returns the new page, segments translated, and segments left in English
    (lookup returned None)."""
    toks, found = segments(page)
    starts = {a: b for a, b in found}
    out, done, left, i = [], 0, 0, 0
    while i < len(toks):
        if i in starts:
            b = starts[i]
            text = segment_text(toks[i:b])[1]
            t = lookup(text)
            if t is None:
                left += 1
                out.append("".join(r for _, r, _ in toks[i:b]))
            else:
                done += 1
                body = "".join(r for _, r, _ in toks[i:b]).strip() if t == text else decode(t, toks[i:b])
                out.append(_raw_space(toks[i:b], "lead") + body + _raw_space(toks[i:b], "trail"))
            i = b
            continue
        kind, raw, name = toks[i]
        if kind == "tag" and not raw.startswith("</"):
            for attr, v in attr_segments(raw):
                t = lookup(v.strip())
                if t is None:
                    left += 1
                else:
                    done += 1
                    if t != v.strip():
                        raw = set_attr(raw, attr, t)
        out.append(raw)
        i += 1
    return "".join(out), done, left


def _raw_space(run, side: str) -> str:
    """The raw whitespace at one edge of a run, kept byte for byte."""
    raw = "".join(r for _, r, _ in run)
    if side == "lead":
        return raw[: len(raw) - len(raw.lstrip())]
    return raw[len(raw.rstrip()):]
