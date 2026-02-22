# OCR Comparison Framework — Process Documentation

This document explains the full process: how documents are collected, how OCR
is applied, how results are evaluated, and how to extend the system.

---

## 1. Overview

The framework compares **25 OCR methods** across three tasks:

```
Task 1: pdf_text   — Extract text from PDF files
Task 2: image_text — Extract text from images (PNG/JPG)
Task 3: pdf_assets — Extract tables and embedded images from PDFs
```

It also includes two **domain-specific tasks**:

```
Task A: affiliations      — Extract author affiliations from academic paper page 1
Task B: executive_summary — Find and extract executive summary from reports
```

---

## 2. Document Collection

### 2.1 How samples were sourced

The framework ships with **5 synthetic-but-realistic test documents** generated
by `ocr/benchmarks/create_samples.py`, which uses the `reportlab` library to
produce PDFs matching the structure of real documents:

#### Arxiv-style academic papers (`benchmarks/samples/arxiv/`)

| File | Description | Authors | Affiliations |
|---|---|---|---|
| `vlm_ocr_benchmark_2025.pdf` | Vision-Language Model OCR paper | Alice Chen et al. | Stanford, Google DeepMind, KAIST, MPI |
| `multilingual_doc_understanding.pdf` | Multilingual document understanding | François Dubois et al. | INRIA Paris, U. Tokyo, IIT Bombay, La Sapienza, ETH, Tsinghua |
| `rl_ocr_training.pdf` | Reinforcement learning for OCR | James O'Brien et al. | Allen AI, UW, UC Berkeley |

Each paper has:
- Title, author list with superscript affiliation keys on **page 1**
- Per-key affiliation lines (institution, department, address, country)
- Contact email addresses
- Multi-page body (abstract + 4–6 sections)

#### World Bank-style reports (`benchmarks/samples/worldbank/`)

| File | Description | Executive Summary sections |
|---|---|---|
| `poverty_shared_prosperity_2024.pdf` | Global poverty report | Overview, Key Findings, Policy Recommendations |
| `digital_economy_development_report.pdf` | World Development Report 2025 | Context, Opportunity, Risks, Framework |

Each report has:
- Cover page with World Bank branding
- Table of Contents
- **Executive Summary** section (clearly headed)
- 4–6 body chapters

### 2.2 Adding your own documents

```
ocr/benchmarks/samples/
├── arxiv/         ← Drop real arxiv PDFs here for affiliation extraction
├── worldbank/     ← Drop World Bank reports here for exec summary extraction
├── pdf_text/      ← Any PDFs for general text extraction benchmark
├── images/        ← PNG/JPG images for image OCR benchmark
└── pdf_with_tables/ ← PDFs with tables for asset extraction benchmark
```

Optionally provide ground truth:

```
ocr/benchmarks/ground_truth/
├── paper_name.txt              ← Expected text (for CER/WER scoring)
└── paper_name_tables.json      ← Expected tables [{markdown, rows}]
```

To get real World Bank reports: https://openknowledge.worldbank.org/
To get real arxiv papers: https://arxiv.org/pdf/PAPER_ID

---

## 3. OCR Method Architecture

### 3.1 Unified interface

Every method inherits from `BaseOCR` (`ocr/methods/base.py`) and implements:

```python
class BaseOCR:
    def extract_pdf_text(self, pdf_path: Path) -> OCRResult
    def extract_image_text(self, image_path: Path) -> OCRResult
    def extract_pdf_assets(self, pdf_path: Path) -> OCRResult
```

`OCRResult` is a dataclass capturing:

| Field | Type | Description |
|---|---|---|
| `text` | `str` | Extracted text |
| `tables` | `list[dict]` | Tables with `{page, markdown, rows}` |
| `images` | `list[dict]` | Image metadata `{page, description, size_bytes}` |
| `elapsed_s` | `float` | Wall-clock seconds |
| `cost_usd` | `float` | Estimated cost |
| `pages` | `int` | Pages processed |
| `error` | `str\|None` | Set if method failed |

### 3.2 Method categories

```
ocr/methods/
├── local_packages/    tesseract, easyocr, paddleocr, surya, doctr
│                      → pip install, runs on CPU/GPU, free
├── pdf_extractors/    pymupdf, pdfplumber, pypdf, marker
│                      → for digital PDFs with embedded text layer
├── ollama_models/     qwen2.5vl, glm-ocr, minicpm-v, deepseek-ocr/2,
│                      llama3.2-vision, gemma3
│                      → local VLMs via Ollama HTTP API
├── apis/              mistral-ocr, claude, gpt-4o, gemini, azure, textract
│                      → cloud APIs, require API keys, metered billing
└── specialized/       camelot, tabula, img2table, unstructured,
                       mineru, docling
                       → purpose-built for tables/figures/pipelines
```

