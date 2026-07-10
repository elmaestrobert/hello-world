/* Phase 2, step 2: applies the substantive free-text corrections from
 * verification-report.md to actors.json. Kept as audit trail.
 * Run once: node cusp/phase2-corrections.js
 */
const fs = require("fs");
const path = require("path");
const DIR = __dirname;
const db = JSON.parse(fs.readFileSync(path.join(DIR, "actors.json"), "utf8"));
const A = Object.fromEntries(db.actors.map(a => [a.id, a]));

/* -- names the merge left as sentences + verified renames -- */
A["es-cdti"].name = "CDTI Innovación — Centro para el Desarrollo Tecnológico y la Innovación";
A["fr-mesr"].name = "Ministry of Higher Education, Research & Space (MESRE)";
A["es-maec"].name = "Ministry of Foreign Affairs, European Union & Cooperation";

/* -- EU batch -- */
A["eu-dgrtd"].documents = ["A European Framework for Science Diplomacy (expert report, Feb 2025)",
  "Proposal COM(2026) 97 (27 Feb 2026)", "Council Recommendation on an EU framework for science diplomacy (adopted 29 May 2026)",
  "Global Approach to R&I (2021)"];
A["eu-erc"].networked = "ERC (est. 2007, FP7) and EIC (fully est. 2021 under Horizon Europe; pilot 2018-20) are distinct bodies under the Commission; global talent attraction (Choose Europe, relocation top-ups); links to national funders.";
A["eu-eeas"].networked += " Initiated EMFASDAN (EU MFAs Science Diplomacy & Advice Network, 2021); hosts a JRC-seconded S&T advisor.";
A["x-allea"].networked = "~60 academies from 40+ Council of Europe countries; runs SAPEA with the Commission's SAM; Code of Conduct for Research Integrity (2011, rev. 2017/2023).";
A["x-fmstan"].networked = "Convenes MFA science advisers (~50 countries); began Feb 2016 (Washington DC) and Vienna Dialogue at IIASA (Oct 2016); SPIDER/FMSTAN Vienna meeting Nov 2019; operates under the INGSA umbrella.";

/* -- Germany -- */
A["de-bmftr"].networked = "Co-initiated DWIH (2009) and sits on its Board of Trustees (network financed by the AA, coordinated by DAAD); bilateral S&T agreements; Horizon Europe; funds big-science (DESY, CERN contributions).";
A["de-bmftr"].alignment.note = "Strong — explicit SD engagement via the internationalisation strategy and DWIH co-initiator role (renamed BMFTR from BMBF, May 2025).";
A["de-daad"].geography = "National (Bonn) + ~60 offices/locations worldwide";
A["de-daad"].networked = "Intermediary for AA & BMFTR; ~60 offices/locations (15 regional offices + ~50 information centres); runs scholarship & university partnership programmes.";

/* -- Austria / Poland -- */
A["at-iiasa"].geography = "Sited in Laxenburg (AT); national member organisations worldwide";
A["at-iiasa"].governance = "International research institute (national member organisations, not treaty-based)";
A["pl-pan"].networked = "~68 institutes; foreign scientific stations (Paris, Rome, Vienna, Berlin, Kyiv) + PolSCA Brussels (since 2006); ALLEA/IAP member; bottom-up partnerships.";
A["pl-fnp"].foundedYear = 1990; A["pl-fnp"].sdSinceYear = 1990;
A["pl-fnp"].networked = "Runs START, TEAM, HOMING and the International Research Agendas (IRAP) programme; partners EU programmes; alumni network. (PASIFIC is PAN's programme, not FNP's — earlier coding corrected.)";
A["pl-fnp"].documents = ["FNP programme reports (START, TEAM, IRAP)"];

/* -- Italy / Spain -- */
A["it-maeci"].networked = "Scientific/space attaché network strengthened +60% (2022) and ~+5% (2023), ~45 attachés/experts abroad; attachés seconded under Art.168 DPR 18/1967 (+ Art.16 L.401/1990); links to CNR.";
A["it-cnr"].sdSinceYear = 2013;
A["it-cnr"].networked = "Supports scientific attachés abroad; ran DIPLOMAzia (agreed Dec 2013, delivered ~2014-15) and DIPLOMAzia2 (2016, courses 2017) — both concluded; bilateral agreements.";
A["it-cnr"].documents = ["DIPLOMAzia / DIPLOMAzia2 programme outputs (concluded)", "International relations reports"];
A["es-maec"].documents = ["Report on Science, Technology & Innovation Diplomacy (Informe, 2016 — recommended preparing a full strategy)"];
A["es-cdti"].networked = "External network incl. SOST office Brussels; ESA delegate role & Eureka coordination since 1985; partners FECYT on SD network. Renamed CDTI Innovación (~2023).";

/* -- France / Netherlands -- */
A["fr-meae"].documents.push("Ministerial science diplomacy strategy (Apr 2026, updated Jun 2026)");
A["fr-pasteur"].networked = "Pasteur Network (renamed 2021, ex-Institut Pasteur International Network): ~32 members in ~25 countries on 5 continents; WHO 'official relations' (2016); One-Health approach; outbreak response.";
A["fr-cnes"].documents = ["Space for Climate Observatory (SCO, launched 2019 — CNES provides secretariat)", "Bilateral space cooperation agreements"];
A["fr-ird"].foundedYear = 1943;

/* -- Nordics / small states -- */
A["no-mfa"].networked = "Chaired Arctic Council 11 May 2023 - 12 May 2025 (handover to Denmark); Svalbard research hub. NOTE: the Svalbard Research Office (opened 3 Mar 2026, Longyearbyen) and updated strategy are led by the Ministry of Education & Research and operated by RCN + Norwegian Polar Institute — not the MFA.";
A["ch-swissnex"].geography = "Six main hubs (Boston+NY, San Francisco, Shanghai, Bangalore, Brazil, Osaka) + 20+ science counsellors at embassies (assoc. state)";
A["cz-mzv"].networked = "Dedicated SD Unit in the Economic & Science Diplomacy Dept (confirmed); RDI-tasked diplomats at Czech missions (the '~90 missions' figure could not be independently verified); interministerial SD group at RVVI with TACR, GACR, CAS (unverified detail).";
A["fi-acadsci"].documents = ["'Towards an Enabling Science Diplomacy' (May 2021, co-produced via Sofi/VN TEAS; 10 recommendations)"];
A["fi-acadsci"].networked = "Co-produced (not sole-authored) the 2021 national SD report via its Sofi science-advice initiative; ALLEA member.";
A["ie-dfa"].documents = ["Global Ireland 2018-2025 (concluded; review published — mission network ~107)", "Global Ireland 2040 (successor, in development 2026)"];
A["gr-diaspora"].sdSinceYear = 2017; A["gr-diaspora"].foundedYear = 2017;
A["gr-diaspora"].activity = "D";
A["gr-diaspora"].networked = "Launched Aug 2017; implemented by the National Documentation Centre (EKT), responsible authority GSSPI; platform knowledgebridges.gr + Bridges Awards. Most dated activity evidence is pre-2026 — current intensity unconfirmed (hence activity D).";

/* bump + save */
db.version = "7.1.1";
fs.writeFileSync(path.join(DIR, "actors.json"), JSON.stringify(db, null, 2));
console.log("corrections applied -> actors.json v7.1.1");
