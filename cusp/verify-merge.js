/* Phase 2 integration: merges verification-agent outputs (verify-*.json) into
 * actors.json. Run: node cusp/verify-merge.js <scratchpad-dir>
 *
 * Per record:
 *  - appends the agent's newSources (deduped by URL, marked supports:"verification")
 *  - adopts the agent's confidence
 *  - status -> "verified" iff verdict is confirm/revise AND the record now has
 *    sources from >= 2 distinct domains; otherwise stays "draft"
 *  - name corrections are applied; other corrections/concerns go to
 *    verification-report.md for human review (free text can't be auto-applied)
 */
const fs = require("fs");
const path = require("path");
const DIR = __dirname;
const SCRATCH = process.argv[2];
if (!SCRATCH) { console.error("usage: node verify-merge.js <scratchpad-dir>"); process.exit(1); }

const db = JSON.parse(fs.readFileSync(path.join(DIR, "actors.json"), "utf8"));
const byId = Object.fromEntries(db.actors.map(a => [a.id, a]));
const TODAY = new Date().toISOString().slice(0, 10);
const domain = u => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return u; } };

const files = fs.readdirSync(SCRATCH).filter(f => /^verify-.*\.json$/.test(f));
if (!files.length) { console.error("no verify-*.json files found in " + SCRATCH); process.exit(1); }

const report = [`# Phase 2 verification report (${TODAY})`, ""];
let stats = { seen: 0, verified: 0, draft: 0, nameFixes: 0, newSources: 0, unconfirmable: [] };

for (const f of files.sort()) {
  let batch;
  try { batch = JSON.parse(fs.readFileSync(path.join(SCRATCH, f), "utf8")); }
  catch (e) { console.error(`SKIP ${f}: unparseable (${e.message})`); report.push(`## ${f}\n**UNPARSEABLE — rerun this batch.**\n`); continue; }
  report.push(`## Batch: ${batch.batch} (${f})`, "");
  for (const r of batch.results || []) {
    const a = byId[r.id];
    if (!a) { report.push(`- ⚠️ unknown id \`${r.id}\``); continue; }
    stats.seen++;

    // sources
    const have = new Set(a.sources.map(s => s.url));
    for (const s of r.newSources || []) {
      if (!s.url || have.has(s.url)) continue;
      a.sources.push({ title: s.title || s.url, url: s.url, accessed: TODAY, supports: "verification" });
      have.add(s.url); stats.newSources++;
    }

    // name correction
    if (r.nameOk === false && r.nameCorrection) {
      report.push(`- ✏️ \`${r.id}\` name: "${a.name}" → "${r.nameCorrection}"`);
      a.name = r.nameCorrection; stats.nameFixes++;
    }

    // confidence + status
    if (["H", "M", "L"].includes(r.confidence)) a.confidence = r.confidence;
    const domains = new Set(a.sources.map(s => domain(s.url)));
    const ok = ["confirm", "revise"].includes(r.verdict) && domains.size >= 2;
    a.status = ok ? "verified" : "draft";
    a.dateVerified = ok ? TODAY : undefined;
    if (!ok) stats.draft++; else stats.verified++;
    if (r.verdict === "unconfirmable") stats.unconfirmable.push(r.id);

    for (const c of r.corrections || []) report.push(`- 📝 \`${r.id}\`: ${c}`);
    for (const c of r.concerns || []) report.push(`- ⚠️ \`${r.id}\` concern: ${c}`);
  }
  report.push("");
}

const untouched = db.actors.filter(a => a.status === "draft" && !stats.unconfirmable.includes(a.id))
  .map(a => a.id).filter(id => !files.length ? true : true);
report.push(`## Summary`, "",
  `- records processed: ${stats.seen} / ${db.actors.length}`,
  `- verified: ${stats.verified} · still draft: ${db.actors.filter(a => a.status === "draft").length}`,
  `- new sources added: ${stats.newSources} · name fixes: ${stats.nameFixes}`,
  `- unconfirmable: ${stats.unconfirmable.join(", ") || "none"}`);

db.version = db.version.replace(/^(\d+)\.(\d+)/, (m, a, b) => `${a}.${+b + 1}`);
db.generated = TODAY;
fs.writeFileSync(path.join(DIR, "actors.json"), JSON.stringify(db, null, 2));
fs.writeFileSync(path.join(DIR, "verification-report.md"), report.join("\n"));
console.log(`merged ${files.length} batches: ${stats.verified} verified, ${stats.newSources} sources added, ${stats.nameFixes} name fixes -> actors.json v${db.version} + verification-report.md`);
