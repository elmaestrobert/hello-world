# OCR Comparison Framework

A comprehensive benchmark comparing OCR methods across three tasks:

| Task | Description |
|---|---|
| **pdf_text** | Extract text from PDF files |
| **image_text** | Extract text from image files (PNG/JPG/etc.) |
| **pdf_assets** | Extract tables and embedded images from PDFs |

Methods are evaluated on **quality** (CER, WER, character similarity), **speed** (seconds/page), and **cost** (USD/page).

---

## Methods Covered

### Local Packages (free, no API key)

| Method | Best For | Notes |
|---|---|---|
| `tesseract` | Simple printed text | Requires `tesseract` binary |
| `easyocr` | Multilingual, scene text | 80+ languages |
| `paddleocr` | High accuracy, fast | 80+ languages, GPU optional |
| `surya` | Complex layouts | 90+ languages, GPU preferred |
| `doctr` | Structured documents | GPU preferred |

### PDF-Native Extractors (free, no API key)

| Method | Best For | Notes |
|---|---|---|
| `pymupdf` | Digital PDFs, fast | Also extracts images & tables |
| `pdfplumber` | Precise table extraction | Character-level positioning |
| `pypdf` | Simple digital PDFs | Pure Python, no C deps |
| `marker` | Scientific PDFs, markdown | GPU preferred; handles math/tables |

### Ollama Local Vision Models (free, requires Ollama)

| Method | Model | Best For | Notes |
|---|---|---|---|
| `qwen2.5vl:7b` | Qwen2.5-VL-7B | OCR, DocVQA (95.7) | Requires Ollama ≥ 0.7.0 |
| `qwen2.5vl:3b` | Qwen2.5-VL-3B | Edge/fast OCR | Compact |
| `glm-ocr` | GLM-OCR | Complex documents | Multilingual, CN/EN |
| `minicpm-v` | MiniCPM-V 2.6 | High-res OCR | Beats GPT-4o on OCRBench |
| `llama3.2-vision` | Llama 3.2 Vision 11B | General vision | Good but trails Qwen |
| `gemma3` | Gemma 3 12B | General vision | Google open model |
| `deepseek-ocr` | DeepSeek-OCR | High-throughput OCR | 3B params (570M active MoE); needs Ollama >= 0.13.0 |
| `deepseek-ocr2` | DeepSeek-OCR 2 | Token-efficient OCR | Jan 2026; Qwen2-0.5B vision encoder, "visual causal flow" |

### Cloud APIs (requires API key)

| Method | API | $/1K pages | $/1K pages (batch) | Notes |
|---|---|---|---|---|
| `mistral-ocr` | Mistral OCR 3 | $2.00 | $1.00 | SOTA tables (96.6%), HW (88.9%) |
| `claude-3-5-sonnet` | Anthropic | ~$4.80* | — | Best reasoning, imperfect image transcription |
| `claude-3-5-haiku` | Anthropic | ~$1.28* | — | Cheap Claude option |
| `gpt-4o` | OpenAI | ~$3.00* | — | Strong general vision |
| `gpt-4o-mini` | OpenAI | ~$0.18* | — | Very cheap, good quality |
| `gemini-2.0-flash` | Google | ~$0.13* | — | Cheapest API option, 1M context |
| `azure` | Azure Doc. Intelligence | $1.50 | — | Enterprise, forms/invoices |
| `textract` | AWS Textract | $1.50 (text) | $15 (tables) | AWS-native |

*Estimated based on ~1600 tokens/page for vision models

### Specialized Table/Figure Extraction (free)

| Method | Best For | Notes |
|---|---|---|
| `camelot` | Ruled-line tables | `lattice` or `stream` flavor |
| `tabula` | Simple tables | Requires Java JRE |
| `img2table` | Scanned doc tables | Uses tesseract/easyocr for cells |
| `unstructured` | Mixed document types | PDF, DOCX, HTML, email |
| `mineru` | PDF-to-Markdown for RAG | **90.67 OmniDocBench** — top open-source; Apache 2.0 |
| `docling` | Enterprise documents | IBM Research; 97.9% table accuracy; MIT license |

---

## Setup

### 1. Install dependencies

```bash
# Full install (all methods)
pip install -r ocr/requirements.txt

# Minimal install (only free/local methods)
pip install PyMuPDF pypdf Pillow pytesseract easyocr paddleocr pdfplumber tabulate

# For Ollama models: install Ollama and pull models
ollama pull qwen2.5vl:7b
ollama pull glm-ocr
ollama pull minicpm-v
ollama pull llama3.2-vision:11b
```

