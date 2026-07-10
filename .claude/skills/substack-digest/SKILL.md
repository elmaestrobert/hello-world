---
name: substack-digest
description: Retrieve Substack posts and understand them — produce structured, vault-ready reading notes (TL;DR, key claims, quotes, links, tags) plus a digest index, delivered as a downloadable file. Use when the user shares a Substack URL, names a newsletter, or asks to catch up on / summarize / digest Substack posts.
---

# Substack → understood, vault-ready notes

Two halves: **retrieve** posts robustly (network access varies wildly by
environment), then **understand** each post into a structured note a future
reader can act on without reopening the original.

## Step 1 — Scope

Establish: which publication(s), how many posts (default: last ~5 or "since
<date>"), and whether the user wants a per-post deep note or a compact
catch-up digest. A bare post URL means: that one post, deep note.

Publication references the tooling accepts: a name (`thezvi`), a
`*.substack.com` URL, or a custom domain (`https://www.astralcodexten.com`).

## Step 2 — Retrieve (ladder — stop at the first rung that works)

Run the bundled fetcher (stdlib only) first:

```bash
python3 scripts/fetch_substack.py list <publication> --limit 12   # recent posts
python3 scripts/fetch_substack.py get  <publication> <slug-or-url> # full post
```

It tries Substack's archive/post APIs, falls back to RSS, and normalizes to
JSON with `body_markdown`. Branch on its error classes:

1. **Success** → done. Note `audience: "only_paid"` posts — you likely have
   only a preview (see paywall rule below).
2. **`network_blocked`** (egress policy denial) → do NOT retry the script.
   Try `WebFetch` on the post URL; if that also 403s, the whole session has
   no web egress — go to rung 3.
3. **`http_403`** (Substack bot-blocking) or no egress at all →
   - `WebSearch` restricted to the publication's domain still gives titles,
     URLs, and snippets — enough for a headline-level digest. Label it as
     such; never pad snippets into fake summaries.
   - Ask the user for content: paste the post text, or save the feed/post
     page and provide the file — then parse offline:
     ```bash
     python3 scripts/fetch_substack.py parse-feed saved_feed.xml
     python3 scripts/fetch_substack.py parse-html saved_post.html
     ```
   - Mention the durable fix once: allow `substack.com` (and the custom
     domain, if any) in this environment's network policy.

**Paywall rule**: if a post is `only_paid` or the body ends abruptly, say so
in the note (`status: preview-only`) and summarize only what was retrieved.
Never reconstruct paywalled content from memory or search snippets.

## Step 3 — Understand (you, not a script)

Read the full `body_markdown` before writing anything. One note per post:

```markdown
---
title: "<post title>"
publication: "<name>"
author: "<author>"
date: <ISO date>
url: <canonical url>
tags: [<2-5 lowercase topic tags>]
status: full | preview-only | headline-only
---

**TL;DR** — 2-3 sentences: what the post argues and why it matters.

## Key claims
- Bulleted claims/arguments, each self-contained. Attribute clearly:
  the author's claim vs. something the author is quoting or disputing.

## Evidence & numbers
- Concrete figures, benchmarks, dates, named sources — the checkable stuff.

## Notable quotes
> Short verbatim quotes (1-3), only when the phrasing itself carries value.

## Links worth following
- [title/description](url) — why the author pointed there.

## Open questions / follow-ups
- What the post leaves unresolved; anything the user should verify or read next.
```

Judgment calls: summarize positions faithfully even when the author is being
sarcastic (common on Substack — don't quote sarcasm as a sincere claim);
long link-roundup posts (e.g. weekly AI digests) get their "Key claims"
organized by the post's own section headers.

## Step 4 — Digest index

When there's more than one post, add `_Digest.md`: frontmatter (`created`,
`publication(s)`, `posts`, `retrieval` route used), a table
(date → title → one-line takeaway → status), then 3-5 bullets of
cross-post themes — things that only become visible reading them together.

## Step 5 — Deliver as a downloadable file

Bundle in a scratchpad dir named `substack-digest-<pub>-<date>/`, zip it
(`python3 -m zipfile -c <name>.zip <dir>/`), and send with `SendUserFile`
(`display: "attach"`). Single post → send the one `.md` directly, no zip.
Summarize inline in chat: posts covered, retrieval route, anything
preview-only.

## Step 6 — Vault destination (deferred)

The user's personal vault ("maestro") isn't reachable yet. When it becomes
available, write the same files into the vault (e.g. `Sources/Substack/<pub>/`)
instead of zipping. Notes are already Obsidian-compatible.
