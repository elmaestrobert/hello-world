/* One-off migration: data.js (v6) -> actors.json (v7 model).
 * Kept in the repo as an audit trail of how the initial recode was derived.
 * Derivation rules are documented in RUBRICS.md. Run: node cusp/migrate.js
 */
const fs = require("fs");
const path = require("path");
const DIR = __dirname;
const TODAY = "2026-07-10";

global.__c = {};
eval(fs.readFileSync(path.join(DIR, "data.js"), "utf8") + "; global.__c.A = ACTORS;");
const OLD = global.__c.A;

/* ---- Table 1: founding vs SD-engagement year (only where they differ or need nulling).
 * sdSinceYear: null = no datable self-engagement in SD (see RUBRICS.md). */
const YEARS = {
  "de-leopoldina": { founded: 1652, sdSince: 2008 },
  "de-siemens":    { founded: 1847, sdSince: null },
  "de-hrk":        { founded: 1949, sdSince: 2010 },
  "fr-cnrs":       { founded: 1939, sdSince: null },
  "fr-univ":       { founded: 1971, sdSince: null },
  "nl-knaw":       { founded: 1808, sdSince: 2018 },
  "nl-nwo":        { founded: 1950, sdSince: 2019 },
  "nl-asml":       { founded: 1984, sdSince: 2019 },
  "x-airbus":      { founded: 1970, sdSince: null },
  "es-csic":       { founded: 1939, sdSince: null },
  "es-crue":       { founded: 1994, sdSince: null },
  "it-cnr":        { founded: 1923, sdSince: 2015 },
  "it-crui":       { founded: 1963, sdSince: null },
  "pl-krasp":      { founded: 1997, sdSince: null },
  "se-iva":        { founded: 1919, sdSince: 2015 },
  "fi-acadsci":    { founded: 1908, sdSince: 2021 }
};

/* ---- Table 2: activity regrades against the RUBRICS.md scale (id -> new grade). */
const ACTIVITY = {
  "fr-cnrs": "B", "eu-erc": "B", "eu-jrc": "B", "de-helmholtz": "B",
  "fr-cnes": "B", "nl-asml": "C"
};

/* ---- Table 3: objective codes (provisional enum, see schema.json). */
const OBJ = {
  "eu-dgrtd":["VAL","SEC","GLB"], "eu-eeas":["SEC","INF","GOV"], "eu-jrc":["EVI","GLB"],
  "eu-sam-gcsa":["EVI"], "eu-erc":["TAL","ECO"], "x-s4d4c":["TRU","GLB","EVI"],
  "x-allea":["VAL","EVI"], "x-fmstan":["TRU","EVI"], "x-airbus":["ECO","SEC"],
  "de-aa":["INF","TRU","VAL"], "de-bmftr":["ECO","GLB","SEC"], "de-daad":["TAL","INF"],
  "de-avh":["TAL","TRU"], "de-leopoldina":["EVI","TRU"], "de-gain":["DIA","TAL"],
  "de-hrk":["VAL","SEC"], "de-helmholtz":["KNOW","GLB"], "de-siemens":["ECO","GOV"],
  "fr-meae":["INF","GLB","ECO"], "fr-mesr":["ECO","KNOW"], "fr-ird":["DEV","GLB"],
  "fr-cnrs":["KNOW","TAL"], "fr-pasteur":["GLB","DEV","TRU"], "fr-univ":["VAL"],
  "fr-cnes":["GOV","GLB","SEC"],
  "nl-owa":["ECO","KNOW"], "nl-ian":["ECO","SEC"], "nl-nwo":["KNOW","GLB"],
  "nl-wrr":["EVI"], "nl-knaw":["VAL","SEC","EVI"], "nl-unl":["VAL","SEC"], "nl-asml":["ECO","SEC"],
  "es-maec":["INF","TRU"], "es-fecyt":["DIA","TAL","INF"], "es-cdti":["ECO"],
  "es-csic":["KNOW","GLB"], "es-raicex":["DIA","TAL","EVI"], "es-crue":["VAL"],
  "it-maeci":["INF","ECO"], "it-cnr":["KNOW","EVI"], "it-mur":["ECO","KNOW"],
  "it-crui":["VAL"], "it-issnaf":["DIA","TAL"], "it-asi":["GOV","GLB"],
  "at-bmeia":["TRU","INF"], "at-oead":["TAL","DEV"], "at-zsi":["TRU","EVI"], "at-iiasa":["TRU","GLB","EVI"],
  "pl-msz":["INF","TRU"], "pl-pan":["KNOW","TRU"], "pl-fnp":["TAL"], "pl-krasp":["VAL"],
  "se-mfa":["ECO","INF"], "se-stint":["TAL","TRU"], "se-vr":["KNOW","GLB"], "se-iva":["EVI","ECO"],
  "be-fps":["GOV","SEC"], "be-belspo":["GOV","GLB","KNOW"],
  "cz-mzv":["ECO","TRU","INF"], "cz-cas":["KNOW","TRU"],
  "pt-fct":["DEV","TAL","GLB"], "pt-mne":["INF","DEV"],
  "dk-icdk":["ECO","TAL"], "dk-techamb":["GOV","SEC"],
  "fi-um":["GLB","DEV"], "fi-acadsci":["EVI","TRU"],
  "ie-research":["TAL","ECO","GLB"], "ie-dfa":["TRU","DEV"],
  "gr-mfa":["INF","TRU"], "gr-diaspora":["DIA","TAL"],
  "ch-fdfa":["GOV","TRU","GLB"], "ch-gesda":["GOV","GLB","EVI"], "ch-swissnex":["ECO","TAL"],
  "no-mfa":["GOV","SEC","GLB"], "no-polar":["EVI","GLB"], "no-rcn":["KNOW","GLB"],
  "ee-mfa":["SEC","GOV","INF"], "ee-mer":["KNOW","ECO"]
};

