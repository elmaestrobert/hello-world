/* CUSP — Mapping Science Diplomacy Actors in the EU & Priority Member States
 * Dataset (v1). Each record is coded against the project taxonomy (a–p) and
 * checked for alignment with the EU Framework for Science Diplomacy (2025 expert
 * report; Council Recommendation COM(2026) 96 final, adopted 29 May 2026).
 *
 * Taxonomy keys:
 *  a geography        b actorType        c sdType[]        d sinceYear
 *  e activity (A–E)   f domains[]        g orientation     h interestFocus
 *  i coreObjective    j positioning      k explicitness    l governance
 *  m tools[]          n sciFields[]      o networked       p documents[]
 *  + alignment (note on fit with EU SD Framework)
 *
 * sdType vocabulary: s4d (science for diplomacy), d4s (diplomacy for science),
 *   SinD (science in diplomacy), DinS (diplomacy in science).
 * activity scale: A=very high, B=high, C=moderate, D=emerging, E=latent.
 */

const TAXONOMY = {
  actorType: ["Diplomatic","Governmental/IO","Scientific/Research","NGO/Network","Training","Policy Advice","Industry"],
  sdType: ["s4d","d4s","SinD","DinS"],
  orientation: ["Cooperative","Mixed","Competitive"],
  interestFocus: ["National","Cross-border","Global"],
  positioning: ["Primary","Secondary","Tertiary"],
  explicitness: ["Explicit","Implicit","Emerging"],
  activity: ["A","B","C","D","E"],
  domains: ["Climate","Oceans","Polar","Space","Digital","Quantum","AI","Health","Food security","Energy","Biodiversity","Archaeology","HSS","Security/Dual-use","Migration","Water","General S&T"]
};

