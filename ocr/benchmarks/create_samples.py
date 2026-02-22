"""
Generate realistic synthetic test PDFs for the OCR benchmark:
  1. Three arxiv-style papers with author affiliations on page 1
  2. Two World Bank-style reports with executive summaries

Run:  python ocr/benchmarks/create_samples.py
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, inch
from reportlab.platypus import (HRFlowable, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table,
                                TableStyle)


# ─── Style helpers ────────────────────────────────────────────────────────────

styles = getSampleStyleSheet()

def _style(name, **kw):
    return ParagraphStyle(name, **kw)

TITLE  = _style("Title",  fontSize=16, leading=20, alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica-Bold")
AUTH   = _style("Authors", fontSize=11, leading=14, alignment=TA_CENTER, spaceAfter=2, fontName="Helvetica")
AFFIL  = _style("Affil",  fontSize=9,  leading=12, alignment=TA_CENTER, spaceAfter=6, fontName="Helvetica-Oblique", textColor=colors.HexColor("#444444"))
EMAIL  = _style("Email",  fontSize=8,  leading=10, alignment=TA_CENTER, spaceAfter=10, fontName="Helvetica", textColor=colors.HexColor("#666666"))
ABSTR  = _style("Abstr",  fontSize=10, leading=14, alignment=TA_JUSTIFY, leftIndent=1*cm, rightIndent=1*cm, spaceAfter=8, fontName="Helvetica")
ABST_H = _style("AbstrH", fontSize=10, leading=14, alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica-Bold")
SECT   = _style("Sect",   fontSize=12, leading=16, spaceAfter=4, spaceBefore=10, fontName="Helvetica-Bold")
BODY   = _style("Body",   fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6, fontName="Helvetica")
SMALL  = _style("Small",  fontSize=8,  leading=11, fontName="Helvetica", textColor=colors.HexColor("#888888"))

WB_TITLE  = _style("WBTitle",  fontSize=20, leading=26, alignment=TA_CENTER, spaceAfter=8, fontName="Helvetica-Bold", textColor=colors.HexColor("#003087"))
WB_SUBT   = _style("WBSubt",   fontSize=13, leading=18, alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica", textColor=colors.HexColor("#003087"))
WB_SECT   = _style("WBSect",   fontSize=13, leading=18, spaceAfter=6, spaceBefore=12, fontName="Helvetica-Bold", textColor=colors.HexColor("#003087"))
WB_BODY   = _style("WBBody",   fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceAfter=8, fontName="Helvetica")
WB_BULLET = _style("WBBullet", fontSize=10, leading=15, leftIndent=1*cm, spaceAfter=4, fontName="Helvetica", bulletIndent=0.5*cm)

LOREM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure "
    "dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."
)


# ─── arxiv-style papers ──────────────────────────────────────────────────────

def _arxiv_paper(path: Path, title: str, authors: list[dict], abstract: str,
                 arxiv_id: str, body_sections: list[tuple[str, str]]):
    """
    authors: list of {name, affil_key, affil}  e.g. [{name:"Alice", affil_key:"1", affil:"MIT"}]
    """
    doc = SimpleDocTemplate(str(path), pagesize=letter,
                            leftMargin=1.2*inch, rightMargin=1.2*inch,
                            topMargin=1*inch, bottomMargin=1*inch)
    story = []

    # arxiv stamp
    story.append(Paragraph(f"arXiv:{arxiv_id} [cs.LG]", SMALL))
    story.append(Spacer(1, 0.2*cm))

    # Title
    story.append(Paragraph(title, TITLE))
    story.append(Spacer(1, 0.3*cm))

    # Authors (with superscript affil keys)
    author_str = ", ".join(
        f"{a['name']}<super>{a['affil_key']}</super>" for a in authors
    )
    story.append(Paragraph(author_str, AUTH))

    # Affiliations (unique)
    seen = {}
    for a in authors:
        if a["affil_key"] not in seen:
            seen[a["affil_key"]] = a["affil"]
    for key, affil in seen.items():
        story.append(Paragraph(f"<super>{key}</super> {affil}", AFFIL))

    # Emails
    emails = [a.get("email", f"{a['name'].split()[0].lower()}@example.edu") for a in authors]
    story.append(Paragraph("{" + ", ".join(emails) + "}", EMAIL))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 0.3*cm))

    # Abstract
    story.append(Paragraph("Abstract", ABST_H))
    story.append(Paragraph(abstract, ABSTR))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey))
    story.append(Spacer(1, 0.3*cm))

    # Body sections
    for i, (sec_title, sec_body) in enumerate(body_sections, 1):
        story.append(Paragraph(f"{i}. {sec_title}", SECT))
        for para in sec_body.split("\n\n"):
            story.append(Paragraph(para.strip(), BODY))
        if i == 3:
            story.append(PageBreak())

    doc.build(story)
    print(f"  Created: {path}")


def create_arxiv_samples(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Paper 1: Vision-Language Model ──────────────────────────────────────
    _arxiv_paper(
        path=out_dir / "vlm_ocr_benchmark_2025.pdf",
        title="Scaling Vision-Language Models for High-Fidelity Document OCR",
        authors=[
            {"name": "Alice Chen",    "affil_key": "1,2", "affil": "Department of Computer Science, Stanford University, Stanford, CA 94305, USA",
             "email": "achen@cs.stanford.edu"},
            {"name": "Bob Kumar",     "affil_key": "1",   "affil": "Department of Computer Science, Stanford University, Stanford, CA 94305, USA",
             "email": "bkumar@cs.stanford.edu"},
            {"name": "Carol Li",      "affil_key": "2",   "affil": "Google DeepMind, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
             "email": "carol.li@deepmind.google.com"},
            {"name": "David Park",    "affil_key": "3",   "affil": "KAIST AI Graduate School, Daejeon 34141, Republic of Korea",
             "email": "dpark@kaist.ac.kr"},
            {"name": "Elena Müller",  "affil_key": "4",   "affil": "Max Planck Institute for Informatics, 66123 Saarbrücken, Germany",
             "email": "emuller@mpi-inf.mpg.de"},
        ],
        arxiv_id="2501.12345",
        abstract=(
            "We present ScaleOCR, a scalable framework for training vision-language models "
            "on document understanding tasks. Our approach combines a high-resolution "
            "image encoder with a large language model decoder, trained on a diverse corpus "
            "of 50 million annotated document pages spanning 84 languages and 12 document "
            "categories. ScaleOCR achieves state-of-the-art results on DocVQA (97.3), "
            "OmniDocBench (91.2), and the OCRBench benchmark suite, outperforming prior "
            "methods by 3.1 points on average. We further demonstrate that scaling model "
            "capacity and training data consistently improves performance, and release our "
            "model weights, training code, and evaluation suite to the research community."
        ),
        body_sections=[
            ("Introduction",
             "Optical character recognition has long been a cornerstone of document digitization. "
             "Recent advances in vision-language models (VLMs) have dramatically improved OCR "
             "quality on complex layouts, multilingual text, and handwriting.\n\n"
             + LOREM + "\n\n" + LOREM),
            ("Related Work",
             "Early OCR systems relied on rule-based character segmentation and HMM-based "
             "recognition. CTC-based models improved performance on scene text. Transformer-based "
             "approaches (Donut, TrOCR) demonstrated end-to-end document understanding.\n\n"
             + LOREM),
            ("Method",
             "Our ScaleOCR architecture consists of three components: (1) a high-resolution "
             "SigLIP visual encoder that processes 4096×4096 images via dynamic tiling, "
             "(2) a cross-attention adapter projecting visual tokens to the LLM embedding space, "
             "and (3) a Qwen-2.5-7B decoder fine-tuned on document QA pairs.\n\n" + LOREM),
            ("Experiments",
             "We evaluate on seven standard benchmarks. Table 1 shows our results. ScaleOCR "
             "achieves 97.3 on DocVQA, 91.2 on OmniDocBench, and 89.1 on OCRBench v2.\n\n"
             + LOREM + "\n\n" + LOREM),
            ("Conclusion", LOREM + "\n\n" + LOREM),
        ],
    )

    # ── Paper 2: Multi-institutional NLP paper ───────────────────────────────
    _arxiv_paper(
        path=out_dir / "multilingual_doc_understanding.pdf",
        title="Multilingual Document Understanding via Cross-Lingual Layout Pretraining",
        authors=[
            {"name": "François Dubois",  "affil_key": "1",   "affil": "INRIA Paris, 2 rue Simone Iff, 75012 Paris, France",
             "email": "francois.dubois@inria.fr"},
            {"name": "Yuki Tanaka",      "affil_key": "2",   "affil": "University of Tokyo, Department of Information Science, Bunkyo-ku, Tokyo 113-8656, Japan",
             "email": "ytanaka@is.s.u-tokyo.ac.jp"},
            {"name": "Priya Sharma",     "affil_key": "3",   "affil": "Indian Institute of Technology Bombay, Mumbai 400076, Maharashtra, India",
             "email": "priya.sharma@iitb.ac.in"},
            {"name": "Marco Rossi",      "affil_key": "4",   "affil": "Sapienza University of Rome, Department of Computer Science, Via Salaria 113, 00198 Rome, Italy",
             "email": "m.rossi@di.uniroma1.it"},
            {"name": "Hannah Schmidt",   "affil_key": "1,5", "affil": "INRIA Paris & ETH Zürich, Department of Computer Science, 8092 Zürich, Switzerland",
             "email": "hschmidt@ethz.ch"},
            {"name": "Chen Wei",         "affil_key": "6",   "affil": "Tsinghua University, Institute for AI Industry Research (AIR), Beijing 100084, China",
             "email": "chenwei@air.tsinghua.edu.cn"},
        ],
        arxiv_id="2502.67890",
        abstract=(
            "Document understanding across languages poses unique challenges due to diverse "
            "scripts, reading orders, and layout conventions. We introduce XLayout-BERT, "
            "a multilingual layout-aware pretrained model trained on 120 million document "
            "pages in 50 languages. Using a novel cross-lingual layout alignment objective, "
            "XLayout-BERT achieves an average of 89.4 F1 across multilingual document "
            "benchmarks, surpassing prior state-of-the-art by 6.2 points. We additionally "
            "release a new benchmark, MultiDocBench, covering 15 languages and 8 document "
            "types including academic papers, government forms, invoices, and newspapers."
        ),
        body_sections=[
            ("Introduction", LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Cross-Lingual Layout Pretraining", LOREM + "\n\n" + LOREM),
            ("MultiDocBench Dataset", LOREM + "\n\n" + LOREM),
            ("Experiments and Results", LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Analysis", LOREM + "\n\n" + LOREM),
            ("Conclusion", LOREM),
        ],
    )

    # ── Paper 3: Reinforcement learning for OCR ──────────────────────────────
    _arxiv_paper(
        path=out_dir / "rl_ocr_training.pdf",
        title="Reward-Guided OCR: Reinforcement Learning with Verifiable Document Rewards",
        authors=[
            {"name": "James O'Brien",   "affil_key": "1",   "affil": "Allen Institute for AI (Ai2), Seattle, WA 98103, USA",
             "email": "jamesobrien@allenai.org"},
            {"name": "Sofia Garcia",    "affil_key": "2",   "affil": "University of Washington, Paul G. Allen School of Computer Science, Seattle, WA 98195, USA",
             "email": "sgarcia@cs.washington.edu"},
            {"name": "Arjun Gupta",     "affil_key": "1,2", "affil": "Allen Institute for AI (Ai2) & University of Washington",
             "email": "agupta@allenai.org"},
            {"name": "Wei-Lin Chiang",  "affil_key": "3",   "affil": "UC Berkeley, EECS Department, Berkeley, CA 94720, USA",
             "email": "wlchiang@eecs.berkeley.edu"},
        ],
        arxiv_id="2510.19817",
        abstract=(
            "Training OCR models with maximum likelihood estimation on noisy ground-truth "
            "annotations leads to systematic errors on challenging document elements such as "
            "mathematical formulas, multi-column layouts, and complex tables. We propose "
            "RLVR-OCR, a reinforcement learning framework that trains OCR models using "
            "verifiable binary rewards derived from automated unit tests. Each reward checks "
            "a specific document property—equation format, table structure, reading order—"
            "without requiring human annotation. Applied to a 7B vision-language model, "
            "RLVR-OCR achieves 82.4 on the olmOCR-Bench benchmark, a +14.2 point improvement "
            "over supervised fine-tuning alone, and demonstrates strong generalization to "
            "out-of-domain document types."
        ),
        body_sections=[
            ("Introduction", LOREM + "\n\n" + LOREM),
            ("Verifiable Reward Design", LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("RLVR-OCR Training", LOREM + "\n\n" + LOREM),
            ("olmOCR-Bench Evaluation", LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Conclusion", LOREM),
        ],
    )


# ─── World Bank-style reports ─────────────────────────────────────────────────

def _wb_report(path: Path, title: str, subtitle: str, year: int,
               exec_summary: list[tuple[str, str]],
               report_no: str, body_chapters: list[tuple[str, str]]):
    doc = SimpleDocTemplate(str(path), pagesize=A4,
                            leftMargin=2.5*cm, rightMargin=2.5*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # ── Cover page ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("THE WORLD BANK GROUP", _style("WBLogo", fontSize=11,
        alignment=TA_CENTER, fontName="Helvetica-Bold", textColor=colors.HexColor("#003087"))))
    story.append(Spacer(1, 2*cm))

    # Blue title bar (simulate with table)
    title_tbl = Table([[Paragraph(title, WB_TITLE)]], colWidths=[16*cm])
    title_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#003087")),
        ("TEXTCOLOR",  (0, 0), (-1, -1), colors.white),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
    ]))
    story.append(title_tbl)
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(subtitle, WB_SUBT))
    story.append(Spacer(1, 4*cm))
    story.append(Paragraph(f"Report No: {report_no}", SMALL))
    story.append(Paragraph(f"© {year} International Bank for Reconstruction and Development / The World Bank", SMALL))
    story.append(Paragraph("1818 H Street NW, Washington, DC 20433, USA", SMALL))
    story.append(PageBreak())

    # ── Table of Contents ───────────────────────────────────────────────────
    story.append(Paragraph("Table of Contents", WB_SECT))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#003087")))
    story.append(Spacer(1, 0.3*cm))
    toc_items = [("Executive Summary", "iii")] + \
                [(f"Chapter {i+1}: {ch[0]}", str(i*8 + 1)) for i, ch in enumerate(body_chapters)]
    for item, pg in toc_items:
        toc_row = Table([[Paragraph(item, BODY), Paragraph(pg, _style("PgNum", fontSize=10,
                          alignment=TA_LEFT, fontName="Helvetica"))]],
                        colWidths=[14*cm, 2*cm])
        story.append(toc_row)
    story.append(PageBreak())

    # ── Executive Summary ───────────────────────────────────────────────────
    story.append(Paragraph("Executive Summary", WB_SECT))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#003087")))
    story.append(Spacer(1, 0.4*cm))

    for subsection_title, subsection_body in exec_summary:
        if subsection_title:
            story.append(Paragraph(subsection_title, _style("ExecSub", fontSize=11,
                leading=15, fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8,
                textColor=colors.HexColor("#003087"))))
        for para in subsection_body.split("\n\n"):
            story.append(Paragraph(para.strip(), WB_BODY))
    story.append(PageBreak())

    # ── Body chapters ────────────────────────────────────────────────────────
    for i, (ch_title, ch_body) in enumerate(body_chapters, 1):
        story.append(Paragraph(f"Chapter {i}: {ch_title}", WB_SECT))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#003087")))
        story.append(Spacer(1, 0.3*cm))
        for para in ch_body.split("\n\n"):
            story.append(Paragraph(para.strip(), WB_BODY))
        if i < len(body_chapters):
            story.append(PageBreak())

    doc.build(story)
    print(f"  Created: {path}")


def create_worldbank_samples(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Report 1: Poverty & Shared Prosperity ────────────────────────────────
    _wb_report(
        path=out_dir / "poverty_shared_prosperity_2024.pdf",
        title="Poverty and Shared Prosperity 2024",
        subtitle="Pathways Out of the Polycrisis: New Evidence on Global Poverty Dynamics",
        year=2024,
        report_no="WB-2024-PSP-001",
        exec_summary=[
            ("Overview", (
                "Global poverty reduction stalled significantly over the 2020–2022 period, "
                "largely due to the convergence of multiple crises—the COVID-19 pandemic, "
                "geopolitical conflicts, and climate-related shocks—collectively described as "
                "a 'polycrisis.' This report presents new evidence on how these compounding "
                "pressures have reshaped poverty dynamics across income groups and regions.\n\n"
                "The number of people living on less than $2.15 per day (2017 PPP) remains at "
                "approximately 700 million as of 2022, a figure that has changed little since "
                "2019. In Sub-Saharan Africa, the poverty headcount actually increased by an "
                "estimated 23 million people between 2019 and 2022, partially offsetting gains "
                "made in South Asia and East Asia & Pacific."
            )),
            ("Key Findings", (
                "This report identifies five key pathways through which countries have "
                "successfully navigated the polycrisis:\n\n"
                "First, countries with strong social protection systems were better able to "
                "cushion households from income shocks. Adaptive social protection—programs "
                "that automatically expand during crises—reduced consumption losses by an "
                "estimated 30–40 percent in countries with pre-existing delivery infrastructure.\n\n"
                "Second, climate resilience investments at the community level show significant "
                "co-benefits for poverty reduction. Evidence from 47 countries shows that "
                "households with access to climate-resilient agricultural extension services "
                "experienced 18 percent lower income volatility during the 2021–2023 droughts.\n\n"
                "Third, digital financial inclusion accelerated recovery for the bottom 40 "
                "percent in countries where mobile money penetration exceeded 60 percent of "
                "the adult population, enabling faster transfer of emergency social assistance."
            )),
            ("Policy Recommendations", (
                "Based on the evidence presented in this report, we recommend four priority "
                "policy areas for governments and development partners:\n\n"
                "1. Invest in adaptive social protection infrastructure before crises occur, "
                "including digital payment systems, beneficiary registries, and automatic "
                "triggers linked to objective crisis indicators.\n\n"
                "2. Accelerate climate adaptation investments in agriculture, water, and "
                "infrastructure, with a focus on the communities most exposed to climate "
                "risk and least able to cope without external support.\n\n"
                "3. Expand access to quality education and health services, which serve as "
                "the primary long-term pathway out of poverty and provide resilience against "
                "future economic shocks.\n\n"
                "4. Strengthen domestic revenue mobilization and fiscal space to finance "
                "social protection and public services sustainably."
            )),
        ],
        body_chapters=[
            ("Measuring Poverty in a Polycrisis Era",
             "Traditional poverty measurement faces new challenges in a world of compounding "
             "crises. This chapter reviews recent advances in near-real-time poverty estimation "
             "using satellite imagery, mobile phone data, and high-frequency household surveys.\n\n"
             + LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Regional Poverty Trends 2019–2024",
             "This chapter presents a systematic review of poverty dynamics across the World "
             "Bank's seven geographic regions, drawing on harmonized household survey data "
             "from 142 countries.\n\n" + LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Social Protection and Crisis Response",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Climate Change and Poverty Intersections",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
        ],
    )

    # ── Report 2: Digital Economy Development ────────────────────────────────
    _wb_report(
        path=out_dir / "digital_economy_development_report.pdf",
        title="World Development Report 2025",
        subtitle="The Digital Transformation Imperative: Harnessing Technology for Inclusive Growth",
        year=2025,
        report_no="WB-2025-WDR-001",
        exec_summary=[
            ("Context and Motivation", (
                "The digital economy is reshaping how goods are produced, how services are "
                "delivered, and how workers earn a living. For developing countries, the "
                "digital transformation represents both an unprecedented opportunity to "
                "leapfrog traditional development pathways and a profound risk of new "
                "forms of exclusion and technological dependency.\n\n"
                "This World Development Report examines the conditions under which digital "
                "technologies contribute to inclusive economic growth, focusing on three "
                "dimensions: (i) access to digital infrastructure, (ii) adoption of digital "
                "tools by firms and workers, and (iii) adaptation of institutions and "
                "regulatory frameworks to the digital economy."
            )),
            ("The Opportunity", (
                "Evidence from 78 developing countries shows that a 10 percentage point "
                "increase in broadband penetration is associated with a 1.4 percentage point "
                "increase in GDP per capita growth, with larger effects in lower-income "
                "countries. The productivity gains from digital adoption in manufacturing and "
                "services sectors are particularly striking: firms that fully digitize their "
                "operations show 22 percent higher total factor productivity on average.\n\n"
                "The platform economy has created new income opportunities for workers in "
                "developing countries. An estimated 154 million workers globally now earn "
                "income through digital labor platforms, with the largest growth occurring in "
                "South Asia and Sub-Saharan Africa. For many, platform work provides the "
                "first access to formal income streams and digital financial services."
            )),
            ("The Risks", (
                "Despite these opportunities, digitalization also poses significant risks "
                "for equitable development. The digital divide remains stark: in low-income "
                "countries, only 26 percent of the population uses the internet, compared to "
                "93 percent in high-income countries. Within countries, gender, income, age, "
                "and geographic gaps in digital access and skills perpetuate and sometimes "
                "amplify existing inequalities.\n\n"
                "Automation threatens to displace workers in sectors such as manufacturing, "
                "data entry, and routine services—sectors that have historically served as "
                "entry points into the formal economy for low-skilled workers. Projections "
                "suggest that up to 85 million jobs in developing countries face high risk "
                "of automation over the next decade, with disproportionate impacts on women "
                "and young workers."
            )),
            ("A Framework for Inclusive Digital Transformation", (
                "This report proposes a three-pillar framework for governments seeking to "
                "harness digital technologies for inclusive growth:\n\n"
                "Pillar 1 — Infrastructure for All: Universal access to affordable, reliable "
                "broadband internet is the foundational prerequisite. This requires regulatory "
                "reform to encourage competition, targeted public investment in underserved "
                "areas, and spectrum management policies that prioritize connectivity.\n\n"
                "Pillar 2 — Digital Skills and Lifelong Learning: Education systems must be "
                "redesigned to equip workers with digital skills at every stage of the "
                "lifecycle. This includes digital literacy programs for adults, coding "
                "education in schools, and reskilling programs for displaced workers.\n\n"
                "Pillar 3 — Adaptive Governance: Regulatory frameworks must balance "
                "innovation with consumer protection, data privacy, and competition. "
                "Governments need capacity to develop and enforce digital regulations while "
                "creating sandboxes for experimentation."
            )),
        ],
        body_chapters=[
            ("The State of the Digital Economy in Developing Countries",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Digital Infrastructure: Connectivity and the Cost of Access",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Digital Firms and the Productivity Dividend",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Labor Markets in the Digital Age",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Data Governance and Digital Public Goods",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
            ("Policy Priorities for Inclusive Digital Transformation",
             LOREM + "\n\n" + LOREM + "\n\n" + LOREM + "\n\n" + LOREM),
        ],
    )


if __name__ == "__main__":
    base = Path(__file__).parent / "samples"
    print("Creating arxiv sample papers...")
    create_arxiv_samples(base / "arxiv")
    print("\nCreating World Bank sample reports...")
    create_worldbank_samples(base / "worldbank")
    print("\nDone!")
