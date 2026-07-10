/* Phase 3 integration: converts agent-authored records (phase3-*.json) into
 * full v7 records and appends them to actors.json.
 * Run: node cusp/phase3-merge.js <scratchpad-dir>   — then node cusp/build.js
 * Derivations mirror migrate.js so coding stays consistent (see RUBRICS.md).
 */
const fs = require("fs");
const path = require("path");
const DIR = __dirname;
const SCRATCH = process.argv[2];
if (!SCRATCH) { console.error("usage: node phase3-merge.js <scratchpad-dir>"); process.exit(1); }

const db = JSON.parse(fs.readFileSync(path.join(DIR, "actors.json"), "utf8"));
const existing = new Set(db.actors.map(a => a.id));
const TODAY = new Date().toISOString().slice(0, 10);
const domain = u => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return u; } };

const ACT_SCORE = { A: 2, B: 2, C: 1, D: 0, E: 0 };
const EXP_SCORE = { Explicit: 2, Emerging: 1, Implicit: 0 };
const HOOD = ["Treasure", "Authority", "Nodality", "Organisation"];

function deriveFit(ordered) {
  const fit = { s4d: "E", d4s: "E", SinD: "E", DinS: "E" };
  (ordered || []).forEach((t, i) => { if (t in fit) fit[t] = i === 0 ? "A" : "B"; });
  return fit;
}
function deriveInstruments(tools) {
  const m = { Treasure: "enabling", Authority: "strategic", Nodality: "operational", Organisation: "operational" };
  const out = { strategic: [], operational: [], enabling: [] };
  tools.forEach(t => { if (m[t]) out[m[t]].push(t); else out.enabling.push(t); });
  return out;
}
function deriveAlignment(r) {
  return {
    strategic: Math.min(3, (EXP_SCORE[r.explicitness] ?? 0) + (r.positioning === "Primary" ? 1 : 0)),
    operational: Math.min(3, (ACT_SCORE[r.activity] ?? 0) + (r.tools.includes("Organisation") ? 1 : 0)),
    enabling: Math.min(3, (r.tools.includes("Treasure") ? 1 : 0) + (r.tools.includes("Nodality") ? 1 : 0) +
      (["Training", "NGO/Network", "Policy Advice"].includes(r.actorType) ? 1 : 0)),
    conduct: 1,
    note: r.alignmentNote || "—"
  };
}

const files = fs.readdirSync(SCRATCH).filter(f => /^phase3-.*\.json$/.test(f)).sort();
if (!files.length) { console.error("no phase3-*.json found"); process.exit(1); }

let added = 0, skipped = [];
for (const f of files) {
  let batch;
  try { batch = JSON.parse(fs.readFileSync(path.join(SCRATCH, f), "utf8")); }
  catch (e) { console.error(`SKIP ${f}: unparseable (${e.message})`); continue; }
  for (const r of batch.records || []) {
    if (existing.has(r.id)) { skipped.push(`${r.id} (duplicate)`); continue; }
    const doms = new Set((r.sources || []).map(s => domain(s.url)));
    const verified = (r.sources || []).length >= 2 && doms.size >= 2;
    if (!verified) skipped.push(`${r.id} (<2 source domains — added as draft)`);
    db.actors.push({
      id: r.id, name: r.name, country: r.country,
      ...(r.hostCountry ? { hostCountry: r.hostCountry } : {}),
      geography: r.geography, actorType: r.actorType,
      sdTypeFit: deriveFit(r.sdTypeOrdered),
      foundedYear: r.foundedYear ?? null, sdSinceYear: r.sdSinceYear ?? null,
      activity: r.activity, domains: r.domains || [], orientation: r.orientation,
      interestFocus: r.interestFocus, coreObjective: r.coreObjective,
      objectiveCodes: r.objectiveCodes || [], positioning: r.positioning,
      explicitness: r.explicitness, governance: r.governance || "—",
      tools: (r.tools || []).filter(t => HOOD.includes(t)),
      toolsInstruments: deriveInstruments(r.tools || []),
      sciFields: r.sciFields || [], networked: r.networked || "—",
      relations: r.relations || [],
      documents: r.documents || [],
      sources: (r.sources || []).map(s => ({ title: s.title, url: s.url, accessed: TODAY, supports: "record" })),
      alignment: deriveAlignment(r),
      coder: "CUSP Phase 3 (AI research agent, batch " + (batch.batch || f) + ")",
      dateCoded: TODAY, confidence: r.confidence || "M",
      status: verified ? "verified" : "draft",
      ...(verified ? { dateVerified: TODAY } : {})
    });
    existing.add(r.id); added++;
  }
}

db.version = "7.2.0"; db.generated = TODAY;
fs.writeFileSync(path.join(DIR, "actors.json"), JSON.stringify(db, null, 2));
console.log(`added ${added} records (total ${db.actors.length}) -> actors.json v7.2.0`);
if (skipped.length) console.log("notes:\n- " + skipped.join("\n- "));
