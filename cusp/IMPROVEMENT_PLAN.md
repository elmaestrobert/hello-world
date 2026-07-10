# CUSP Actor Mapping — Critical Assessment & Improvement Plan

*Status: proposed · Covers dataset v6 (78 actors, 19 jurisdictions) + viewer + survey.*

---

## Part 1 — Honest assessment of the current mapping

### What it does well
- **Breadth-first skeleton is in place**: EU level, 16 member states, 2 associated states,
  pan-EU networks; all 7 actor types represented; every record coded against all 16
  taxonomy fields (a–p) plus an alignment note.
- **Two working instruments**: an exploration viewer (filter/cards/table/charts) and an
  A–E judgement survey — together they support both *mapping* and *expert elicitation*.
- **Consistent record shape** makes migration to a stricter model cheap.

### Critical weaknesses (in order of severity)

**W1 — No provenance (critical).** Zero of 78 records carry source URLs; the
`documents` field lists titles only. Each record was coded in a single pass from
1–2 web-search results by one coder, with no confidence rating, no coder ID, no
date-coded. As it stands the dataset is *not citable and not auditable* — the
single biggest blocker to serious use.

**W2 — Judgement fields have no rubric.** Activity (e), positioning (j),
orientation (g), explicitness (k) are analyst gut-calls. Symptom in the data:
the A–E activity scale is never used below D (A:19, B:33, C:22, D:4, **E:0**) —
classic selection/inflation bias, since we only added actors we found evidence
for. Without operational definitions, a second coder could not reproduce the
coding, and the project's own question ("how to judge this?") remains unanswered.

**W3 — Taxonomy fidelity gaps against the project's own spec.**
- (c) The spec asks *how fitting* each SD type is (A–E per type). The dataset
  stores a binary membership list instead. (The survey captures graded fit — the
  baseline doesn't, so survey results can't be compared to a baseline.)
- (d) "Time engaged in SD" is conflated with founding year: Siemens `1847`,
  Pasteur `1887`, KNAW `1808` are founding dates, not SD-engagement dates.
- (i) Core objective should map to the A–E report's objective list (p.66) —
  currently free text, so no cross-actor comparison is possible.
- (m) Tools use Hood's categories but the promised mapping to the Framework's
  strategic/operational/enabling instruments is absent.
- The promised **alignment check** is one unstructured sentence per actor, not a
  scored assessment against the Framework's dimensions.