---

## 4. Task A: Affiliation Extraction

**File:** `ocr/tasks/affiliations.py`

### 4.1 Process

```
PDF → page 1 text → regex pattern matching → structured output
```

**Step 1: Extract page 1 text** using the chosen method (PyMuPDF by default,
since it is fast and handles digital PDFs perfectly).

**Step 2: Pattern matching** identifies:

| Pattern | What it detects |
|---|---|
| `AFFIL_KEYWORDS` | Lines containing "University", "Institute", "INRIA", "MIT", country names, etc. |
| `EMAIL_RE` | `name@domain.tld` patterns |
| `ADDRESS_RE` | Street addresses, zip codes |
| `MARKER_RE` | Superscript keys (`1`, `2,3`, `*`) between author names and affiliations |

**Step 3: Output structure**

```json
{
  "authors_line": "Alice Chen, Bob Kumar, Carol Li, ...",
  "institutions": [
    "1,2 Department of Computer Science, Stanford University, Stanford, CA 94305, USA",
    "2 Google DeepMind, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
    "3 KAIST AI Graduate School, Daejeon 34141, Republic of Korea"
  ],
  "emails": [
    "achen@cs.stanford.edu",
    "bkumar@cs.stanford.edu",
    "carol.li@deepmind.google.com"
  ],
  "raw_affiliation_block": "..."
}
```

### 4.2 Running

```bash
# Default: all arxiv samples, PyMuPDF only
python -m ocr.tasks.affiliations

# Specific PDF
python -m ocr.tasks.affiliations --pdf path/to/paper.pdf

# Multiple methods (when dependencies available)
python -m ocr.tasks.affiliations --methods pymupdf pdfplumber tesseract

# Save results
python -m ocr.tasks.affiliations --output ocr/results/tasks/affiliations.json
```

### 4.3 Sample output

```
======================================================================
AFFILIATION EXTRACTION: vlm_ocr_benchmark_2025.pdf
======================================================================

--- PYMUPDF ---
  Authors:      Alice Chen, Bob Kumar, Carol Li, David Park, Elena Müller
  Institutions (5):
    • 1,2 Department of Computer Science, Stanford University, Stanford, CA 94305, USA
    • 1   Department of Computer Science, Stanford University, Stanford, CA 94305, USA
    • 2   Google DeepMind, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA
    • 3   KAIST AI Graduate School, Daejeon 34141, Republic of Korea
    • 4   Max Planck Institute for Informatics, 66123 Saarbrücken, Germany
  Emails: achen@cs.stanford.edu, bkumar@cs.stanford.edu, carol.li@deepmind.google.com, ...
```

### 4.4 When to use which OCR method for affiliations

| Document type | Recommended method | Why |
|---|---|---|
| Digital PDF (e-born) | `pymupdf` | Instant, perfect character accuracy |
| Scanned paper | `paddleocr` or `surya` | Best OCR for scanned pages |
| Image of paper page | `qwen2.5vl:7b` (Ollama) | Top VLM for document image OCR |
| Need structured JSON | `claude-3-5-sonnet` | Reason about affiliation structure |

For scanned or image-only papers, the VLM-based methods (Ollama or API) can
be combined with the same pattern matcher by running:

```python
from ocr.methods.ollama_models.qwen25vl import Qwen25VLMethod
from ocr.tasks.affiliations import extract_affiliations_from_text

method = Qwen25VLMethod(size="7b")
result = method.extract_image_text(Path("scanned_paper.png"))
affiliations = extract_affiliations_from_text(result.text)
```

---

## 5. Task B: Executive Summary Extraction

**File:** `ocr/tasks/executive_summary.py`

### 5.1 Process

```
PDF → full text (all pages) → heading detection → section boundary → excerpt
```

**Step 1: Extract full document text** (all pages, concatenated with `\n`).

**Step 2: Heading detection** via `EXEC_SUMMARY_RE` — a regex that matches:

| Pattern | Matches |
|---|---|
| `executive summary` | English standard |
| `executive sum` | Abbreviated |
| `résumé exécutif` | French |
| `zusammenfassung` | German |
| `resumen ejecutivo` | Spanish |
| `key findings / messages / points` | Alternative headings |
| `main overview`, `highlights` | Informal equivalents |