/* ---- Table 4: typed relations (edges for the future network view).
 * "to" is an internal id when the target is a record, else a free-text label. */
const REL = {
  "eu-dgrtd": [["coordinates","eu-jrc"],["partners","eu-eeas"],["informs","Member State ministries via ERAC"]],
  "eu-eeas": [["partners","eu-dgrtd"]],
  "eu-jrc": [["part-of","European Commission"],["advises","eu-dgrtd"]],
  "eu-sam-gcsa": [["advises","European Commission"],["partners","x-allea"]],
  "eu-erc": [["part-of","European Commission (Horizon Europe)"]],
  "x-s4d4c": [["informs","eu-dgrtd"],["convenes","EU SD community of practice"]],
  "x-allea": [["partners","eu-sam-gcsa"],["convenes","50+ national academies"]],
  "x-fmstan": [["convenes","MFA science advisers worldwide"],["partners","at-iiasa"]],
  "x-airbus": [["partners","fr-cnes"],["partners","European Space Agency"]],
  "de-aa": [["coordinates","de-daad"],["coordinates","de-avh"],["hosts","DWIH board chair"]],
  "de-bmftr": [["funds","de-helmholtz"],["partners","de-aa"]],
  "de-daad": [["joint-initiative-of","de-gain"],["funds","exchange & partnership programmes"]],
  "de-avh": [["joint-initiative-of","de-gain"],["convenes","Humboldtian alumni network"]],
  "de-leopoldina": [["member-of","x-allea"],["advises","German federal government"]],
  "de-gain": [["joint-initiative-of","de-avh"],["joint-initiative-of","de-daad"],["partners","de-hrk"]],
  "de-hrk": [["member-of","European University Association"],["partners","de-gain"]],
  "de-helmholtz": [["hosts","DESY / European XFEL / FAIR user communities"]],
  "de-siemens": [["partners","standards bodies & EU industrial policy fora"]],
  "fr-meae": [["coordinates","science counsellor/attaché network"],["partners","fr-mesr"]],
  "fr-mesr": [["steers","fr-cnrs"],["steers","fr-ird"],["steers","fr-cnes"]],
  "fr-ird": [["partners","Global South research institutions"],["partners","AFD"]],
  "fr-cnrs": [["hosts","International Research Labs (IRL)"],["member-of","CERN & big-science consortia"]],
  "fr-pasteur": [["convenes","Pasteur Network (33 institutes)"],["partners","World Health Organization"]],
  "fr-univ": [["member-of","European University Association"],["partners","fr-mesr"]],
  "fr-cnes": [["member-of","European Space Agency"],["partners","NASA / ISRO bilaterals"]],
  "nl-owa": [["part-of","Ministry of Education, Culture & Science"],["partners","nl-nwo"]],
  "nl-ian": [["part-of","Ministry of Economic Affairs"],["partners","RVO & top sectors"]],
  "nl-nwo": [["partners","nl-owa"],["funds","international programmes"]],
  "nl-wrr": [["advises","Dutch government"],["member-of","INGSA"]],
  "nl-knaw": [["member-of","x-allea"],["advises","Dutch government on knowledge security"]],
  "nl-unl": [["partners","National Contact Point Knowledge Security"],["member-of","European University Association"]],
  "nl-asml": [["partners","NL/EU/US export-control dialogues"]],
  "es-maec": [["partners","es-fecyt"],["coordinates","embassy science coordinators"]],
  "es-fecyt": [["partners","es-maec"],["partners","es-raicex"],["coordinates","Science Diplomacy Network"]],
  "es-cdti": [["partners","es-fecyt"],["member-of","ESA / Eureka"]],
  "es-csic": [["hosts","international joint units"],["partners","Antarctic & ocean campaigns"]],
  "es-raicex": [["partners","es-fecyt"],["convenes","Spanish researchers in 18 countries"]],
  "es-crue": [["member-of","European University Association"],["partners","Ibero-American university networks"]],
  "it-maeci": [["coordinates","scientific/space attaché network"],["partners","it-cnr"]],
  "it-cnr": [["partners","it-maeci"],["member-of","x-allea"]],
  "it-mur": [["steers","it-cnr"],["steers","it-asi"]],
  "it-crui": [["member-of","European University Association"]],
  "it-issnaf": [["partners","it-maeci"],["convenes","Italian researchers in North America"]],
  "it-asi": [["member-of","European Space Agency"],["partners","NASA Artemis"]],
  "at-bmeia": [["partners","at-iiasa"],["partners","at-oead"],["convenes","FMSTAN/SPIDER Vienna meetings"]],
  "at-oead": [["coordinates","bilateral S&T (WTZ) programmes"]],
  "at-zsi": [["coordinates","x-s4d4c"],["informs","eu-dgrtd"]],
  "at-iiasa": [["convenes","member academies of 20+ countries"],["partners","x-fmstan"]],
  "pl-msz": [["partners","pl-pan"],["hosts","Diplomatic Academy"]],
  "pl-pan": [["member-of","x-allea"],["hosts","PolSCA Brussels + foreign stations"]],
  "pl-fnp": [["funds","PASIFIC fellowships (MSCA cofund)"]],
  "pl-krasp": [["member-of","European University Association"]],
  "se-mfa": [["coordinates","7 innovation & research offices"],["partners","se-vr"]],
  "se-stint": [["funds","international HE & research partnerships"]],
  "se-vr": [["convenes","IntSam funder coordination"],["member-of","CERN / ESS / ESO consortia"]],
  "se-iva": [["convenes","industry-policy fora"]],
  "be-fps": [["partners","be-belspo"],["hosts","EU & NATO institutions in Brussels"]],
  "be-belspo": [["member-of","European Space Agency"],["hosts","Princess Elisabeth Antarctica"]],
  "cz-mzv": [["coordinates","cz-cas"],["coordinates","interministerial SD steering group"],["hosts","SD Unit + ~90 mission attachés"]],
  "cz-cas": [["member-of","x-allea"],["partners","cz-mzv"]],
  "pt-fct": [["partners","pt-mne"],["coordinates","goPORTUGAL partnerships"]],
  "pt-mne": [["partners","pt-fct"],["convenes","CPLP/lusophone science ties"]],
  "dk-icdk": [["joint-initiative-of","Danish MFA + Ministry of HE & Science"],["hosts","7 innovation centres"]],
  "dk-techamb": [["part-of","Danish MFA"],["convenes","dialogue with global tech industry"]],
  "fi-um": [["funds","development research with Research Council of Finland"]],
  "fi-acadsci": [["member-of","x-allea"],["advises","Finnish government (SD report)"]],
  "ie-research": [["partners","ie-dfa"],["funds","SDG Challenge"]],
  "ie-dfa": [["partners","ie-research"],["convenes","British-Irish Council shared evidence"]],
  "gr-mfa": [["convenes","EU SD symposium (2026)"],["partners","gr-diaspora"]],
  "gr-diaspora": [["convenes","Greek scientific diaspora"],["partners","gr-mfa"]],
  "ch-fdfa": [["funds","ch-gesda"],["coordinates","ch-swissnex"],["member-of","CERN host-state role"]],
  "ch-gesda": [["partners","ch-fdfa"],["convenes","International Geneva science-diplomacy fora"]],
  "ch-swissnex": [["part-of","EAER/SERI + FDFA"],["hosts","global swissnex hubs"]],
  "no-mfa": [["coordinates","no-polar"],["coordinates","no-rcn"],["convenes","Arctic Council chairship 2023-25"]],
  "no-polar": [["partners","no-mfa"],["hosts","Ny-Alesund & Troll stations"]],
  "no-rcn": [["funds","polar & High North research"],["partners","no-polar"]],
  "ee-mfa": [["partners","ee-mer"],["hosts","Digital & Cyber Diplomacy Dept"]],
  "ee-mer": [["partners","ee-mfa"],["coordinates","RDIE Strategy 2021-2035"]]
};