**W4 — Coverage gaps.**
- **11 EU members absent**: BG, HR, CY, HU, LV, LT, LU, MT, RO, SK, SI.
- **Depth skew**: Germany 9 actors vs. 8 countries at 2 each.
- **Type skew**: Training = 1, Industry = 3, civil-society organisations = 0
  (category 19 of the project's own 21-item list).
- **Whole layers missing**: intergovernmental research infrastructures —
  *CERN, the canonical SD case, is not a record* — nor EMBL, ESA, ESO, ECMWF,
  ESS, EuroHPC; sub-national actors (Flanders' FWO/EWI, Bavaria, Catalonia)
  despite taxonomy point (a) naming regional/sub-national geography; universities
  as institutions (project question #13 unresolved); grant agencies patchy (no
  DFG, ANR, AEI records); diaspora networks for only 4 of 19 jurisdictions.
- **Project question #9 (where do EU agencies go?) is unresolved** — currently
  handled ad hoc (IIASA sits under Austria with a note).

**W5 — Data engineering debt.** Data lives in a JS file (hard to reuse outside
the apps), no schema, no validation, and the standalone HTML builds are manual
one-off commands — they *will* drift from `data.js` (the shipped
`survey-standalone.html` freezes whatever the dataset was at build time).

**W6 — App limitations.** No source links in the detail sheet (nothing to click
to verify); field (o) "networked with" is prose, so no network/graph view is
possible; no map view; no export from the viewer; survey responses can be
exported but not aggregated or compared against the baseline coding;
colour-only encodings hurt accessibility.

---

## Part 2 — Improvement plan

Ordering principle: **credibility before coverage before features.** More actors
added on today's foundations would just multiply un-auditable records.

### Phase 0 — Data model & build infrastructure
1. Migrate `data.js` → `actors.json` + a JSON Schema (`schema.json`).
   `data.js` becomes a *generated* artifact.
2. Extend the record model:
   - `sources[]` — `{url, title, accessed, supports}` (which field(s) it evidences)
   - `sdSinceYear` (taxonomy d) **separate from** `foundedYear`
   - `sdTypeFit` — `{s4d,d4s,SinD,DinS}` each A–E (replaces binary `sdType`)
   - `objectiveCodes[]` — enum drawn from the A–E report objective list (p.66)
   - `alignment` → structured: `{strategic, operational, enabling, conduct}`
     scores (0–3 each) + free-text note
   - `toolsInstruments` — map Hood tools → Framework strategic/operational/enabling
   - `relations[]` — typed edges `{to, type}` (funds / coordinates / member-of /
     hosts / advises) extracted from today's prose field (o)
   - record metadata: `coder`, `dateCoded`, `confidence` (H/M/L), `status`
     (draft → verified)
3. `build.js`: one command that validates every record against the schema,
   regenerates `data.js` and **both** standalone files. Failing validation
   fails the build.
   *Acceptance: standalones can no longer drift; invalid records can't ship.*

### Phase 1 — Rubrics, then recode
1. Write `RUBRICS.md` with operational definitions, e.g. activity (e):
   - **A** dedicated SD unit/staff *and* budgeted programmes *and* activity in the
     last 12 months; **B** two of those; **C** documented but intermittent;
     **D** declared intent, little visible activity; **E** latent/dormant.
   Analogous indicator lists for positioning (j), explicitness (k), orientation (g).
2. Recode all 78 records against the rubrics, recording per-field confidence.
   Expect the distribution to widen (E must become assignable).
   *Acceptance: every judgement traceable to a rubric criterion + source; a second
   coder could reproduce it.*

### Phase 2 — Verification & provenance pass
- Per record: ≥2 independent sources for factual fields, ≥1 for each judgement;
  verify institutional names against post-2024 reorganisations; flag or drop
  what can't be confirmed. Work in country batches (parallelisable).
  *Acceptance: 100% of records `status: verified`; zero URL-less records.*

### Phase 3 — Coverage completion
1. **Missing 11 EU members** — 1–3 anchor actors each (MFA + research
   ministry/funder + academy).
2. **New layer: intergovernmental organisations & research infrastructures** —
   CERN, EMBL/EMBO, ESA, ESO, ECMWF, ESS, ELIXIR, EuroHPC…
   Proposed convention resolving question #9: geography = `Intergovernmental`
   (own filter value), with a `hostCountry` field — an org neither disappears
   into its host nor double-counts under it. Same treatment for EU agencies.
3. **Sub-national actors** — FWO/EWI (Flanders), WBI (Wallonia), Bavaria, BW,
   Catalonia, Basque Country (taxonomy point a).
4. **Rebalance types** — Training (diplomatic academies, College of Europe, SD
   courses/summer schools); Industry (Leonardo, Ericsson, Nokia, Novo Nordisk
   Foundation); Civil society (EuroScience, Scholars at Risk Europe); grant
   agencies (DFG, ANR, AEI); diaspora networks for remaining countries.
5. **Universities (question #13)** — proposal: don't enumerate universities in the
   main map (unboundable); keep rectors' conferences as the sector voice + add
   2–3 flagship universities per *priority* state only, flagged `layer: sample`.
6. **Coverage matrix** — script rendering a country × 21-category grid (the
   project's preliminary list) so gaps are visible and tracked, not implicit.

### Phase 4 — Analytical & app layer
1. Detail sheet: clickable sources; per-SD-type fit shown as A–E chips.
2. **Network view** from `relations[]` (force-directed graph; answers taxonomy o
   properly).
3. **Alignment dashboard** — actors scored on the four Framework dimensions.
4. Country **compare mode** (side-by-side profiles) + map view.
5. **Survey round-trip**: import multiple respondents' JSON exports → consensus /
   disagreement per actor → diff against baseline coding → accepted judgements
   flow back into `actors.json` (the survey becomes the expert-elicitation
   instrument for Phases 1–2).
6. Accessibility: text labels alongside colour, keyboard navigation, focus states.

### Phase 5 — Governance & publication
- `CODING_MANUAL.md` (merges rubrics + conventions), per-record changelog,
  versioned dataset releases, `CITATION.cff`, optional GitHub Pages deployment
  of viewer + survey.

### Decisions needed from the project team
1. Confirm the **intergovernmental convention** for EU agencies/IOs (Phase 3.2).
2. Confirm the **universities sampling** approach (Phase 3.5).
3. Scope for think tanks (questions #10/#12): proposal — include only those with
   a demonstrable SD work-stream (e.g. EUISS, Bruegel on tech-sovereignty, IFRI).
4. Source of truth for the **A–E report objective list (p.66)** — needs the
   actual report text to build the `objectiveCodes` enum faithfully.

### Suggested sequencing
| Order | Phase | Why first |
|---|---|---|
| 1 | 0 + 1 (model, rubrics, recode) | Everything else inherits this quality floor |
| 2 | 2 (verification) | Makes the existing 78 records defensible |
| 3 | 3 (coverage) | Now new records enter at the higher standard |
| 4 | 4 (analytics/app) | Built on verified, structured data |
| 5 | 5 (governance) | Locks it in for collaborators |
