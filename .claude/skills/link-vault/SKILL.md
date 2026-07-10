---
name: link-vault
description: Turn a link dump (OneTab share URL / export, pasted URL list, or saved HTML) into a vault-ready bundle of categorized Markdown notes, delivered as a downloadable file. Use when the user wants their saved tabs or links organized into notes for a knowledge vault (Obsidian-style), or asks for a downloadable, categorized link collection.
---

# Link dump → vault-ready notes bundle

Convert a raw pile of links into a small set of Obsidian-compatible Markdown
notes — an index plus one note per category — and hand the result to the user
as a downloadable file. The notes are written so they can later be dropped
into a personal vault unchanged; until that vault is reachable, the
deliverable is the download itself.

## Step 1 — Get the raw links

Accept any of these inputs, in order of preference:

1. **OneTab share URL** (`https://www.one-tab.com/page/<id>`). Try fetching it
   once. one-tab.com blocks many non-browser clients; on 403 / connection
   refused, do NOT retry — ask for option 2 instead.
2. **Plain-text export** — OneTab *Export / Import URLs* format
   (`URL | Title` per line, blank lines between groups), or any pasted list of
   URLs (one per line, `|` title optional).
3. **Saved HTML** of a OneTab share page.

## Step 2 — Parse to JSON

```bash
python3 scripts/parse_onetab.py <url-or-file>      # or `-` for stdin
```

Emits `{"groups": [{"name", "links": [{"url", "title", "domain"}]}], "total_links": N}`.
On `no links found`, the input wasn't a recognized format — show the user the
accepted formats from Step 1 rather than guessing.

## Step 3 — Smart categorization (you, not a script)

Titles and domains carry the semantics; do this yourself, don't write a
keyword matcher.

- Derive 4–10 categories from the data itself. Don't force a fixed taxonomy.
- Every link lands in exactly one category; use `Unsorted` rather than
  mis-filing.
- **De-duplicate**: treat URLs as identical after stripping fragments and
  tracking params (`utm_*`, `fbclid`, `ref`). Keep the first occurrence, note
  duplicates in the index.
- For each link, write a one-line "why this is worth keeping" gloss inferred
  from title + URL. If a title is empty or opaque, infer from the URL path;
  only fetch the page when it's load-bearing.
- Give each category 2–4 lowercase tags (e.g. `ai/agents`, `reading/paper`).

## Step 4 — Build the notes bundle

Create the bundle in a scratchpad directory named after the source and date,
e.g. `link-vault-2026-07-10/`:

1. `_Index.md` — the dashboard:
   - YAML frontmatter: `created`, `source` (share URL or "pasted export"),
     `total_links`, `duplicates_removed`.
   - Summary table: category → count → tags.
   - A `[[wikilink]]` to each category note.
2. One `<Category>.md` per category:
   - YAML frontmatter: `tags`, `created`, `source`.
   - One-line category description, then bullets:
     `- [title](url) — gloss` (append `· from <original group>` when the
     source had multiple groups).

Keep filenames vault-safe: no `/ \ : # ^ [ ] |` in note names.

## Step 5 — Deliver as a downloadable file

- **Several notes** (the normal case): zip the bundle and send it —
  `python3 -m zipfile -c link-vault-<date>.zip link-vault-<date>/`, then
  `SendUserFile` with `display: "attach"`.
- **Single-note fallback**: if there are ≤2 categories or the user asks for
  "one file", concatenate index + categories into one Markdown file and send
  that instead.

Finish by summarizing inline in chat: categories with counts, duplicates
removed, and what's in the download.

## Step 6 — Vault destination (deferred)

The user's personal vault ("maestro") isn't reachable from this environment
yet. When it becomes available — as a GitHub repo, Dropbox folder, or local
path — replace Step 5's zip with writing the bundle's files directly into the
vault's inbox folder (same file contents, no zip), and confirm the paths
written. Until then, always deliver the download.