/* ---- Table 5: sources actually consulted for the v1-v6 coding (accessed this session).
 * Phase 2 adds independent verification sources; status stays "draft" until then. */
const SRC = {
  "eu-dgrtd":[["EC - Science diplomacy","https://research-and-innovation.ec.europa.eu/strategy/strategy-research-and-innovation/europe-world/international-cooperation/science-diplomacy_en"],["Council Recommendation COM(2026) 96 final","https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A52026DC0096"]],
  "eu-eeas":[["EC news - EU strengthens science diplomacy & research security (2026)","https://research-and-innovation.ec.europa.eu/news/all-research-and-innovation-news/eu-strengthens-science-diplomacy-and-research-security-support-global-research-cooperation-2026-02-27_en"]],
  "eu-jrc":[["EC Knowledge for Policy platform","https://knowledge4policy.ec.europa.eu/"]],
  "eu-sam-gcsa":[["EC Scientific Advice Mechanism","https://scientificadvice.eu/"]],
  "eu-erc":[["ERC - mission & work programmes","https://erc.europa.eu/"]],
  "x-s4d4c":[["S4D4C project site","https://www.s4d4c.eu/"],["ZSI project record","https://www.zsi.at/en/object/project/4711"]],
  "x-allea":[["ALLEA","https://allea.org/"]],
  "x-fmstan":[["S4D4C - FMSTAN/SPIDER Vienna workshop","https://www.s4d4c.eu/opening-science-opening-diplomacy-the-s4d4c-science-diplomacy-workshop-in-vienna/"]],
  "x-airbus":[["Airbus corporate site","https://www.airbus.com/"]],
  "de-aa":[["Federal Foreign Office - Science diplomacy","https://www.auswaertiges-amt.de/en/aussenpolitik/themen/science-universities/2209874"]],
  "de-bmftr":[["BMFTR - Science Diplomacy","https://www.bmftr.bund.de/EN/Research/InternationalAffairs/ScienceDiplomacy/sciencediplomacy_node.html"]],
  "de-daad":[["DAAD-run GAIN page","https://www.daad.org/en/about-us/network/german-academic-international-network-gain/"]],
  "de-avh":[["AvH - GAIN press release","https://www.humboldt-foundation.de/en/explore/newsroom/gain-2019-das-groesste-netzwerktreffen-deutscher-wissenschaftlerinnen-und-wissenschaftler-startet-in-den-usa"]],
  "de-leopoldina":[["S4D4C - Germany case","https://www.s4d4c.eu/topic/5-2-3-germany/"]],
  "de-gain":[["GAIN (DAAD New York)","https://www.daad.org/en/about-us/network/german-academic-international-network-gain/"]],
  "de-hrk":[["HRK - at a glance","https://www.hrk.de/hrk-at-a-glance/"],["HRK - Alliance of Science Organisations","https://www.hrk.de/hrk-at-a-glance/alliance-of-science-organisations-in-germany/"]],
  "de-helmholtz":[["Helmholtz Association","https://www.helmholtz.de/en/"]],
  "de-siemens":[["Siemens corporate site","https://www.siemens.com/"]],
  "fr-meae":[["MEAE - Scientific & academic diplomacy","https://www.diplomatie.gouv.fr/en/french-foreign-policy/scientific-and-academic-diplomacy/"],["Science Diplomacy for France (2013)","https://www.diplomatie.gouv.fr/IMG/pdf/science-diplomacy-for-france-2013_cle83c9d2.pdf"]],
  "fr-mesr":[["S4D4C - France case","https://www.s4d4c.eu/topic/5-2-4-france/"]],
  "fr-ird":[["France's Science Diplomacy (Science & Diplomacy, 2020)","https://www.sciencediplomacy.org/article/2020/frances-science-diplomacy"]],
  "fr-cnrs":[["CNRS international","https://international.cnrs.fr/"]],
  "fr-pasteur":[["Institut Pasteur International Network - organisation","https://www.pasteur.fr/en/home/institut-pasteur/institut-pasteur-throughout-world/institut-pasteur-international-network/organization-institut-pasteur-international-network"],["Pasteur Network missions","https://www.pasteur.fr/en/institut-pasteur/institut-pasteur-throughout-world/institut-pasteur-international-network/institut-pasteur-international-network-missions"]],
  "fr-univ":[["France Universites","https://franceuniversites.fr/"]],
  "fr-cnes":[["CNES","https://cnes.fr/en"]],
  "nl-owa":[["Government.nl - Network of Education & Science Attaches","https://www.government.nl/topics/education-and-internationalisation/network-of-education-and-science-attaches"]],
  "nl-ian":[["Netherlands Innovation Network - about","https://netherlandsinnovation.nl/about-us/"]],
  "nl-nwo":[["NWO - Science diplomacy","https://www.nwo.nl/en/science-diplomacy"]],
  "nl-wrr":[["WRR (English)","https://english.wrr.nl/"],["INGSA profile","https://ingsa.org/resources/netherlands-wrr/"]],
  "nl-knaw":[["KNAW - Knowledge Security position paper","https://www.knaw.nl/en/publications/knowledge-security-academy-position-paper"],["KNAW on Knowledge Security Act","https://www.knaw.nl/en/news/royal-netherlands-academy-arts-and-sciences-knaw-warns-against-proposed-knowledge-security-act"]],
  "nl-unl":[["Universities of the Netherlands","https://www.universiteitenvannederland.nl/en/"]],
  "nl-asml":[["NL Times - knowledge security debate","https://nltimes.nl/2023/10/10/dutch-science-academy-critical-cabinets-new-anti-espionage-law"]],
  "es-maec":[["Spanish Science Diplomacy (Science & Diplomacy, 2017)","https://www.sciencediplomacy.org/article/2017/spanish-science-diplomacy-global-and-collaborative-bottom-approach"]],
  "es-fecyt":[["Spanish Science Diplomacy (Science & Diplomacy, 2017)","https://www.sciencediplomacy.org/article/2017/spanish-science-diplomacy-global-and-collaborative-bottom-approach"],["S4D4C - Spain case","https://www.s4d4c.eu/topic/5-2-6-spain-2/"]],
  "es-cdti":[["CDTI","https://www.cdti.es/"]],
  "es-csic":[["CSIC","https://www.csic.es/en"]],
  "es-raicex":[["RAICEX: A Successful Story of the Spanish Scientific Diaspora (PMC)","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9326310/"]],
  "es-crue":[["CRUE","https://www.crue.org/"]],
  "it-maeci":[["MAECI - Science Diplomacy","https://www.esteri.it/en/diplomazia-culturale-e-diplomazia-scientifica/cooperscientificatecnologica/"],["MAECI - S&T experts and attaches","https://www.esteri.it/en/diplomazia-culturale-e-diplomazia-scientifica/cooperscientificatecnologica/reteaddettiscientificitecnologici/"]],
  "it-cnr":[["CNR - International relations","https://www.cnr.it/en/international-relations"]],
  "it-mur":[["ResearchItaly - SD's increasing role","https://researchitaly.mur.gov.it/en/science-diplomacy-an-increasing-role-in-italys-growth/"]],
  "it-crui":[["CRUI","https://www.crui.it/"]],
  "it-issnaf":[["Development of Scientific Diasporas: Italian case (2025)","https://www.researchgate.net/publication/395877977_Development_of_Scientific_Diasporas_as_a_Tool_of_Science_Diplomacy_Italian_Case"]],
  "it-asi":[["ASI","https://www.asi.it/en/"]],
  "at-bmeia":[["BMEIA - Scientific & Technical Cooperation","https://www.bmeia.gv.at/en/european-foreign-policy/international-cultural-policy/scientific-and-technical-cooperation"]],
  "at-oead":[["OeAD - S&T Cooperation","https://oead.at/en/cooperations/international-he-cooperations/scientific-technological-cooperation-st-cooperation"]],
  "at-zsi":[["ZSI - S4D4C project","https://www.zsi.at/en/object/project/4711"]],
  "at-iiasa":[["IIASA","https://iiasa.ac.at/"],["S4D4C - FMSTAN/SPIDER Vienna (IIASA co-org)","https://www.s4d4c.eu/opening-science-opening-diplomacy-the-s4d4c-science-diplomacy-workshop-in-vienna/"]],
  "pl-msz":[["Polish MFA - Diplomatic Academy","https://www.gov.pl/web/diplomacy/diplomatic-academy"]],
  "pl-pan":[["Science diplomacy of Poland (HSS Communications, 2020)","https://www.nature.com/articles/s41599-020-00555-2"],["PAN","https://pan.pl/en/"]],
  "pl-fnp":[["FNP / PASIFIC","https://pasific.pan.pl/polish-academy-of-sciences/"]],
  "pl-krasp":[["Science diplomacy of Poland (HSS Communications, 2020)","https://www.nature.com/articles/s41599-020-00555-2"]],
  "se-mfa":[["Sweden Abroad - Science & Innovation","https://www.swedenabroad.se/en/about-sweden-non-swedish-citizens/india/business-and-trade-with-sweden/science-and-technology/"]],
  "se-stint":[["STINT - Science Diplomacy in and for Sweden (2022)","https://www.stint.se/wp-content/uploads/2022/02/STINT_Science_Diplomacy.pdf"]],
  "se-vr":[["Swedish Research Council - international work","https://www.vr.se/english/mandates/international-work.html"]],
  "se-iva":[["IVA","https://www.iva.se/en/"]],
  "be-fps":[["FPS Foreign Affairs - international space policy","https://diplomatie.belgium.be/en/policy/policy-areas/highlighted/belgium-and-international-space-policy"]],
  "be-belspo":[["BELSPO","https://www.belspo.be/"],["ESA - BELSPO profile","https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Belgian_Science_Policy_Office_BELSPO"]],
  "cz-mzv":[["Czech MFA - Science Diplomacy","https://mzv.gov.cz/jnp/en/foreign_relations/science_and_technology/index.html"],["Czech MFA - S&T in the Czech Republic","https://mzv.gov.cz/jnp/en/foreign_relations/science_and_technology/sience_and_technology_in_the_czech.html"]],
  "cz-cas":[["CAS - mission","https://www.avcr.cz/en/about-us/mission-of-the-cas/"]],
  "pt-fct":[["FCT - goPORTUGAL","https://www.fct.pt/en/internacional/goportugal"],["SD in the EU: the Portuguese case (HSS Communications, 2024)","https://www.nature.com/articles/s41599-024-04102-1"]],
  "pt-mne":[["SD in the EU: the Portuguese case (HSS Communications, 2024)","https://www.nature.com/articles/s41599-024-04102-1"]],
  "dk-icdk":[["ICDK - about","https://icdk.dk/about-us"],["UFM - Innovation Centres & attaches","https://ufm.dk/en/research-and-innovation/international-cooperation/global-cooperation/innovation-centres-and-attaches"]],
  "dk-techamb":[["Office of Denmark's Tech Ambassador","https://techamb.um.dk/"]],
  "fi-um":[["Finnish MFA - research projects & development research","https://um.fi/support-for-development-research"]],
  "fi-acadsci":[["Finnish Academy of Science & Letters - SD report","https://acadsci.fi/en/news/finnish-academy-of-science-and-letters-produces-a-science-diplomacy-report/"]],
  "ie-research":[["SFI/Research Ireland - international","https://www.sfi.ie/funding/international/"],["SFI Strategy","https://www.sfi.ie/strategy/"]],
  "ie-dfa":[["Global Ireland strategies","https://www.ireland.ie/en/global-ireland-strategies/"]],
  "gr-mfa":[["Hellenic MFA - Symposium on Greece in EU Science Diplomacy (2026)","https://www.mfa.gr/en/symposium-on-the-role-of-greece-in-eu-science-diplomacy-11-06-2026/"]],
  "gr-diaspora":[["Establishing a Greek Diaspora Knowledge Network (2020)","https://www.researchgate.net/publication/341218967_Establishing_a_Greek_Diaspora_Knowledge_Network_through_Knowledge_and_Partnership_Bridges"]],
  "ch-fdfa":[["FDFA - Science in foreign policy","https://www.eda.admin.ch/en/science-foreign-policy"],["Swiss science diplomacy (Science & Public Policy, 2025)","https://academic.oup.com/spp/article/52/2/298/7932446"]],
  "ch-gesda":[["GESDA - how it all started","https://old.gesda.global/how-it-all-started/"],["FDFA on GESDA","https://www.eda.admin.ch/eda/en/fdfa/fdfa/aktuell/newsuebersicht/2023/10/gesda.html"]],
  "ch-swissnex":[["swissnex annual report - next-gen science diplomats","https://annualreport.swissnex.org/projects/project-meet-the-next-generation-of-science-diplomats-ObVTW/"]],
  "no-mfa":[["Norwegian Government Arctic Policy","https://www.regjeringen.no/en/documents/arctic_policy/id2830120/"],["High North News - Svalbard research office & strategy","https://en.highnorthnews.com/science/updated-strategy-and-new-research-office/1105806"]],
  "no-polar":[["Arctic SD of Norway: Svalbard case (Polar Science, 2022)","https://www.sciencedirect.com/science/article/pii/S1873965222001840"]],
  "no-rcn":[["High North News - Svalbard research office & strategy","https://en.highnorthnews.com/science/updated-strategy-and-new-research-office/1105806"]],
  "ee-mfa":[["Estonian MFA - Digital & Cyber Diplomacy","https://vm.ee/en/activity/digital-and-cyber-diplomacy/overview-cyber-diplomacy"]],
  "ee-mer":[["EURAXESS - Estonia in focus (RDIE strategy)","https://euraxess.ec.europa.eu/worldwide/north-america/news/euraxess-country-focus-estonia"]]
};

