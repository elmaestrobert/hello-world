# CUSP — Mapping Science Diplomacy Actors in the EU & Priority Member States

Interactive mapping of **science diplomacy (SD) actors** across the EU level and
priority Member States, coded against a 16-field taxonomy (a–p) and checked for
**alignment with the EU Framework for Science Diplomacy**.

## Files
- `index.html` — interactive viewer (filter, search, cards / table / charts, per-actor detail). Open directly in a browser; no build step or network needed.
- `data.js` — the dataset. Each actor is one object coded against the taxonomy.
- `README.md` — method, taxonomy, sources, and the running country log.

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
  **France**, **Netherlands**. — *21 actors.*
- _Next:_ Spain, Italy, Austria, Poland, Sweden/Nordics, then deepen each country
  (universities, academies, research infrastructures, industry, diaspora networks).

## Key sources
- *A European Framework for Science Diplomacy* — EC expert report, Feb 2025.
- *Council Recommendation on an EU framework for science diplomacy* — COM(2026) 96 final (adopted 29 May 2026).
- European Commission, Science diplomacy pages (research-and-innovation.ec.europa.eu).
- S4D4C / EU Science Diplomacy Alliance state-of-the-art reports.
- National sources: Auswärtiges Amt & BMFTR (DE); MEAE & MESR (FR); Min. OCW / EZ, NWO, WRR (NL).

## Method & caveats
Coding is **indicative** and refined iteratively as more sources are reviewed.
Activity (e) and positioning (j) are analyst judgements pending the A–E report's
formal rubric. The dataset is designed to be extended one country at a time; add
records to `ACTORS` in `data.js` keeping the same field names.
