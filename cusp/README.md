# CUSP — Mapping Science Diplomacy Actors in the EU & Priority Member States

Interactive mapping of **science diplomacy (SD) actors** across the EU level and
priority Member States, coded against a 16-field taxonomy (a–p) and checked for
**alignment with the EU Framework for Science Diplomacy**.

## Files
- **`actors.json`** — the dataset, single source of truth (v7 model: per-record
  sources, graded SD-type fit, split founded/SD-engagement years, objective codes,
  structured alignment scores, typed relations, coder/confidence/status metadata).
- **`schema.json`** — required fields + enums; `build.js` validates against it.
- **`build.js`** — run `node cusp/build.js` after any data edit: validates every
  record (fails the build on bad data) and regenerates `data.js` + both standalones.
- `data.js` — **generated** app bundle (do not edit by hand).
- `index.html` — interactive viewer (filter, search, cards / table / charts, per-actor detail incl. sources and alignment scores).
- `survey.html` — **assessment tool**: pick a country *or* a partner type, then judge each matching actor one at a time on the A–E scale (significance, per-SD-type fit, activity, orientation, notes). Auto-saves to the browser; exports JSON/CSV.
- `*-standalone.html` — generated self-contained builds of the viewer and survey.
- `RUBRICS.md` — operational definitions for all judgement fields + the documented
  heuristics used for the initial v7 recode.
- `migrate.js` — audit trail of the v6 → v7 migration (override tables).
- `IMPROVEMENT_PLAN.md` — assessment of weaknesses and the phased plan.

## Assessment tool (`survey.html`)
A light, guided survey so a respondent can *judge* the mapped actors:
1. Choose a lens — **by country/geography** or **by diplomacy partner type** (actor type b).
2. Rate each actor on: overall **significance** (A–E), **fit of each SD type** s4d/d4s/SinD/DinS (A–E), **how active** (A–E), **orientation** (cooperative↔competitive), plus free notes — or mark "not familiar" to skip.
3. Review screen aggregates your scores and exports **JSON** or **CSV**. Answers persist per lens in `localStorage`, so multiple respondents/lenses can be collected and combined offline.

## How to use
Open `cusp/index.html`. Filter via the left rail (country, actor type, SD type,
domain, orientation, interest focus, positioning, activity), free-text search,
and toggle **Cards / Table / Charts**. Click any actor for the full a–p coding
plus its EU-Framework alignment note.

## Taxonomy (project coding scheme)
| Key | Field | Notes |
|---|---|---|
| a | Country / geography | incl. supranational, regional, sub-national |
| b | Type of actor | Diplomatic · Governmental/IO · Scientific/Research · NGO/Network · Training · Policy Advice · Industry (adapted from EU Framework p.30) |
| c | Type of SD | s4d (science *for* diplomacy) · d4s (diplomacy *for* science) · SinD (science *in* diplomacy) · DinS (diplomacy *in* science) |
| d | Years engaged | coded as `sinceYear` |
| e | How active | A (very high) → E (latent) |
| f | Thematic domain | climate, oceans, polar, space, digital, quantum, AI, health, food security, energy, biodiversity, archaeology, HSS, security/dual-use, etc. |
| g | Orientation | Cooperative · Mixed · Competitive (EU Framework framing) |
| h | Interest focus | National · Cross-border · Global (Gluckman) |
| i | Core objective | mapped to the A–E report objective list |
| j | Positioning | Primary / Secondary / Tertiary site of SD |
| k | Explicitness of SD self-identification | Explicit · Implicit · Emerging |
| l | Governance model | centralised / coordinated / fragmented etc. |
| m | Tools | treasure · authority · nodality · organisation (Hood); mapped to strategic/operational/enabling instruments |
| n | Fields of science prioritised | per A–E report |
| o | How networked with other actors/IOs | |
| p | SD-related documents produced | |
| + | **Alignment** | explicit note on fit with the EU SD Framework |

## Alignment check (per proposal)
Every record carries an `alignment` note assessing how the actor relates to the
EU Framework for Science Diplomacy's shared vision, instruments (strategic /
operational / enabling) and code of conduct — as promised in the proposal text.

## Coverage log
- **v1 (2026-06-10):** EU level (DG RTD, EEAS/Delegations, JRC, SAM/GCSA, ERC/EIC),
  pan-EU networks (EU Science Diplomacy Alliance/S4D4C, ALLEA), **Germany**,
  **France**, **Netherlands**.
- **v2 (2026-06-10):** added **Spain** (MAEC, FECYT, CDTI, CSIC), **Italy** (MAECI/
  Farnesina, CNR, MUR), **Austria** (BMEIA, OeAD, ZSI, IIASA), **Poland** (MSZ/
  Diplomatic Academy, PAN/PolSCA, FNP, KRASP) + FMSTAN network. — *36 actors, 8 jurisdictions.*