const ACTORS = [
  /* ===================== EU LEVEL ===================== */
  {
    id:"eu-dgrtd", name:"European Commission — DG Research & Innovation (DG RTD)",
    country:"EU", geography:"Supranational (Brussels)", actorType:"Governmental/IO",
    sdType:["s4d","d4s","SinD"], sinceYear:2014, activity:"A",
    domains:["General S&T","Climate","Health","Digital","Security/Dual-use"],
    orientation:"Mixed", interestFocus:"Cross-border", coreObjective:"Promote EU values & strategic interests through open, secure international S&T cooperation",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised (Commission-led, comitology)",
    tools:["Authority","Treasure","Organisation","Nodality"],
    sciFields:["All fields","Engineering","Life sciences","Climate science","ICT"],
    networked:"Owns the EU SD Framework; coordinates EEAS, JRC, Member States via ERAC/strategic fora; runs Horizon Europe international cooperation.",
    documents:["A European Framework for Science Diplomacy (2025)","COM(2026) 96 final — Council Recommendation","Global Approach to R&I (2021)"],
    alignment:"Author/owner of the Framework — full alignment by definition; sets the shared vision, narrative and code of conduct."
  },
  {
    id:"eu-eeas", name:"European External Action Service (EEAS) & EU Delegations",
    country:"EU", geography:"Supranational + global network of Delegations", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2011, activity:"B",
    domains:["General S&T","Security/Dual-use","Digital","Climate","Space"],
    orientation:"Mixed", interestFocus:"Global", coreObjective:"Embed S&T in EU foreign & security policy; leverage research for geopolitical objectives",
    positioning:"Secondary", explicitness:"Emerging", governance:"Centralised (HR/VP-led)",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Partners DG RTD on Framework delivery; some Delegations host science/tech counsellors; links to Member State embassies.",
    documents:["EU Strategic Compass (2022)","Joint communications on tech sovereignty"],
    alignment:"Identified in the Framework as a key operational arm; alignment growing as SD attaché/counsellor function develops."
  },
  {
    id:"eu-jrc", name:"Joint Research Centre (JRC)",
    country:"EU", geography:"Supranational (Ispra, Seville, Geel, Karlsruhe, Petten)", actorType:"Scientific/Research",
    sdType:["SinD","s4d"], sinceYear:1957, activity:"A",
    domains:["General S&T","Climate","Health","Food security","Security/Dual-use","Digital"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Provide independent scientific evidence to underpin EU policy & external action",
    positioning:"Secondary", explicitness:"Explicit", governance:"Centralised (Commission in-house science)",
    tools:["Nodality","Organisation","Authority"],
    sciFields:["Nuclear","Environmental","Data science","Economics","Materials"],
    networked:"Science-for-policy backbone; supports Competence Centre on Science Diplomacy concepts; partners with national labs & IAEA.",
    documents:["Science for policy reports","Knowledge for Policy platform outputs"],
    alignment:"Strong — exemplifies 'science in diplomacy' evidence function the Framework promotes."
  },
  {
    id:"eu-sam-gcsa", name:"Group of Chief Scientific Advisors / Scientific Advice Mechanism (SAM)",
    country:"EU", geography:"Supranational (Brussels)", actorType:"Policy Advice",
    sdType:["SinD"], sinceYear:2015, activity:"B",
    domains:["General S&T","Health","Climate","Digital"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Independent scientific advice to the College of Commissioners",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Centralised advisory",
    tools:["Nodality","Authority"],
    sciFields:["All fields"],
    networked:"Works with SAPEA (academies) & national academies; feeds evidence into SD-relevant dossiers.",
    documents:["SAM scientific opinions","SAPEA evidence reviews"],
    alignment:"Supports the evidence-into-policy pillar; not primarily an SD body but enabling."
  },
  {
    id:"eu-erc", name:"European Research Council (ERC) & European Innovation Council (EIC)",
    country:"EU", geography:"Supranational (Brussels)", actorType:"Governmental/IO",
    sdType:["d4s"], sinceYear:2007, activity:"A",
    domains:["General S&T","Quantum","AI","Health"],
    orientation:"Competitive", interestFocus:"Global", coreObjective:"Fund frontier research; attract & retain global talent (diplomacy for science)",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Centralised executive agency",
    tools:["Treasure","Nodality"],
    sciFields:["All fields"],
    networked:"Global talent magnet; mobility shapes EU's S&T standing; links to national funders.",
    documents:["ERC Work Programmes","Talent & mobility statistics"],
    alignment:"Embodies 'diplomacy for science' — using EU convening power & funds to enable science."
  },

  /* ===================== GERMANY ===================== */
  {
    id:"de-aa", name:"Federal Foreign Office (Auswärtiges Amt) — Science & Academic Relations",
    country:"Germany", geography:"National (Berlin) + global missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2009, activity:"A",
    domains:["General S&T","Climate","Health","Security/Dual-use","HSS"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Use science & academic exchange to build trust and project soft power",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised within federal structure",
    tools:["Authority","Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Chairs DWIH Board of Trustees; deploys science counsellors; funds intermediary organisations (DAAD, AvH, Goethe).",
    documents:["Foreign Cultural & Education Policy reports","Research & Academic Relations Initiative"],
    alignment:"High — long-standing explicit SD posture; model for the Framework's 'science for diplomacy'."
  },
  {
    id:"de-bmftr", name:"Federal Ministry of Research, Technology & Space (BMFTR)",
    country:"Germany", geography:"National (Berlin/Bonn)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:2014, activity:"A",
    domains:["General S&T","Space","Quantum","Climate","Health"],
    orientation:"Mixed", interestFocus:"National", coreObjective:"Steer international research cooperation & innovation policy",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised (federal competence)",
    tools:["Treasure","Authority","Organisation"],
    sciFields:["Engineering","Physics","Life sciences","Space"],
    networked:"Co-runs DWIH; bilateral S&T agreements; partners EU on Horizon; funds big-science (DESY, CERN contributions).",
    documents:["Internationalisation Strategy","China Strategy for research"],
    alignment:"Strong — explicit SD framing ('interface of science, international politics, diplomacy')."
  },
  {
    id:"de-daad", name:"German Academic Exchange Service (DAAD)",
    country:"Germany", geography:"National (Bonn) + 70+ offices worldwide", actorType:"NGO/Network",
    sdType:["s4d","d4s"], sinceYear:1925, activity:"A",
    domains:["HSS","General S&T","Health","Climate"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Promote academic exchange, mobility & internationalisation as soft power",
    positioning:"Secondary", explicitness:"Implicit", governance:"Self-governing membership org (publicly funded)",
    tools:["Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Intermediary for AA & BMFTR; runs scholarship & university partnership programmes; lektorat network.",
    documents:["DAAD Strategy 2025","Academic freedom monitoring reports"],
    alignment:"Aligned as a key intermediary/network the Framework relies on for talent & trust-building."
  },
  {
    id:"de-avh", name:"Alexander von Humboldt Foundation",
    country:"Germany", geography:"National (Bonn) + global alumni network", actorType:"NGO/Network",
    sdType:["d4s","s4d"], sinceYear:1953, activity:"B",
    domains:["General S&T","HSS","Climate"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Build a lifelong global network of top researchers (research diplomacy via fellowships)",
    positioning:"Secondary", explicitness:"Implicit", governance:"Foundation (publicly funded)",
    tools:["Treasure","Nodality"],
    sciFields:["All fields"],
    networked:"~30,000 Humboldtians in 140 countries; Philipp Schwartz Initiative for at-risk scholars.",
    documents:["Annual reports","Philipp Schwartz Initiative reports"],
    alignment:"Aligned — exemplary 'diplomacy for science' talent diplomacy instrument."
  },
  {
    id:"de-leopoldina", name:"Leopoldina — German National Academy of Sciences",
    country:"Germany", geography:"National (Halle)", actorType:"Policy Advice",
    sdType:["SinD","s4d"], sinceYear:2008, activity:"B",
    domains:["Health","Climate","General S&T","HSS"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Represent German science abroad & advise government on science-based policy",
    positioning:"Secondary", explicitness:"Explicit", governance:"Self-governing academy",
    tools:["Nodality","Authority"],
    sciFields:["All fields"],
    networked:"G-Science (G7/G20) academies statements; ALLEA & IAP member; advises federal government.",
    documents:["G-Science statements","Ad hoc policy statements"],
    alignment:"Aligned — science-academy track-II diplomacy explicitly recognised in the Framework."
  },

  /* ===================== FRANCE ===================== */
  {
    id:"fr-meae", name:"Ministry for Europe & Foreign Affairs (MEAE) — Scientific & Academic Diplomacy",
    country:"France", geography:"National (Paris) + global network", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2013, activity:"A",
    domains:["General S&T","Climate","Oceans","Health","Space","Digital"],
    orientation:"Mixed", interestFocus:"Global", coreObjective:"Project French scientific excellence & influence; link science community to foreign policy",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised (étatist)",
    tools:["Authority","Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Ambassador-delegate for S,T&I; dense network of scientific counsellors/attachés; annual strategy meeting.",
    documents:["Science Diplomacy for France (2013)","Annual scientific cooperation guidelines"],
    alignment:"High — one of the most explicit national SD doctrines in the EU; influences the Framework."
  },
  {
    id:"fr-mesr", name:"Ministry of Higher Education & Research (MESR)",
    country:"France", geography:"National (Paris)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:2013, activity:"A",
    domains:["General S&T","Space","Climate","Health","Quantum"],
    orientation:"Mixed", interestFocus:"National", coreObjective:"Develop & conduct national research policy incl. international dimension",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised",
    tools:["Treasure","Authority","Organisation"],
    sciFields:["Physics","Space","Life sciences","Mathematics"],
    networked:"Steers CNRS, CNES, IRD; co-leads SD with MEAE; bilateral programmes (PHC Hubert Curien).",
    documents:["National Research Strategy","Loi de programmation de la recherche"],
    alignment:"Aligned — co-pilot of French SD; supports EU Framework's research-policy integration."
  },
  {
    id:"fr-ird", name:"French National Research Institute for Sustainable Development (IRD)",
    country:"France", geography:"National (Marseille) + Global South network", actorType:"Scientific/Research",
    sdType:["s4d","d4s"], sinceYear:1944, activity:"B",
    domains:["Climate","Health","Biodiversity","Food security","Oceans"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Equitable research partnerships with the Global South (development diplomacy)",
    positioning:"Secondary", explicitness:"Explicit", governance:"Public research establishment",
    tools:["Treasure","Organisation","Nodality"],
    sciFields:["Environmental","Health","Agronomy","Social sciences"],
    networked:"Representations across Africa, LatAm, Asia; partners AFD, AU; SDG-oriented co-construction.",
    documents:["Science for sustainable development reports","IRD objectives & means contract"],
    alignment:"Aligned — embodies the Framework's emphasis on equitable global partnerships."
  },
  {
    id:"fr-cnrs", name:"CNRS — National Centre for Scientific Research",
    country:"France", geography:"National (Paris) + international labs (IRL/IRP)", actorType:"Scientific/Research",
    sdType:["d4s","DinS"], sinceYear:1939, activity:"A",
    domains:["General S&T","Quantum","Climate","Space","HSS"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Conduct & internationalise French basic research",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Public research establishment (large, fragmented internally)",
    tools:["Organisation","Nodality","Treasure"],
    sciFields:["All fields"],
    networked:"International Research Labs worldwide; CERN/big-science membership; bilateral partnerships.",
    documents:["CNRS international strategy","Objectives contract with state"],
    alignment:"Aligned as a research actor whose mobility & partnerships deliver 'diplomacy in science'."
  },

  /* ===================== NETHERLANDS ===================== */
  {
    id:"nl-owa", name:"Network of Education & Science Attachés (OWA) — Min. of Education, Culture & Science",
    country:"Netherlands", geography:"National (The Hague) + 12 missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2000, activity:"B",
    domains:["General S&T","Digital","Health","Climate"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Strengthen international representation of the Dutch knowledge sector",
    positioning:"Primary", explicitness:"Explicit", governance:"Coordinated (consensus 'polder')",
    tools:["Nodality","Organisation","Authority"],
    sciFields:["All fields"],
    networked:"Sits under OCW Directorate of International Policy; links to NWO, universities, KNAW.",
    documents:["International knowledge policy letters to parliament"],
    alignment:"Aligned — attaché network is exactly the operational instrument the Framework promotes."
  },
  {
    id:"nl-ian", name:"Netherlands Innovation Network (IA Network) — Min. of Economic Affairs",
    country:"Netherlands", geography:"National (The Hague) + innovation hubs", actorType:"Diplomatic",
    sdType:["d4s","s4d"], sinceYear:2003, activity:"B",
    domains:["Digital","Quantum","Energy","Health","General S&T"],
    orientation:"Competitive", interestFocus:"National", coreObjective:"Connect Dutch & global innovation ecosystems; support economic security",
    positioning:"Secondary", explicitness:"Implicit", governance:"Coordinated",
    tools:["Nodality","Treasure","Organisation"],
    sciFields:["ICT","Engineering","Life sciences"],
    networked:"Innovation Attachés co-located with embassies; partners RVO, top sectors.",
    documents:["Innovation attaché network reports"],
    alignment:"Aligned to the economic-security/competitiveness dimension of the Framework."
  },
  {
    id:"nl-nwo", name:"Dutch Research Council (NWO)",
    country:"Netherlands", geography:"National (The Hague)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:1950, activity:"B",
    domains:["General S&T","Climate","Health","Quantum"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Coordinate national & international knowledge policy and funding",
    positioning:"Secondary", explicitness:"Explicit", governance:"Coordinated council",
    tools:["Treasure","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Bridges government international knowledge policy & institutions; Science4Diplomacy activities.",
    documents:["NWO strategy","Science diplomacy web programme"],
    alignment:"Aligned — explicitly frames a 'science diplomacy' role bridging policy and institutions."
  },
  {
    id:"nl-wrr", name:"Scientific Council for Government Policy (WRR)",
    country:"Netherlands", geography:"National (The Hague)", actorType:"Policy Advice",
    sdType:["SinD"], sinceYear:1972, activity:"C",
    domains:["HSS","Digital","Climate","Health","Security/Dual-use"],
    orientation:"Cooperative", interestFocus:"National", coreObjective:"Independent multidisciplinary advice on long-term policy issues",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Independent advisory body",
    tools:["Nodality","Authority"],
    sciFields:["Social sciences","Economics","Law"],
    networked:"INGSA member; feeds science into government strategy incl. external relations.",
    documents:["WRR reports (e.g. on security, AI, EU)"],
    alignment:"Enabling — strengthens the science-into-policy capacity the Framework calls for."
  },

  /* ===================== PAN-EU / TRANSNATIONAL NETWORKS ===================== */
  {
    id:"x-s4d4c", name:"S4D4C / EU Science Diplomacy Alliance",
    country:"EU", geography:"Transnational network (Vienna-coordinated)", actorType:"NGO/Network",
    sdType:["s4d","d4s","SinD","DinS"], sinceYear:2018, activity:"B",
    domains:["General S&T","Climate","Health","Water","HSS"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Build EU science diplomacy capacity, training & community of practice",
    positioning:"Primary", explicitness:"Explicit", governance:"Network/consortium",
    tools:["Nodality","Organisation","Training"],
    sciFields:["All fields"],
    networked:"Successor to S4D4C, InsSciDE, EL-CSID Horizon projects; trains diplomats & scientists; informs the Framework.",
    documents:["State-of-the-art reports","Training curricula","Madrid Declaration"],
    alignment:"Foundational input to the EU Framework — high alignment & intellectual influence."
  },
  {
    id:"x-allea", name:"ALLEA — All European Academies",
    country:"EU", geography:"Transnational (Berlin secretariat)", actorType:"Policy Advice",
    sdType:["SinD","s4d"], sinceYear:1994, activity:"C",
    domains:["HSS","General S&T","Climate","Health"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Federate national academies; advise on science & values (academic freedom, integrity)",
    positioning:"Secondary", explicitness:"Implicit", governance:"Federation of academies",
    tools:["Nodality","Authority","Organisation"],
    sciFields:["All fields"],
    networked:"50+ academies in 40+ countries; runs SAPEA with the Commission's SAM.",
    documents:["European Code of Conduct for Research Integrity","Statements on academic freedom"],
    alignment:"Aligned — academy diplomacy & values protection central to the Framework."
  },
  {
    id:"x-fmstan", name:"FMSTAN — Foreign Ministries S&T Advisers Network / SPIDER",
    country:"EU", geography:"Transnational (informal, global)", actorType:"NGO/Network",
    sdType:["s4d","SinD"], sinceYear:2016, activity:"C",
    domains:["General S&T","Security/Dual-use","Health","Climate"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Peer network of S&T advisers in foreign ministries; share practice",
    positioning:"Primary", explicitness:"Explicit", governance:"Informal network",
    tools:["Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Convenes MFA science advisers; met with S4D4C/SPIDER in Vienna; links EU & non-EU ministries.",
    documents:["Meeting reports","Joint statements with SPIDER"],
    alignment:"Aligned — operationalises the 'science adviser in the MFA' role the Framework promotes."
  },

  /* ===================== SPAIN ===================== */
  {
    id:"es-maec", name:"Ministry of Foreign Affairs, EU & Cooperation (MAEC)",
    country:"Spain", geography:"National (Madrid) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2016, activity:"B",
    domains:["General S&T","Climate","Health","Oceans"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Use science as soft power; coordinate STI diplomacy strategy",
    positioning:"Primary", explicitness:"Explicit", governance:"Coordinated inter-ministerial",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Co-owns 2016 STI Diplomacy Strategy with Min. of Science; hosts FECYT scientific coordinators in embassies.",
    documents:["Strategy for Science, Technology & Innovation Diplomacy (2016)"],
    alignment:"Aligned — early national SD strategy; bottom-up model complements the Framework."
  },
  {
    id:"es-fecyt", name:"FECYT — Spanish Foundation for Science & Technology + Science Diplomacy Network",
    country:"Spain", geography:"National (Madrid) + embassy coordinators", actorType:"NGO/Network",
    sdType:["s4d","d4s"], sinceYear:2016, activity:"B",
    domains:["General S&T","Health","Digital"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Mobilise Spanish researchers abroad as a science-diplomacy network",
    positioning:"Primary", explicitness:"Explicit", governance:"Public foundation",
    tools:["Nodality","Organisation","Treasure"],
    sciFields:["All fields"],
    networked:"Runs the 'Science Diplomacy Network'; deployed scientific coordinators to Washington, London, Berlin (2018 pilot).",
    documents:["Science Diplomacy Network materials","Annual activity reports"],
    alignment:"Strong — diaspora/network model directly serves the Framework's talent & influence aims."
  },
  {
    id:"es-cdti", name:"CDTI — Centre for the Development of Industrial Technology",
    country:"Spain", geography:"National (Madrid) + tech attachés", actorType:"Governmental/IO",
    sdType:["d4s"], sinceYear:1977, activity:"C",
    domains:["Digital","Space","Energy","General S&T"],
    orientation:"Competitive", interestFocus:"National", coreObjective:"Support business R&D internationalisation & innovation diplomacy",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Public agency",
    tools:["Treasure","Organisation"],
    sciFields:["Engineering","ICT","Space"],
    networked:"Network of technological attachés; manages ESA/Eureka participation; partners FECYT on SD network.",
    documents:["CDTI international programmes"],
    alignment:"Aligned to the competitiveness/economic-security strand of the Framework."
  },
  {
    id:"es-csic", name:"CSIC — Spanish National Research Council",
    country:"Spain", geography:"National (Madrid) + Brussels & Rome offices", actorType:"Scientific/Research",
    sdType:["d4s","DinS"], sinceYear:1939, activity:"B",
    domains:["General S&T","Oceans","Climate","Health","Archaeology"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Conduct & internationalise Spanish public research",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Large public research body",
    tools:["Organisation","Nodality","Treasure"],
    sciFields:["All fields"],
    networked:"International joint units; Antarctic & oceanographic campaigns; archaeology missions abroad.",
    documents:["CSIC international strategy"],
    alignment:"Aligned as a research actor delivering partnerships & 'diplomacy in science'."
  },

  /* ===================== ITALY ===================== */
  {
    id:"it-maeci", name:"MAECI (Farnesina) — DGSP & Network of Scientific/Space Attachés",
    country:"Italy", geography:"National (Rome) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2000, activity:"A",
    domains:["General S&T","Space","Health","Digital","Archaeology"],
    orientation:"Mixed", interestFocus:"Cross-border", coreObjective:"Promote Italian S&T abroad; support competitiveness of industry",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised (DGSP-led)",
    tools:["Authority","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Expanded science/space attaché network by ~70%; attachés seconded from public bodies (Art.168); links to CNR.",
    documents:["Science diplomacy pages (esteri.it)","Scientific Attachés conference proceedings"],
    alignment:"Strong — explicit, well-resourced attaché network central to the Framework's operational layer."
  },
  {
    id:"it-cnr", name:"CNR — National Research Council of Italy",
    country:"Italy", geography:"National (Rome) + Brussels office", actorType:"Scientific/Research",
    sdType:["d4s","SinD"], sinceYear:1923, activity:"B",
    domains:["General S&T","Oceans","Climate","Health","Polar"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Conduct research & support diplomacy with scientific expertise",
    positioning:"Secondary", explicitness:"Explicit", governance:"Large public research body",
    tools:["Nodality","Organisation","Treasure"],
    sciFields:["All fields"],
    networked:"Supports scientific attachés abroad; ran the 'DIPLOMAzia' programme (2015–16); bilateral agreements.",
    documents:["DIPLOMAzia programme outputs","International relations reports"],
    alignment:"Aligned — supplies expertise into diplomacy; partner to MAECI attaché network."
  },
  {
    id:"it-mur", name:"Ministry of University & Research (MUR)",
    country:"Italy", geography:"National (Rome)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:2020, activity:"C",
    domains:["General S&T","Space","Health"],
    orientation:"Mixed", interestFocus:"National", coreObjective:"Set research policy incl. international cooperation",
    positioning:"Secondary", explicitness:"Implicit", governance:"Centralised",
    tools:["Treasure","Authority"],
    sciFields:["All fields"],
    networked:"Steers CNR, ASI, INFN; Horizon Europe; bilateral S&T programmes with MAECI.",
    documents:["National Research Programme (PNR)"],
    alignment:"Aligned — research-policy pillar supporting Italy's SD posture."
  },

  /* ===================== AUSTRIA ===================== */
  {
    id:"at-bmeia", name:"Federal Ministry for European & International Affairs (BMEIA) — S&T Cooperation",
    country:"Austria", geography:"National (Vienna) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2018, activity:"C",
    domains:["General S&T","Climate","Security/Dual-use"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Integrate science into Austrian foreign policy",
    positioning:"Secondary", explicitness:"Emerging", governance:"Coordinated",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Co-organised FMSTAN/SPIDER Vienna meetings with IIASA; works with OeAD & universities.",
    documents:["Scientific & Technical Cooperation programme materials"],
    alignment:"Aligned, emerging — Austria treats SD as a 'relatively new field'; building toward the Framework."
  },
  {
    id:"at-oead", name:"OeAD — Austria's Agency for Education & Internationalisation",
    country:"Austria", geography:"National (Vienna)", actorType:"Training",
    sdType:["d4s","s4d"], sinceYear:1961, activity:"B",
    domains:["General S&T","HSS","Climate"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Run mobility, S&T cooperation & development-research programmes",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Public agency",
    tools:["Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Manages bilateral S&T cooperation (WTZ) programmes; Austria Centres; Appear development research.",
    documents:["WTZ programme reports","APPEAR programme outputs"],
    alignment:"Aligned — capacity, mobility & training instruments the Framework's 'enabling' layer relies on."
  },
  {
    id:"at-zsi", name:"ZSI — Centre for Social Innovation (S4D4C coordinator)",
    country:"Austria", geography:"National (Vienna) + EU projects", actorType:"NGO/Network",
    sdType:["s4d","d4s","SinD","DinS"], sinceYear:2018, activity:"B",
    domains:["General S&T","HSS","Climate","Health"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Research & train the EU SD community of practice",
    positioning:"Primary", explicitness:"Explicit", governance:"Research NGO",
    tools:["Nodality","Organisation","Training"],
    sciFields:["Social sciences","All fields"],
    networked:"Coordinated H2020 S4D4C; co-founder EU Science Diplomacy Alliance; trains diplomats.",
    documents:["S4D4C case studies & reports","Science Diplomacy in the Making (2020)"],
    alignment:"High — intellectual contributor to the Framework's evidence base."
  },
  {
    id:"at-iiasa", name:"IIASA — International Institute for Applied Systems Analysis",
    country:"Austria", geography:"Sited in Laxenburg (AT); intergovernmental membership", actorType:"Scientific/Research",
    sdType:["s4d","SinD"], sinceYear:1972, activity:"A",
    domains:["Climate","Energy","Food security","Biodiversity","Water","General S&T"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Systems analysis bridging science & policy across geopolitical divides",
    positioning:"Primary", explicitness:"Explicit", governance:"Intergovernmental (member academies)",
    tools:["Nodality","Organisation","Authority"],
    sciFields:["Systems analysis","Environmental","Economics","Demography"],
    networked:"Founded as Cold-War bridge-building institute; national member organisations; UN/IPCC links; co-hosted FMSTAN.",
    documents:["IIASA global assessments","Systems analysis reports for policy"],
    alignment:"Exemplary — the archetypal 'science for diplomacy' bridge institution; strongly cited in SD literature. (Sited in AT but international — logged under host country with IO note.)"
  },

  /* ===================== POLAND ===================== */
  {
    id:"pl-msz", name:"Ministry of Foreign Affairs (MSZ) + Diplomatic Academy",
    country:"Poland", geography:"National (Warsaw) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2000, activity:"C",
    domains:["General S&T","HSS","Security/Dual-use","Climate"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Promote & internationalise Polish science as part of foreign policy",
    positioning:"Secondary", explicitness:"Emerging", governance:"Coordinated",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Historically led science promotion (cultural diplomacy); Diplomatic Academy trains diplomats; works with PAN.",
    documents:["Diplomatic Academy materials","Foreign policy strategy"],
    alignment:"Aligned, emerging — Polish SD is largely bottom-up; ministry coordination still consolidating."
  },
  {
    id:"pl-pan", name:"Polish Academy of Sciences (PAN) + PolSCA Brussels & foreign stations",
    country:"Poland", geography:"National (Warsaw) + stations Paris/Rome/Vienna/Kyiv/Berlin/Brussels", actorType:"Scientific/Research",
    sdType:["d4s","s4d","SinD"], sinceYear:1952, activity:"B",
    domains:["General S&T","HSS","Archaeology","Climate","Space"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Internationalise Polish science; represent it abroad (d4s priority)",
    positioning:"Primary", explicitness:"Explicit", governance:"Self-governing academy + 79 institutes (fragmented)",
    tools:["Nodality","Organisation","Authority"],
    sciFields:["All fields"],
    networked:"Foreign scientific stations & PolSCA contact agency in Brussels; ALLEA/IAP member; bottom-up partnerships.",
    documents:["PAN international activity reports","Science diplomacy of Poland (academic study, 2020)"],
    alignment:"Aligned — active across all three classic SD types; matches the Framework's academy-diplomacy role."
  },
  {
    id:"pl-fnp", name:"Foundation for Polish Science (FNP)",
    country:"Poland", geography:"National (Warsaw)", actorType:"NGO/Network",
    sdType:["d4s"], sinceYear:1991, activity:"C",
    domains:["General S&T","Health","Quantum"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Support top researchers & international mobility (talent diplomacy)",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Independent foundation",
    tools:["Treasure","Nodality"],
    sciFields:["All fields"],
    networked:"Runs PASIFIC (MSCA-cofunded) fellowships; partners EU programmes; alumni network.",
    documents:["FNP programme reports","PASIFIC fellowship materials"],
    alignment:"Aligned — 'diplomacy for science' talent instrument."
  },
  {
    id:"pl-krasp", name:"KRASP — Conference of Rectors of Academic Schools in Poland",
    country:"Poland", geography:"National (Warsaw)", actorType:"NGO/Network",
    sdType:["d4s"], sinceYear:1997, activity:"D",
    domains:["General S&T","HSS"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Represent universities; coordinate internationalisation",
    positioning:"Tertiary", explicitness:"Implicit", governance:"Rectors' association",
    tools:["Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Member of EUA; partners ministries on internationalisation; historic role in science promotion.",
    documents:["KRASP resolutions & strategy papers"],
    alignment:"Aligned — rectors' associations are the university-sector voice the Framework engages."
  },

  /* ===================== SWEDEN ===================== */
  {
    id:"se-mfa", name:"Ministry for Foreign Affairs (UD) + Innovation/Research Offices",
    country:"Sweden", geography:"National (Stockholm) + 7 innovation & research offices", actorType:"Diplomatic",
    sdType:["d4s","s4d"], sinceYear:2010, activity:"B",
    domains:["General S&T","Climate","Digital","Energy","Health"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Promote Swedish research & innovation; 'innovation diplomacy'",
    positioning:"Secondary", explicitness:"Implicit", governance:"Coordinated (agency-led)",
    tools:["Nodality","Organisation","Treasure"],
    sciFields:["All fields"],
    networked:"7 innovation/research offices abroad; works with Vinnova, VR; historic SD legacy (1972 Stockholm Conference).",
    documents:["Innovation diplomacy materials","1972 Stockholm Conference legacy"],
    alignment:"Aligned — strong agency-coordinated model; less explicit 'SD' branding than the Framework uses."
  },
  {
    id:"se-stint", name:"STINT — Swedish Foundation for Int'l Cooperation in Research & Higher Education",
    country:"Sweden", geography:"National (Stockholm)", actorType:"NGO/Network",
    sdType:["d4s","s4d"], sinceYear:1994, activity:"B",
    domains:["General S&T","HSS","Climate"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Internationalise Swedish HE & research; build a science-diplomacy capacity",
    positioning:"Primary", explicitness:"Explicit", governance:"Parliament-created foundation",
    tools:["Treasure","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Funds partnerships & mobility; published 'Science Diplomacy in and for Sweden' (2022).",
    documents:["Science Diplomacy in and for Sweden (2022)"],
    alignment:"Strong — explicitly frames and advocates Swedish science diplomacy."
  },
  {
    id:"se-vr", name:"Swedish Research Council (VR) + IntSam coordination",
    country:"Sweden", geography:"National (Stockholm)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:2001, activity:"B",
    domains:["General S&T","Climate","Space","Health"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Fund research; coordinate agencies' international activity (IntSam)",
    positioning:"Secondary", explicitness:"Implicit", governance:"Coordinated council",
    tools:["Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Convenes IntSam with Vinnova, Formas, Forte, SNSA, Energy Agency; big-science memberships (CERN, ESS, ESO).",
    documents:["International strategy","IntSam coordination materials"],
    alignment:"Aligned — funder coordination underpins the Framework's 'enabling' instruments."
  },
  {
    id:"se-iva", name:"IVA — Royal Swedish Academy of Engineering Sciences",
    country:"Sweden", geography:"National (Stockholm)", actorType:"Policy Advice",
    sdType:["SinD","s4d"], sinceYear:1919, activity:"C",
    domains:["General S&T","Energy","Digital","Climate"],
    orientation:"Cooperative", interestFocus:"National", coreObjective:"Bridge engineering science, business & policy",
    positioning:"Tertiary", explicitness:"Implicit", governance:"State-funded academy/foundation",
    tools:["Nodality","Authority","Organisation"],
    sciFields:["Engineering","Economics"],
    networked:"Convenes industry & policy; international academy links; advises on research & innovation policy.",
    documents:["IVA policy reports & roadmaps"],
    alignment:"Enabling — academy-business-policy convening complements the Framework."
  },

  /* ===================== BELGIUM ===================== */
  {
    id:"be-fps", name:"FPS Foreign Affairs (Diplomatie.be) — incl. space & S&T cooperation",
    country:"Belgium", geography:"National (Brussels) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2000, activity:"C",
    domains:["Space","General S&T","Security/Dual-use","Polar"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Embed S&T (esp. space) in foreign policy; host EU/NATO institutions",
    positioning:"Secondary", explicitness:"Emerging", governance:"Federal + regional (fragmented)",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["Space","All fields"],
    networked:"Coordinates with BELSPO on ESA; Brussels hosts EU/NATO; works across federal & regional levels.",
    documents:["International space policy materials"],
    alignment:"Aligned — strong in space diplomacy; federal/regional split complicates a single SD posture."
  },
  {
    id:"be-belspo", name:"BELSPO — Belgian Science Policy Office",
    country:"Belgium", geography:"National (Brussels)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:1959, activity:"B",
    domains:["Space","Polar","Climate","Biodiversity","Oceans","General S&T"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Manage federal research & Belgium's role in int'l scientific organisations",
    positioning:"Secondary", explicitness:"Implicit", governance:"Federal science administration",
    tools:["Treasure","Organisation","Authority"],
    sciFields:["Space","Polar","Environmental","All fields"],
    networked:"Main Belgian actor in ESA; runs Belgian Polar Platform (Princess Elisabeth Antarctica); coordinates with Foreign Affairs.",
    documents:["Federal research programme reports","Belgian Polar Platform materials"],
    alignment:"Aligned — delivers big-science & polar diplomacy the Framework values; coordinates with MFA."
  },

  /* ===================== CZECHIA ===================== */
  {
    id:"cz-mzv", name:"MFA — Science Diplomacy Unit (Economic & Science Diplomacy Dept.)",
    country:"Czechia", geography:"National (Prague) + ~90 missions", actorType:"Diplomatic",
    sdType:["s4d","d4s","SinD"], sinceYear:2015, activity:"B",
    domains:["General S&T","Digital","Health","Security/Dual-use"],
    orientation:"Mixed", interestFocus:"Cross-border", coreObjective:"Build SD capacity; connect Czech science, firms & diplomacy",
    positioning:"Primary", explicitness:"Explicit", governance:"Coordinated (interministerial steering group)",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Dedicated SD Unit; scientific counsellors/attachés at ~90 missions; interministerial group at RVVI with TACR, GACR, CAS.",
    documents:["Science diplomacy strategy/pages (mzv.gov.cz)"],
    alignment:"Strong — explicit, institutionalised SD Unit; close fit with the Framework's operational layer."
  },
  {
    id:"cz-cas", name:"Czech Academy of Sciences (CAS / AV ČR)",
    country:"Czechia", geography:"National (Prague) + 54 institutes", actorType:"Scientific/Research",
    sdType:["d4s","SinD"], sinceYear:1992, activity:"B",
    domains:["General S&T","HSS","Health","Climate"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Integrate Czech science into the international context",
    positioning:"Secondary", explicitness:"Implicit", governance:"Self-governing academy + 54 institutes",
    tools:["Organisation","Nodality","Treasure"],
    sciFields:["All fields"],
    networked:"Member of interministerial SD group; ALLEA/IAP; bilateral academy agreements; mobility schemes.",
    documents:["CAS international strategy"],
    alignment:"Aligned — academy diplomacy plus participation in national SD coordination."
  },

  /* ===================== PORTUGAL ===================== */
  {
    id:"pt-fct", name:"FCT — Foundation for Science & Technology (incl. goPORTUGAL)",
    country:"Portugal", geography:"National (Lisbon)", actorType:"Governmental/IO",
    sdType:["d4s","s4d"], sinceYear:1997, activity:"B",
    domains:["General S&T","Oceans","Climate","Space","Health"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Fund research & steer bilateral/multilateral S&T agreements",
    positioning:"Primary", explicitness:"Explicit", governance:"Public funding agency",
    tools:["Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Runs goPORTUGAL & int'l partnerships (MIT, CMU, UT Austin); places postdoc science advisers in embassies; CPLP/PSAC focus.",
    documents:["goPORTUGAL programme (2018)","International cooperation agreements"],
    alignment:"Strong — funder-led SD with embassy science advisers; close to the Framework's model."
  },
  {
    id:"pt-mne", name:"Ministry of Foreign Affairs (MNE) — Camões & S&T cooperation",
    country:"Portugal", geography:"National (Lisbon) + lusophone network", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2018, activity:"C",
    domains:["General S&T","Oceans","HSS","Climate"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Use science & language ties (CPLP) for influence & development",
    positioning:"Secondary", explicitness:"Emerging", governance:"Coordinated",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Co-hosts embassy science advisers with FCT; Camões Institute; Portuguese-speaking African countries & Timor-Leste.",
    documents:["MNE–FCT cooperation materials"],
    alignment:"Aligned — combines science with cultural/lusophone diplomacy in line with the Framework."
  },

  /* ===================== DENMARK ===================== */
  {
    id:"dk-icdk", name:"Innovation Centre Denmark (ICDK)",
    country:"Denmark", geography:"National (Copenhagen) + 7 innovation hubs", actorType:"Diplomatic",
    sdType:["d4s","s4d"], sinceYear:2006, activity:"A",
    domains:["Digital","Energy","Health","General S&T","Quantum"],
    orientation:"Competitive", interestFocus:"National", coreObjective:"Connect Danish research & business to global innovation ecosystems (triple-helix)",
    positioning:"Primary", explicitness:"Explicit", governance:"Joint MFA + Min. of HE & Science",
    tools:["Nodality","Organisation","Treasure"],
    sciFields:["ICT","Life sciences","Engineering","Quantum"],
    networked:"7 centres (Silicon Valley, Boston, Munich, Bangalore, Seoul, Shanghai, Tel Aviv); part of the foreign service; green/life-science/tech focus.",
    documents:["ICDK annual reports","CFA evaluation of ICDK"],
    alignment:"Strong — embedded science-in-the-foreign-service model the Framework promotes."
  },
  {
    id:"dk-techamb", name:"Tech Ambassador / TechPlomacy (Office of Denmark's Tech Ambassador)",
    country:"Denmark", geography:"HQ Silicon Valley + Copenhagen & Beijing", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2017, activity:"A",
    domains:["Digital","AI","Quantum","Security/Dual-use"],
    orientation:"Mixed", interestFocus:"Global", coreObjective:"Conduct diplomacy with the tech industry as a geopolitical actor ('TechPlomacy')",
    positioning:"Primary", explicitness:"Explicit", governance:"MFA (ambassador-rank office)",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["ICT","AI","Quantum"],
    networked:"World's first national tech ambassador; engages Big Tech directly; inspired other states' tech-diplomacy offices.",
    documents:["TechPlomacy strategy materials"],
    alignment:"Pioneering — extends SD into digital/tech diplomacy, a priority domain of the Framework."
  },

  /* ===================== FINLAND ===================== */
  {
    id:"fi-um", name:"Ministry for Foreign Affairs (UM) + Academy joint development research",
    country:"Finland", geography:"National (Helsinki) + missions", actorType:"Diplomatic",
    sdType:["s4d","d4s"], sinceYear:2012, activity:"C",
    domains:["Climate","General S&T","Food security","Health"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Use science to 'operate larger than its size'; SDGs & climate",
    positioning:"Secondary", explicitness:"Emerging", governance:"Coordinated",
    tools:["Treasure","Nodality","Organisation"],
    sciFields:["All fields"],
    networked:"Co-funds development research with Research Council of Finland; works with OKM ministry & academies.",
    documents:["Development research strategy","MFA research project materials"],
    alignment:"Aligned, emerging — Finland building explicit SD capacity per the academy report's recommendations."
  },
  {
    id:"fi-acadsci", name:"Finnish Academy of Science and Letters",
    country:"Finland", geography:"National (Helsinki)", actorType:"Policy Advice",
    sdType:["SinD","s4d"], sinceYear:1908, activity:"C",
    domains:["General S&T","HSS","Climate"],
    orientation:"Cooperative", interestFocus:"National", coreObjective:"Advise on science & represent the Finnish scientific community",
    positioning:"Secondary", explicitness:"Explicit", governance:"Self-governing academy",
    tools:["Nodality","Authority"],
    sciFields:["All fields"],
    networked:"Produced a national science-diplomacy report (survey/interviews) with 10 recommendations; ALLEA member.",
    documents:["Finnish science diplomacy report (10 recommendations)"],
    alignment:"Strong — explicitly advancing a national SD agenda mapped onto the EU Framework."
  },

  /* ===================== IRELAND ===================== */
  {
    id:"ie-research", name:"Research Ireland (formerly Science Foundation Ireland + IRC)",
    country:"Ireland", geography:"National (Dublin)", actorType:"Governmental/IO",
    sdType:["d4s"], sinceYear:2000, activity:"B",
    domains:["General S&T","Digital","Health","Climate","Food security"],
    orientation:"Competitive", interestFocus:"Global", coreObjective:"Fund research; attract talent & build international partnerships",
    positioning:"Secondary", explicitness:"Implicit", governance:"National funding agency",
    tools:["Treasure","Nodality","Organisation"],
    sciFields:["ICT","Life sciences","Engineering"],
    networked:"International strategy (5 pillars); SDG Challenge with Irish Aid; co-investment with national funders.",
    documents:["SFI Strategy 'Shaping Our Future'","International strategy pillars"],
    alignment:"Aligned — funder-led talent/partnership diplomacy; SDG Challenge links science to development."
  },
  {
    id:"ie-dfa", name:"Department of Foreign Affairs — Global Ireland & Irish Aid",
    country:"Ireland", geography:"National (Dublin) + expanding mission network", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2018, activity:"C",
    domains:["General S&T","Health","Climate","Water"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Project influence via Global Ireland; science for peacebuilding & development",
    positioning:"Secondary", explicitness:"Emerging", governance:"Coordinated",
    tools:["Authority","Nodality","Treasure"],
    sciFields:["All fields"],
    networked:"Global Ireland strategies; Irish Aid–Research Ireland SDG partnership; British–Irish Council shared evidence (peacebuilding).",
    documents:["Global Ireland strategies"],
    alignment:"Aligned — notable for science-for-peacebuilding, a core SD value in the Framework."
  },

  /* ===================== GREECE ===================== */
  {
    id:"gr-mfa", name:"Hellenic MFA — Science & Public Diplomacy",
    country:"Greece", geography:"National (Athens) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2020, activity:"D",
    domains:["General S&T","Archaeology","HSS","Digital","Oceans"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Develop Greece's role in EU science diplomacy; leverage cultural heritage",
    positioning:"Secondary", explicitness:"Emerging", governance:"Coordinated (forming)",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["All fields","Archaeology"],
    networked:"Hosting 'Role of Greece in EU Science Diplomacy' symposium (Jun 2026); engages diaspora & academics abroad.",
    documents:["EU SD symposium programme (2026)","Cultural diplomacy materials"],
    alignment:"Emerging — explicitly orienting toward the EU Framework; community still forming."
  },
  {
    id:"gr-diaspora", name:"Greek Diaspora Knowledge Network ('Knowledge & Partnership Bridges')",
    country:"Greece", geography:"National (Athens) + global diaspora", actorType:"NGO/Network",
    sdType:["d4s","s4d"], sinceYear:2016, activity:"C",
    domains:["AI","Digital","General S&T","Health","Energy"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Mobilise the Greek scientific diaspora as a knowledge & partnership asset",
    positioning:"Primary", explicitness:"Explicit", governance:"Network/platform",
    tools:["Nodality","Organisation"],
    sciFields:["AI","ICT","Biotechnology","Materials","Energy"],
    networked:"Links 250k+ Greek-born professionals & wider 8M diaspora; bridges to universities & firms abroad.",
    documents:["Knowledge & Partnership Bridges programme materials"],
    alignment:"Aligned — exemplifies the diaspora-network instrument the project taxonomy & Framework highlight."
  },

  /* ===================== SWITZERLAND (Horizon-associated) ===================== */
  {
    id:"ch-fdfa", name:"Federal Dept. of Foreign Affairs (FDFA) — Science & Foreign Policy",
    country:"Switzerland", geography:"National (Bern) + Int'l Geneva (assoc. state)", actorType:"Diplomatic",
    sdType:["s4d","SinD","d4s"], sinceYear:2018, activity:"A",
    domains:["General S&T","Health","Digital","Climate","Quantum","Security/Dual-use"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Anticipatory science diplomacy; strengthen multilateralism via Int'l Geneva",
    positioning:"Primary", explicitness:"Explicit", governance:"Coordinated (FDFA + EAER/SERI)",
    tools:["Authority","Nodality","Organisation","Treasure"],
    sciFields:["All fields"],
    networked:"SD is a pillar of Foreign Policy Strategy 2024–27; backs GESDA, swissnex, CERN; co-led with EAER/SERI.",
    documents:["Foreign Policy Strategy 2024–27","Science-diplomacy pages (eda.admin.ch)"],
    alignment:"Exemplary — among the most explicit, anticipatory SD doctrines; a reference point for the Framework."
  },
  {
    id:"ch-gesda", name:"GESDA — Geneva Science and Diplomacy Anticipator",
    country:"Switzerland", geography:"International Geneva (assoc. state)", actorType:"NGO/Network",
    sdType:["s4d","SinD"], sinceYear:2019, activity:"A",
    domains:["Quantum","AI","Health","Climate","Space","Digital","General S&T"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Anticipate scientific breakthroughs & use them to strengthen multilateralism",
    positioning:"Primary", explicitness:"Explicit", governance:"Public-private foundation (Confederation + Geneva)",
    tools:["Nodality","Organisation","Authority"],
    sciFields:["Quantum","AI","Neuroscience","Eco-regeneration","Space"],
    networked:"Runs the 'Science Breakthrough Radar'; convenes scientists & diplomats in Int'l Geneva; Open Quantum Institute.",
    documents:["Science Breakthrough Radar (annual)","GESDA summit reports"],
    alignment:"Exemplary — anticipatory, multilateral SD model strongly resonant with the Framework's forward-looking aims."
  },
  {
    id:"ch-swissnex", name:"swissnex — Swiss global network for education, research & innovation",
    country:"Switzerland", geography:"Hubs in innovation centres worldwide (assoc. state)", actorType:"Diplomatic",
    sdType:["d4s","s4d"], sinceYear:2000, activity:"B",
    domains:["Digital","Health","General S&T","Energy"],
    orientation:"Competitive", interestFocus:"National", coreObjective:"Connect Swiss research/innovation to global hubs (public-private)",
    positioning:"Secondary", explicitness:"Explicit", governance:"Public-private, under EAER/SERI + FDFA",
    tools:["Nodality","Organisation","Treasure"],
    sciFields:["ICT","Life sciences","Engineering"],
    networked:"swissnex hubs (Boston, SF, Bangalore, Shanghai, Rio, Osaka…); trains 'next-generation science diplomats'.",
    documents:["swissnex annual report"],
    alignment:"Aligned — network/attaché model the Framework's operational layer relies on."
  },

  /* ===================== NORWAY (Horizon-associated) ===================== */
  {
    id:"no-mfa", name:"Ministry of Foreign Affairs — Arctic & High North / Svalbard policy",
    country:"Norway", geography:"National (Oslo) + Svalbard (assoc. state)", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2006, activity:"A",
    domains:["Polar","Oceans","Climate","Security/Dual-use","General S&T"],
    orientation:"Mixed", interestFocus:"Cross-border", coreObjective:"Use polar science to anchor sovereignty, cooperation & High-North policy",
    positioning:"Primary", explicitness:"Explicit", governance:"Coordinated",
    tools:["Authority","Nodality","Organisation","Treasure"],
    sciFields:["Polar","Marine","Climate"],
    networked:"Chaired Arctic Council (2023–25); Svalbard research hub; new Svalbard research office (2026) with RCN & Polar Institute.",
    documents:["The Norwegian Government's Arctic Policy","Svalbard research strategy (2026)"],
    alignment:"Exemplary — Arctic/polar science diplomacy is a textbook case the Framework references."
  },
  {
    id:"no-polar", name:"Norwegian Polar Institute",
    country:"Norway", geography:"National (Tromsø) + Arctic/Antarctic stations (assoc. state)", actorType:"Scientific/Research",
    sdType:["SinD","s4d"], sinceYear:1948, activity:"B",
    domains:["Polar","Climate","Oceans","Biodiversity"],
    orientation:"Cooperative", interestFocus:"Global", coreObjective:"Polar research & scientific advice underpinning Arctic/Antarctic governance",
    positioning:"Secondary", explicitness:"Implicit", governance:"Public research/advisory body",
    tools:["Nodality","Organisation","Authority"],
    sciFields:["Polar","Glaciology","Marine biology","Climate"],
    networked:"Ny-Ålesund & Troll stations; Antarctic Treaty/SCAR; staffing the new Svalbard research office.",
    documents:["Scientific advice on Arctic/Antarctic governance"],
    alignment:"Aligned — research-based 'science in diplomacy' for polar governance."
  },
  {
    id:"no-rcn", name:"Research Council of Norway (RCN)",
    country:"Norway", geography:"National (Oslo) (assoc. state)", actorType:"Governmental/IO",
    sdType:["d4s"], sinceYear:1993, activity:"B",
    domains:["Polar","Climate","Energy","Oceans","General S&T"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Fund & internationalise Norwegian research",
    positioning:"Tertiary", explicitness:"Implicit", governance:"National funding council",
    tools:["Treasure","Organisation","Nodality"],
    sciFields:["All fields"],
    networked:"Funds High North Research Centre & polar research; Horizon Europe; new Svalbard office co-staffing.",
    documents:["RCN international strategy"],
    alignment:"Aligned — funder enabling Norway's polar & climate science diplomacy."
  },

  /* ===================== ESTONIA ===================== */
  {
    id:"ee-mfa", name:"Ministry of Foreign Affairs — Digital & Cyber Diplomacy Dept.",
    country:"Estonia", geography:"National (Tallinn) + missions", actorType:"Diplomatic",
    sdType:["s4d","SinD"], sinceYear:2019, activity:"B",
    domains:["Digital","AI","Security/Dual-use","General S&T"],
    orientation:"Mixed", interestFocus:"Global", coreObjective:"Project e-governance expertise as digital & science diplomacy",
    positioning:"Primary", explicitness:"Explicit", governance:"Centralised (digital-first state)",
    tools:["Authority","Nodality","Organisation"],
    sciFields:["ICT","AI","Cybersecurity"],
    networked:"Dedicated Digital & Cyber Diplomacy Dept (2019); e-Residency; exports e-governance; hosts NATO CCDCOE.",
    documents:["Digital diplomacy materials","RDIE Strategy 2021–2035"],
    alignment:"Aligned — leads the digital-diplomacy frontier the Framework names as a priority domain."
  },
  {
    id:"ee-mer", name:"Ministry of Education & Research — RDIE Strategy / international cooperation",
    country:"Estonia", geography:"National (Tartu/Tallinn)", actorType:"Governmental/IO",
    sdType:["d4s","SinD"], sinceYear:2021, activity:"C",
    domains:["Digital","General S&T","Health","Climate"],
    orientation:"Cooperative", interestFocus:"Cross-border", coreObjective:"Boost research capacity & promote science diplomacy with partner regions",
    positioning:"Secondary", explicitness:"Explicit", governance:"Coordinated",
    tools:["Treasure","Authority","Organisation"],
    sciFields:["ICT","All fields"],
    networked:"Runs RDIE Strategy 2021–2035 (with Econ. Affairs); Horizon Europe, Nordic-Baltic, Taiwan & Japan schemes.",
    documents:["RDIE Strategy 2021–2035"],
    alignment:"Aligned — strategy text explicitly names 'science diplomacy' as an objective."
  }
];
