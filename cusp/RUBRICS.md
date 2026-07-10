# CUSP Coding Rubrics (v1)

Operational definitions for every judgement field, so that a second coder can
reproduce the coding and so the A–E scales mean the same thing across records.
Applied in the v7 recode (see `migrate.js` for the exact derivations and
per-record override tables — that file is the audit trail).

## e · Activity (A–E)
Indicators: (i) a dedicated SD/international unit or named staff; (ii) budgeted
programmes or instruments; (iii) visible activity in the last 12 months
(events, postings, publications, agreements).

| Grade | Definition |
|---|---|
| A | All three indicators present |
| B | Two indicators present |
| C | Documented SD activity, but intermittent or peripheral to the actor's mission |
| D | Declared intent or occasional participation; little independent activity |
| E | Latent/dormant: named in SD contexts but no observable activity |

> Note: the current dataset contains no E — expected selection bias (actors were
> found *through* their activity). E exists so that Phase 3 additions and future
> downgrades are expressible; its absence should be reported, not hidden.

## c · SD-type fit (A–E per type: s4d, d4s, SinD, DinS)
A = the type is the actor's primary mode; B = a substantial secondary mode;
C = present but marginal; D = plausible only; E = absent.
**Initial derivation (v7):** first self-claimed type → A, further claimed
types → B, unclaimed → E. This is a *mechanical seed*, confidence M — the
survey tool collects graded expert judgements that should replace it.

## d · SD engagement year (`sdSinceYear`) vs `foundedYear`
`sdSinceYear` = first identifiable SD engagement (strategy document, dedicated
unit, named programme, or purpose-built international mission). For
purpose-built internationalisation bodies (DAAD, IIASA, ICDK, swissnex…) it
equals the founding year. Where no engagement is datable (e.g. Siemens,
Airbus), `sdSinceYear` is **null** — displayed as "not datable", never guessed.

## j · Positioning (Primary / Secondary / Tertiary)
Primary = SD (or an SD instrument) is a core, stated function.
Secondary = SD is a recognised side-function of a broader mandate.
Tertiary = the actor matters to SD outcomes without an SD function of its own.

## k · Explicitness (Explicit / Emerging / Implicit)
Explicit = uses the term "science diplomacy" (or a direct national equivalent)
about itself in official materials. Emerging = beginning to (events, drafts).
Implicit = does SD-relevant work without the label.

## g · Orientation (Cooperative / Mixed / Competitive)
Cooperative = openness, partnership and global-goods framing dominates.
Competitive = national advantage, talent capture, tech-sovereignty framing
dominates. Mixed = both framings load-bearing in official materials.

## Alignment with the EU SD Framework (0–3 × four dimensions)
Dimensions follow the Framework's instrument categories: **strategic**
(vision/mandate), **operational** (delivery capacity), **enabling**
(funding/networks/training), **conduct** (values, integrity, research security).

**Initial heuristic (v7, transparent and reproducible):**
- strategic = explicitness score (Explicit 2 / Emerging 1 / Implicit 0) + 1 if positioning is Primary (cap 3)
- operational = activity score (A,B → 2 / C → 1 / D,E → 0) + 1 if tools include Organisation (cap 3)
- enabling = +1 Treasure, +1 Nodality, +1 if actor type is Training, NGO/Network or Policy Advice (cap 3)
- conduct = 1 by default; hand-raised where values/integrity work is core
  (e.g. ALLEA 3, KNAW 3, DG RTD 3 — see `CONDUCT` table in `migrate.js`)

These are **placeholders with a documented formula**, not judgements — Phase 2
replaces them with evidence-based scores per record. The UI labels them as such.

## m · Tools → instruments mapping
Hood categories kept as source coding; mapped to Framework instrument layers:
Authority → strategic; Nodality, Organisation → operational; Treasure → enabling.
("Training" appearing in legacy tool lists is normalised into enabling.)

## i · Objective codes
12-code provisional enum (`schema.json`) reconstructed from the SD literature.
**Must be remapped once the A–E report's objective list (p.66) is available** —
flagged as a project decision in `IMPROVEMENT_PLAN.md`.

## Record metadata
`confidence`: H = multiple independent sources; M = single good source;
L = inference from thin sourcing. `status`: `draft` until the Phase 2
verification pass; only then `verified`.
