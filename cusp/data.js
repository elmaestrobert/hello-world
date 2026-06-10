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
  }
];