**Step 3: Section boundary** — `NEXT_SECTION_RE` finds the next major heading
("Chapter 1", "Introduction", "Background") to delimit where the exec summary ends.

**Step 4: Output**

```json
{
  "found": true,
  "heading": "Executive Summary",
  "text": "Global poverty reduction stalled significantly...",
  "start_char": 1823,
  "char_count": 3847,
  "method_note": "heading match"
}
```

### 5.2 Running

```bash
# Default: all worldbank samples
python -m ocr.tasks.executive_summary

# Specific report
python -m ocr.tasks.executive_summary --pdf report.pdf

# Longer preview
python -m ocr.tasks.executive_summary --snippet 1200

# Save results
python -m ocr.tasks.executive_summary --output ocr/results/tasks/exec_summary.json
```

### 5.3 Sample output

```
======================================================================
EXECUTIVE SUMMARY EXTRACTION: poverty_shared_prosperity_2024.pdf
======================================================================

--- PYMUPDF ---
  Pages read:   7     Total chars:  7,719
  Found:        YES
  Heading:      "Executive Summary"
  Section size: 3,847 chars

  -- First 600 chars of Executive Summary --
  Overview
  Global poverty reduction stalled significantly over the 2020–2022 period,
  largely due to the convergence of multiple crises—the COVID-19 pandemic,
  geopolitical conflicts, and climate-related shocks—collectively described
  as a 'polycrisis.' This report presents new evidence on how these
  compounding pressures have reshaped poverty dynamics across income groups
  and regions.

  Key Findings
  This report identifies five key pathways through which countries have
  successfully navigated the polycrisis...
```

### 5.4 Extending to other report structures

Some reports use different conventions:

| Convention | How to handle |
|---|---|
| "Foreword" instead of "Executive Summary" | Add pattern to `EXEC_SUMMARY_RE` |
| Summary at very start (no heading) | The first-page fallback triggers automatically |
| Multi-language reports | Patterns already cover EN/FR/DE/ES |
| Scanned reports | Use `surya` or `mineru` for text extraction first |

---

## 6. General Benchmark Evaluation

### 6.1 Running the full benchmark

```bash
# All free/local methods on all sample types
python -m ocr.compare --only-free --no-ollama

# Specific methods
python -m ocr.compare --methods pymupdf paddleocr surya mistral-ocr

# Single task
python -m ocr.compare --task pdf_text --only-free
```

### 6.2 Evaluation metrics

#### Text quality (Task 1 & 2)

| Metric | Formula | Direction |
|---|---|---|
| CER | `edit_distance(pred_chars, ref_chars) / len(ref_chars)` | ↓ lower better |
| WER | `edit_distance(pred_words, ref_words) / len(ref_words)` | ↓ lower better |
| Character Similarity | `1 - CER` | ↑ higher better |
| BLEU-1 | `precision of unigrams in pred vs. ref` | ↑ higher better |

#### Table quality (Task 3)

| Metric | Description | Direction |
|---|---|---|
| Cell Accuracy | Fraction of cells matching reference (aligned by position) | ↑ |
| Structure Score | Jaccard similarity of table shape (rows × cols) | ↑ |

#### Performance

| Metric | Description | Direction |
|---|---|---|
| Seconds/page | Wall-clock time ÷ page count | ↓ |
| Cost/page | USD ÷ page count | ↓ |

### 6.3 Output format

Results are saved as:

```
ocr/results/raw/benchmark_<timestamp>.json    ← per-sample raw results
ocr/results/reports/report_<timestamp>.md     ← aggregated markdown report
ocr/results/tasks/affiliations_results.json   ← affiliation task results
ocr/results/tasks/executive_summary_results.json
```

The JSON structure per sample:

```json
{
  "method": "pymupdf",
  "task": "pdf_text",
  "sample": "paper.pdf",
  "text_length": 12500,
  "elapsed_s": 0.08,
  "cost_usd": 0.0,
  "pages": 8,
  "seconds_per_page": 0.01,
  "cost_per_page": 0.0,
  "error": null,
  "text_scores": {
    "cer": 0.0312,
    "wer": 0.0451,
    "char_similarity": 0.9688,
    "bleu1": 0.9123
  },
  "table_scores": {
    "cell_accuracy": 0.94,
    "structure_score": 1.0
  }
}
```

---

## 7. Decision Guide

### Which method to use?