/* ---- Table 6: conduct-dimension overrides for the alignment heuristic. */
const CONDUCT = {
  "x-allea": 3, "nl-knaw": 3, "eu-dgrtd": 3, "de-leopoldina": 2, "de-hrk": 2,
  "de-avh": 2, "nl-unl": 2, "ch-gesda": 2, "fi-acadsci": 2, "x-s4d4c": 2, "at-zsi": 2
};

/* ---- Table 7: confidence overrides (default M). */
const CONF = {
  "de-siemens": "L", "x-airbus": "L", "se-iva": "L", "fr-univ": "L", "es-crue": "L",
  "it-crui": "L", "pl-krasp": "L", "gr-mfa": "L", "be-fps": "L", "fi-um": "L"
};

/* ---- Derivations (documented in RUBRICS.md) ---- */
const ACT_SCORE = { A: 2, B: 2, C: 1, D: 0, E: 0 };
const EXP_SCORE = { Explicit: 2, Emerging: 1, Implicit: 0 };

function deriveFit(old) {
  const fit = { s4d: "E", d4s: "E", SinD: "E", DinS: "E" };
  old.sdType.forEach((t, i) => { fit[t] = i === 0 ? "A" : "B"; });
  return fit;
}
function deriveAlignment(a, act) {
  const strategic = Math.min(3, EXP_SCORE[a.explicitness] + (a.positioning === "Primary" ? 1 : 0));
  const operational = Math.min(3, ACT_SCORE[act] + (a.tools.includes("Organisation") ? 1 : 0));
  const enabling = Math.min(3, (a.tools.includes("Treasure") ? 1 : 0) + (a.tools.includes("Nodality") ? 1 : 0) +
    (["Training", "NGO/Network", "Policy Advice"].includes(a.actorType) ? 1 : 0));
  const conduct = CONDUCT[a.id] ?? 1;
  return { strategic, operational, enabling, conduct };
}
const HOOD = ["Treasure", "Authority", "Nodality", "Organisation"];
function deriveInstruments(tools) {
  const m = { Treasure: "enabling", Authority: "strategic", Nodality: "operational", Organisation: "operational" };
  const out = { strategic: [], operational: [], enabling: [] };
  tools.forEach(t => { if (m[t]) out[m[t]].push(t); else out.enabling.push(t); });
  return out;
}

