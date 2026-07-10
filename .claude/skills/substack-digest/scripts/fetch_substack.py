#!/usr/bin/env python3
"""Retrieve and normalize Substack posts. Python 3 stdlib only.

Commands
  list <publication> [--limit N]
      List recent posts (newest first). Tries the archive API, falls back to
      the RSS feed. <publication> is a name ("thezvi"), a substack URL, or a
      custom-domain URL ("https://www.astralcodexten.com").
  get <publication> <slug-or-post-url>
      Fetch one post's full content. Tries the post API, falls back to RSS.
  parse-feed <file|->
      Offline: parse a saved RSS feed (XML) into the same JSON as `list`,
      including full post bodies when the feed carries content:encoded.
  parse-html <file|->
      Offline: convert saved post HTML (or a pasted fragment) to markdown.

Output: JSON on stdout. Errors: JSON {"error": <class>, "detail": ...} on
stderr + nonzero exit. Error classes the caller should branch on:
  network_blocked   egress proxy refused the tunnel (policy denial) — do not
                    retry; use another retrieval route.
  http_403          the server refused us (bot blocking) — try another route.
  not_found         wrong publication/slug.
"""

import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


def die(err, detail=""):
    print(json.dumps({"error": err, "detail": detail}), file=sys.stderr)
    sys.exit(1)


def base_url(publication):
    p = publication.strip().rstrip("/")
    if not p:
        die("not_found", "empty publication")
    if "://" in p:
        u = urllib.parse.urlparse(p)
        return f"{u.scheme}://{u.netloc}"
    if "." in p:
        return f"https://{p}"
    return f"https://{p}.substack.com"


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            die("not_found", url)
        die(f"http_{e.code}", url)
    except (urllib.error.URLError, OSError) as e:
        msg = str(e)
        if "403" in msg or "Tunnel" in msg or "CONNECT" in msg:
            die("network_blocked",
                f"{url} — egress proxy denied the connection (session network "
                "policy). Do not retry; fall back to WebFetch/WebSearch or "
                "user-provided content.")
        die("network_error", f"{url} — {msg}")


# ---------------------------------------------------------------- HTML → md

