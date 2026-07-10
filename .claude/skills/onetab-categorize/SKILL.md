---
name: onetab-categorize
description: Turn a OneTab tab list (share URL, exported text, or saved HTML) into a categorized, mapped link collection. Use when the user shares a one-tab.com link, pastes a OneTab "Export URLs" dump, or asks to organize/categorize their saved tabs.
---

# OneTab → Categorized Link Map

Convert a raw OneTab tab list into (a) semantic categories and (b) a mapping
document the user can act on.

## Step 1 — Get the raw list

Accept any of these inputs, in order of preference:

1. **OneTab share URL** (`https://www.one-tab.com/page/<id>`). Try fetching it
   directly. Note: one-tab.com blocks many non-browser clients and some
   sandboxed network policies; if the fetch fails (403 / connection refused),
   do NOT keep retrying — fall back to asking the user for option 2.
2. **Plain-text export** — in OneTab click *Export / Import URLs* and paste the
   result. Format: `URL | Title` per line, blank lines between tab groups.
3. **Saved HTML** of the share page (browser "Save page as").

## Step 2 — Parse to JSON

Run the bundled parser (no dependencies, Python 3 stdlib only):

```bash
python3 scripts/parse_onetab.py <url-or-file>      # or `-` for stdin
```

It emits `{"groups": [{"name", "links": [{"url", "title", "domain"}]}], "total_links": N}`.
If it warns `no links found`, the input wasn't a recognized OneTab format —
show the user the expected formats from Step 1 instead of guessing.

## Step 3 — Categorize

You (Claude) do the categorization — do not write a keyword-matching script
for this; titles and domains carry the semantics.

- Derive 4–10 categories from the data itself (e.g. "ML papers", "Home
  improvement", "Job hunt", "News — read later"). Don't force a fixed taxonomy.
- Every link lands in exactly one category; use a final "Unsorted / unclear"
  category rather than mis-filing.
- Preserve each link's title, URL, and original OneTab group so the mapping is
  reversible.
- If a title is empty or opaque (e.g. a bare ID), infer from the URL path; only
  fetch the page if it's load-bearing for the user's goal.

## Step 4 — Emit the mapping

Produce two artifacts (in the directory the user is working in, or scratchpad
if this is exploratory):

1. `onetab-categorized.md` — human-readable report:
   - One `##` section per category with a one-line description.
   - Bullet list of `[title](url)` — note the original group when there were
     several (`_from Group 3_`).
   - A summary table at the top: category → count.
2. `onetab-mapping.json` — machine-readable mapping:

```json
{
  "source": "<share url or 'pasted export'>",
  "categories": [
    {"name": "...", "description": "...",
     "links": [{"url": "...", "title": "...", "domain": "...", "original_group": "Group 1"}]}
  ]
}
```

Finish by telling the user the category breakdown (name + count) inline in
chat, and offer next actions: de-duplicate, drop dead links, or re-import into
OneTab (the text-export format from Step 1 round-trips: emit `URL | Title`
lines grouped by category, blank line between categories).

## Example

Input (text export):

```
https://arxiv.org/abs/2005.14165 | Language Models are Few-Shot Learners
https://react.dev/learn | Quick Start – React

https://www.allrecipes.com/recipe/20144/banana-banana-bread/ | Banana Bread
```

Output categories: **AI/ML research** (arxiv), **Web development** (react.dev),
**Cooking** (allrecipes) — with the mapping JSON linking each back to Group 1
or Group 2.