### 2. Set API keys (for cloud methods)

```bash
export ANTHROPIC_API_KEY="..."
export MISTRAL_API_KEY="..."
export OPENAI_API_KEY="..."
export GOOGLE_API_KEY="..."
export AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT="https://..."
export AZURE_DOCUMENT_INTELLIGENCE_KEY="..."
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
```

### 3. Add test samples

Place files in the appropriate subdirectory:

```
ocr/benchmarks/samples/
├── pdf_text/         ← PDFs for text extraction
├── images/           ← Images (PNG/JPG) for text extraction
└── pdf_with_tables/  ← PDFs with tables for asset extraction

ocr/benchmarks/ground_truth/
├── sample1.txt               ← Ground truth text for sample1.pdf
└── sample1_tables.json       ← Ground truth tables (list of {markdown, rows})
```

---

## Usage

```bash
# Run all available methods on all samples
python -m ocr.compare

# Run specific methods
python -m ocr.compare --methods tesseract paddleocr surya mistral-ocr

# Run only free/local methods (skip APIs)
python -m ocr.compare --only-free

# Run only a specific task
python -m ocr.compare --task pdf_text

# Skip Ollama methods (if Ollama is not running)
python -m ocr.compare --no-ollama

# Generate report from existing results
python -m ocr.compare --report ocr/results/raw/benchmark_12345.json
```

---

## Output

Results are saved to:
- `ocr/results/raw/benchmark_<timestamp>.json` – raw per-sample results
- `ocr/results/reports/report_<timestamp>.md` – formatted markdown report

### Metrics

| Metric | Direction | Description |
|---|---|---|
| CER | ↓ lower better | Character Error Rate |
| WER | ↓ lower better | Word Error Rate |
| Similarity | ↑ higher better | 1 - CER |
| BLEU-1 | ↑ higher better | Unigram precision |
| Cell Accuracy | ↑ higher better | Table cell match rate |
| Structure Score | ↑ higher better | Table shape similarity |
| Sec/page | ↓ lower better | Throughput |
| $/page | ↓ lower better | Cost |

---

## Known Benchmarks (2025–2026)

| Method | Accuracy | DocVQA | Table Acc | Source |
|---|---|---|---|---|
| surya | 97.7% | — | — | Invoice benchmark |
| qwen2.5vl:7b | — | 95.7 | — | Official Qwen2.5-VL paper |
| minicpm-v 2.6 | SOTA* | — | — | OCRBench, beats GPT-4o |
| mistral-ocr-3 | 94.9% | — | 96.6% | Mistral internal |
| azure-doc-intel | 89.5% | — | — | Mistral benchmark |
| paddleocr | 92.96% | — | — | Nanonets benchmark |
| tesseract | 87.74% | — | — | Invoice benchmark |
| aws-textract | — | — | 84.8% | Mistral table benchmark |
| olmOCR-2 | — | — | 82.4 | olmOCR-Bench |
| marker | — | — | 76.1 | olmOCR-Bench |
| **mineru2.5** | **90.67** | — | — | **OmniDocBench CVPR 2025 — best open-source** |
| docling | — | 97.9%* | — | Enterprise table benchmark (IBM Research) |
| deepseek-ocr | ~97% | — | — | At <10x image compression |

---

## Project Structure

```
ocr/
├── README.md
├── requirements.txt
├── __init__.py
├── compare.py                  ← Main entry point
├── report.py                   ← Report generation
├── methods/
│   ├── base.py                 ← BaseOCR class + OCRResult dataclass
│   ├── local_packages/         ← tesseract, easyocr, paddleocr, surya, doctr
│   ├── pdf_extractors/         ← pymupdf, pdfplumber, pypdf, marker
│   ├── ollama_models/          ← qwen2.5vl, glm-ocr, minicpm-v, llama3.2-vision, gemma3, deepseek-ocr/2
│   ├── apis/                   ← mistral-ocr-3, claude, gpt-4o, gemini, azure, textract
│   └── specialized/            ← camelot, tabula, img2table, unstructured, mineru, docling
├── evaluators/
│   ├── text_metrics.py         ← CER, WER, BLEU-1
│   ├── table_metrics.py        ← Cell accuracy, structure score
│   └── benchmark_runner.py     ← Orchestration
└── benchmarks/
    ├── samples/                ← Add your test files here
    └── ground_truth/           ← Add ground truth text/tables here
```