- **v3 (2026-06-10):** added **Sweden** (UD/innovation offices, STINT, VR/IntSam, IVA),
  **Belgium** (FPS Foreign Affairs, BELSPO), **Czechia** (MFA SD Unit, CAS),
  **Portugal** (FCT/goPORTUGAL, MNE/Camões). — *46 actors, 12 jurisdictions.*
- **v4 (2026-06-10):** added **Denmark** (ICDK, Tech Ambassador/TechPlomacy),
  **Finland** (UM + Academy, Finnish Academy of Science & Letters), **Ireland**
  (Research Ireland, DFA/Global Ireland), **Greece** (MFA, diaspora knowledge
  network). — *54 actors, 16 jurisdictions.*
- **v5 (2026-06-10):** added **Switzerland** (FDFA, GESDA, swissnex), **Norway**
  (MFA/Arctic, Polar Institute, RCN) — both Horizon-associated — and **Estonia**
  (MFA Digital & Cyber Diplomacy, Min. of Education & Research). — *62 actors, 19 jurisdictions.*
- **v6 (2026-06-10) — depth pass on priority states:** added diaspora networks
  (DE: GAIN; ES: RAICEX; IT: ISSNAF), rectors'/university associations (DE: HRK;
  FR: France Universités; NL: UNL; ES: CRUE; IT: CRUI), flagship research
  institutions & infrastructures (DE: Helmholtz/DESY; FR: Institut Pasteur Network;
  FR: CNES; IT: ASI), academies (NL: KNAW), and multinationals (DE: Siemens; NL:
  ASML; EU: Airbus). — *78 actors, 19 jurisdictions, all 7 actor types represented.*
- **v7 (2026-07-10) — Phase 0+1 of the improvement plan:** migrated to
  `actors.json` + schema + validating `build.js`; added per-record **sources**
  (97 URLs), split `foundedYear`/`sdSinceYear` (8 records honestly "not datable"),
  graded **sdTypeFit** (A–E per type), 12-code objective enum, structured 4-dimension
  **alignment scores** (documented heuristic), 153 typed **relations** edges,
  coder/confidence/status metadata; wrote `RUBRICS.md`; recoded activity per rubric
  (5 downgrades). All records `status: draft` pending Phase 2 verification.
- **v7.1.1 (2026-07-10) — Phase 2 verification pass:** all 78 records verified by
  7 parallel research agents against current (Jul 2026) official sources. Now
  **250 sources** (min 2 per record, all with ≥2 distinct domains); confidence
  72 H / 6 M; `status: verified` across the board. ~30 substantive corrections
  applied — highlights: Council Rec proposal is **COM(2026) 97** (not 96); EIC
  est. 2021 (not 2007); PASIFIC is **PAN's** programme (not FNP's); French
  research ministry renamed **MESRE** (Space added); CDTI renamed CDTI Innovación;
  DAAD ~60 offices (not 70+); MAECI attaché growth +60%+5% (not 70%); Svalbard
  Research Office led by Norway's Education Ministry (not MFA); IIASA membership
  is national member organisations (not intergovernmental); Greek diaspora
  network launched Aug 2017, activity downgraded to D. Full detail in
  `verification-report.md`; audit trail in `phase2-corrections.js`.
- **v7.2.0 (2026-07-10) — Phase 3 coverage:** +40 records (118 total, 117 verified).
  All 27 EU member states now covered + intergovernmental layer (CERN, EMBL, ESA,
  ESO, ESS, ECMWF, EuroHPC, EUI — `country: Intergovernmental` + `hostCountry`
  convention, resolving proposal question #9) + first sub-national actors (FWO,
  WBI, BayFOR, ICREA, Ikerbasque — taxonomy point a) + type rebalance (Vienna
  Diplomatic Academy & EUI/STG for Training; Scholars at Risk Europe; DFG;
  Leonardo & Nokia for Industry). First honest **E grade**: EuroScience
  (liquidated Jan 2024). One record kept draft: lt-lmt (single-domain sourcing).
  New records researched & sourced by parallel agents at the verified standard
  (≥2 independent domains).
- _Next (Phase 4):_ analytical layer — network graph from `relations[]`,
  alignment dashboard, country compare, survey aggregation round-trip.

> A self-contained build, `cusp-standalone.html` (data inlined), is regenerated each
> iteration for one-tap opening without the sibling `data.js`.

## Key sources
- *A European Framework for Science Diplomacy* — EC expert report, Feb 2025.
- *Council Recommendation on an EU framework for science diplomacy* — proposal COM(2026) 97 (27 Feb 2026); adopted by Council 29 May 2026.
- European Commission, Science diplomacy pages (research-and-innovation.ec.europa.eu).
- S4D4C / EU Science Diplomacy Alliance state-of-the-art reports.
- National sources: Auswärtiges Amt & BMFTR (DE); MEAE & MESR (FR); Min. OCW / EZ, NWO, WRR (NL).

## Method & caveats
Coding is **indicative** and refined iteratively as more sources are reviewed.
Activity (e) and positioning (j) are analyst judgements pending the A–E report's
formal rubric. The dataset is designed to be extended one country at a time; add
records to `ACTORS` in `data.js` keeping the same field names.