```
Is the PDF digitally created (not scanned)?
  YES → Use pymupdf (fastest, free, perfect accuracy for native PDFs)
    Need tables?     → Also run pdfplumber or camelot
    Need figures?    → Also run pymupdf (extracts embedded images)
    Need markdown?   → Use marker or mineru

  NO (scanned PDF or photo of document):
    Have GPU?        → surya or paddleocr (best open-source OCR)
    No GPU, free?    → paddleocr (CPU mode) or tesseract
    Need best quality, don't mind API cost?
                     → mistral-ocr-3 ($1/1K pages, SOTA tables)
                     → claude-3-5-haiku ($0.64/1K pages est.)
                     → gemini-2.0-flash ($0.07/1K pages est.)
    Have Ollama installed?
                     → qwen2.5vl:7b (best OCR quality, DocVQA 95.7)
                     → deepseek-ocr2 (high throughput, 2500 tok/s)
```

### Price vs. quality summary

| Tier | Method | Approx $/1K pages | OCR Quality |
|---|---|---|---|
| Free, instant | pymupdf (digital PDFs) | $0 | Perfect (digital) |
| Free, fast CPU | paddleocr | $0 | ★★★★ |
| Free, local GPU | surya | $0 | ★★★★★ |
| Free, local GPU | qwen2.5vl:7b (Ollama) | $0 | ★★★★★ |
| Cheapest API | gemini-2.0-flash | ~$0.07 | ★★★★ |
| Best price/quality | mistral-ocr-3 | $1–2 | ★★★★★ |
| Best reasoning | claude-3-5-sonnet | ~$5 | ★★★★★ |
| Enterprise | azure / textract | $1.50–15 | ★★★★ |

---

## 8. File Index

```
ocr/
├── PROCESS.md                    ← This file
├── README.md                     ← Quick-start guide
├── requirements.txt              ← All dependencies
├── compare.py                    ← Main benchmark CLI
├── report.py                     ← Report generation
│
├── methods/                      ← 25 OCR method implementations
│   ├── base.py                   ← BaseOCR + OCRResult
│   ├── local_packages/           ← tesseract, easyocr, paddleocr, surya, doctr
│   ├── pdf_extractors/           ← pymupdf, pdfplumber, pypdf, marker
│   ├── ollama_models/            ← qwen2.5vl, glm-ocr, minicpm-v, deepseek-ocr/2,
│   │                                llama3.2-vision, gemma3
│   ├── apis/                     ← mistral-ocr, claude, gpt-4o, gemini, azure, textract
│   └── specialized/              ← camelot, tabula, img2table, unstructured, mineru, docling
│
├── evaluators/                   ← Scoring
│   ├── text_metrics.py           ← CER, WER, BLEU-1, character similarity
│   ├── table_metrics.py          ← Cell accuracy, structure score
│   └── benchmark_runner.py       ← Orchestration, aggregation
│
├── tasks/                        ← Domain-specific extraction
│   ├── affiliations.py           ← Author affiliation extractor
│   └── executive_summary.py      ← Executive summary finder
│
├── benchmarks/
│   ├── create_samples.py         ← Generate synthetic test PDFs
│   ├── samples/
│   │   ├── arxiv/                ← 3 academic papers (affiliations task)
│   │   ├── worldbank/            ← 2 World Bank reports (exec summary task)
│   │   ├── pdf_text/             ← General PDF text samples
│   │   ├── images/               ← Image OCR samples
│   │   └── pdf_with_tables/      ← PDF asset extraction samples
│   └── ground_truth/             ← Reference text/tables for scoring
│
└── results/
    ├── raw/                      ← benchmark_<ts>.json
    ├── reports/                  ← report_<ts>.md
    └── tasks/                    ← affiliations_results.json
                                     executive_summary_results.json
```

---

## 9. Extending the Framework

### Add a new OCR method

1. Create `ocr/methods/<category>/my_method.py` inheriting `BaseOCR`
2. Implement `_extract_pdf_text`, `_extract_image_text`, `_extract_pdf_assets`
3. Register it in `ocr/compare.py` under `_build_method_registry()`

```python
# ocr/methods/local_packages/my_method.py
from ..base import BaseOCR, OCRResult

class MyOCRMethod(BaseOCR):
    name = "my-ocr"
    category = "local_package"
    supports_pdf_text = True
    supports_image_text = True

    def _extract_image_text(self, image_path):
        import my_ocr_lib
        text = my_ocr_lib.read(str(image_path))
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
        )
```

### Add a new domain task

Create `ocr/tasks/my_task.py` following the pattern in `affiliations.py` or
`executive_summary.py`:

1. Define a `run_extraction(pdf_path, methods)` function
2. Define a `print_results(pdf_path, results)` function
3. Add a `main()` with argparse so it's runnable as `python -m ocr.tasks.my_task`