/* ---- Assemble ---- */
const missing = [];
["YEARS","ACTIVITY","OBJ","REL","SRC","CONDUCT","CONF"].forEach(n => {
  Object.keys({ YEARS, ACTIVITY, OBJ, REL, SRC, CONDUCT, CONF }[n]).forEach(id => {
    if (!OLD.find(a => a.id === id)) missing.push(`${n}:${id}`);
  });
});
if (missing.length) { console.error("Override ids not in dataset:", missing.join(", ")); process.exit(1); }

const actors = OLD.map(a => {
  const y = YEARS[a.id] || {};
  const act = ACTIVITY[a.id] || a.activity;
  return {
    id: a.id, name: a.name, country: a.country, geography: a.geography, actorType: a.actorType,
    sdTypeFit: deriveFit(a),
    foundedYear: y.founded ?? a.sinceYear,
    sdSinceYear: "sdSince" in y ? y.sdSince : a.sinceYear,
    activity: act,
    domains: a.domains, orientation: a.orientation, interestFocus: a.interestFocus,
    coreObjective: a.coreObjective,
    objectiveCodes: OBJ[a.id] || [],
    positioning: a.positioning, explicitness: a.explicitness, governance: a.governance,
    tools: a.tools.filter(t => HOOD.includes(t)), toolsInstruments: deriveInstruments(a.tools),
    sciFields: a.sciFields, networked: a.networked,
    relations: (REL[a.id] || []).map(([type, to]) => ({ type, to })),
    documents: a.documents,
    sources: (SRC[a.id] || []).map(([title, url]) => ({ title, url, accessed: TODAY, supports: "record" })),
    alignment: { ...deriveAlignment(a, act), note: a.alignment },
    coder: "CUSP initial coding (AI-assisted, single-coder)",
    dateCoded: TODAY, confidence: CONF[a.id] || "M", status: "draft"
  };
});

const noObj = actors.filter(a => !a.objectiveCodes.length).map(a => a.id);
const noSrc = actors.filter(a => !a.sources.length).map(a => a.id);
if (noObj.length) console.warn("WARN no objectiveCodes:", noObj.join(", "));
if (noSrc.length) console.warn("WARN no sources:", noSrc.join(", "));

fs.writeFileSync(path.join(DIR, "actors.json"),
  JSON.stringify({ version: "7.0.0", generated: TODAY, actors }, null, 2));
console.log(`actors.json written: ${actors.length} records, ${noSrc.length} without sources, ${noObj.length} without objectives`);
