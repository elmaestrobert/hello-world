#!/usr/bin/env python3
"""Parse OneTab tab lists into structured JSON.

Accepts any of the three formats OneTab produces:
  1. A shared page URL (https://www.one-tab.com/page/<id>) -- fetched over HTTP.
  2. A saved HTML file of a shared page.
  3. The plain-text "Export URLs" format: one "URL | Title" per line,
     blank lines separating tab groups.

Output (stdout): JSON of the form
  {"groups": [{"name": "Group 1", "links": [{"url": ..., "title": ..., "domain": ...}]}]}

Usage:
  parse_onetab.py https://www.one-tab.com/page/XXXX
  parse_onetab.py exported.txt
  parse_onetab.py page.html
  cat exported.txt | parse_onetab.py -
"""

import html
import json
import re
import sys
import urllib.parse
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def domain_of(url: str) -> str:
    netloc = urllib.parse.urlparse(url).netloc.lower()
    return netloc[4:] if netloc.startswith("www.") else netloc


def parse_text_export(text: str) -> list:
    """Parse OneTab's plain-text export: 'URL | Title' lines, blank line = new group."""
    groups, current = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            if current:
                groups.append(current)
                current = []
            continue
        if "|" in line:
            url, title = line.split("|", 1)
            url, title = url.strip(), title.strip()
        else:
            url, title = line, ""
        if url.startswith(("http://", "https://")):
            current.append({"url": url, "title": title, "domain": domain_of(url)})
    if current:
        groups.append(current)
    return groups


def parse_shared_html(markup: str) -> list:
    """Parse a OneTab shared-page HTML document.

    Shared pages render each tab group as a block of anchor tags; group
    boundaries appear as headings/dividers. We take a tolerant approach:
    grab anchors in order and start a new group whenever a group marker
    (heading or 'tabGroup' container) appears between them.
    """
    boundary = re.compile(
        r"<(?:h[1-6][^>]*|div[^>]*class=\"[^\"]*tabGroup[^\"]*\")>", re.I
    )
    anchor = re.compile(r"<a\s[^>]*href=\"(https?://[^\"]+)\"[^>]*>(.*?)</a>", re.I | re.S)
    tag = re.compile(r"<[^>]+>")

    groups, current = [], []
    pos = 0
    events = sorted(
        [(m.start(), "boundary", None) for m in boundary.finditer(markup)]
        + [(m.start(), "link", m) for m in anchor.finditer(markup)]
    )
    for _, kind, m in events:
        if kind == "boundary":
            if current:
                groups.append(current)
                current = []
        else:
            url = html.unescape(m.group(1))
            if "one-tab.com" in domain_of(url):
                continue  # skip OneTab's own chrome/footer links
            title = html.unescape(tag.sub("", m.group(2))).strip()
            current.append({"url": url, "title": title, "domain": domain_of(url)})
    if current:
        groups.append(current)
    return groups


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    src = sys.argv[1]

    if src == "-":
        raw = sys.stdin.read()
    elif src.startswith(("http://", "https://")):
        raw = fetch(src)
    else:
        with open(src, encoding="utf-8", errors="replace") as f:
            raw = f.read()

    looks_like_html = "<a " in raw.lower() or "<html" in raw.lower()
    groups = parse_shared_html(raw) if looks_like_html else parse_text_export(raw)

    out = {
        "groups": [
            {"name": f"Group {i + 1}", "links": g} for i, g in enumerate(groups)
        ],
        "total_links": sum(len(g) for g in groups),
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    print()
    if out["total_links"] == 0:
        print("warning: no links found in input", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