class MarkdownConverter(HTMLParser):
    """Lossy but readable HTML→markdown for Substack post bodies."""

    SKIP = {"script", "style", "svg", "button", "form", "iframe", "audio", "video"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.href = None
        self.link_text = []
        self.skip_depth = 0
        self.pre = False
        self.quote = False
        self.list_stack = []  # 'ul' | 'ol' counters

    def _emit(self, text):
        tgt = self.link_text if self.href is not None else self.out
        tgt.append(text)

    def _block_break(self):
        self.out.append("\n\n")

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._block_break()
            self._emit("#" * int(tag[1]) + " ")
        elif tag == "p":
            self._block_break()
            if self.quote:
                self._emit("> ")
        elif tag == "br":
            self._emit("\n")
        elif tag == "a":
            self.href = a.get("href", "")
            self.link_text = []
        elif tag == "img":
            src, alt = a.get("src", ""), a.get("alt", "image")
            if src:
                self._emit(f"![{alt}]({src})")
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "blockquote":
            self._block_break()
            self.quote = True
        elif tag == "pre":
            self._block_break()
            self._emit("```\n")
            self.pre = True
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("ul", "ol"):
            self.list_stack.append(0 if tag == "ol" else -1)
        elif tag == "li":
            self._block_break() if not self.list_stack else self.out.append("\n")
            indent = "  " * max(len(self.list_stack) - 1, 0)
            if self.list_stack and self.list_stack[-1] >= 0:
                self.list_stack[-1] += 1
                self._emit(f"{indent}{self.list_stack[-1]}. ")
            else:
                self._emit(f"{indent}- ")
        elif tag == "hr":
            self._block_break()
            self._emit("---")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(self.skip_depth - 1, 0)
            return
        if self.skip_depth:
            return
        if tag == "a" and self.href is not None:
            text = "".join(self.link_text).strip() or self.href
            href, self.href = self.href, None
            if href and href != text:
                self.out.append(f"[{text}]({href})")
            else:
                self.out.append(text)
        elif tag in ("strong", "b"):
            self._emit("**")
        elif tag in ("em", "i"):
            self._emit("*")
        elif tag == "blockquote":
            self.quote = False
        elif tag == "pre":
            self._emit("\n```")
            self.pre = False
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("ul", "ol") and self.list_stack:
            self.list_stack.pop()

    def handle_data(self, data):
        if self.skip_depth:
            return
        if self.pre:
            self._emit(data)
        else:
            self._emit(re.sub(r"\s+", " ", data))

    def markdown(self):
        text = "".join(self.out)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def html_to_markdown(fragment):
    conv = MarkdownConverter()
    conv.feed(fragment)
    return conv.markdown()


# ---------------------------------------------------------------- RSS

def parse_feed_xml(xml_text):
    """Regex-based RSS item extraction (Substack feeds are flat RSS 2.0)."""
    posts = []
    for item in re.findall(r"<item>(.*?)</item>", xml_text, re.S):
        def tag(name):
            m = re.search(rf"<{name}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{name}>",
                          item, re.S)
            return html.unescape(m.group(1).strip()) if m else ""
        body = ""
        m = re.search(r"<content:encoded>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?"
                      r"</content:encoded>", item, re.S)
        if m:
            body = html_to_markdown(m.group(1))
        posts.append({
            "title": tag("title"),
            "url": tag("link"),
            "date": tag("pubDate"),
            "author": tag("dc:creator"),
            "subtitle": tag("description"),
            "slug": tag("link").rstrip("/").rsplit("/", 1)[-1] if tag("link") else "",
            "body_markdown": body,
        })
    return posts


# ---------------------------------------------------------------- commands

def cmd_list(publication, limit):
    base = base_url(publication)
    api = f"{base}/api/v1/archive?sort=new&offset=0&limit={limit}"
    try:
        raw = fetch(api)
        items = json.loads(raw)
        posts = [{
            "title": p.get("title", ""),
            "subtitle": p.get("subtitle", ""),
            "slug": p.get("slug", ""),
            "url": p.get("canonical_url", ""),
            "date": p.get("post_date", ""),
            "audience": p.get("audience", ""),   # "everyone" | "only_paid"
            "wordcount": p.get("wordcount"),
        } for p in items]
        return {"publication": base, "source": "archive_api", "posts": posts}
    except SystemExit:
        raise
    except Exception:
        pass  # fall through to RSS
    posts = parse_feed_xml(fetch(f"{base}/feed"))[:limit]
    return {"publication": base, "source": "rss", "posts": posts}


def cmd_get(publication, ref):
    base = base_url(publication)
    slug = ref.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
    try:
        p = json.loads(fetch(f"{base}/api/v1/posts/{slug}"))
        body_html = p.get("body_html") or ""
        return {
            "title": p.get("title", ""),
            "subtitle": p.get("subtitle", ""),
            "url": p.get("canonical_url", f"{base}/p/{slug}"),
            "date": p.get("post_date", ""),
            "audience": p.get("audience", ""),
            "paywalled_preview": bool(p.get("audience") == "only_paid"
                                      and p.get("should_show_paywall", True)),
            "body_markdown": html_to_markdown(body_html),
            "source": "post_api",
        }
    except SystemExit:
        raise
    except Exception:
        pass
    for post in parse_feed_xml(fetch(f"{base}/feed")):
        if post["slug"] == slug:
            post["source"] = "rss"
            return post
    die("not_found", f"slug '{slug}' not in API or feed of {base}")


def read_input(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def main(argv):
    if len(argv) < 2:
        die("usage", __doc__)
    cmd = argv[1]
    if cmd == "list" and len(argv) >= 3:
        limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else 12
        out = cmd_list(argv[2], limit)
    elif cmd == "get" and len(argv) >= 4:
        out = cmd_get(argv[2], argv[3])
    elif cmd == "parse-feed" and len(argv) >= 3:
        out = {"source": "saved_feed", "posts": parse_feed_xml(read_input(argv[2]))}
    elif cmd == "parse-html" and len(argv) >= 3:
        out = {"source": "saved_html",
               "body_markdown": html_to_markdown(read_input(argv[2]))}
    else:
        die("usage", __doc__)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv)
