"""
OCR Comparison – main entry point.

Usage examples:
  # Run all methods on sample files in benchmarks/samples/
  python -m ocr.compare

  # Run specific methods and tasks
  python -m ocr.compare --methods tesseract paddleocr mistral-ocr --task pdf_text

  # Run with custom sample directory
  python -m ocr.compare --samples /path/to/samples --task image_text

  # Generate report from existing results file
  python -m ocr.compare --report results/raw/benchmark_12345.json

Environment variables for API keys:
  ANTHROPIC_API_KEY, OPENAI_API_KEY, MISTRAL_API_KEY,
  GOOGLE_API_KEY, AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
  AZURE_DOCUMENT_INTELLIGENCE_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Resolve package root
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ocr.evaluators.benchmark_runner import BenchmarkRunner, BenchmarkSample
from ocr.report import generate_report, print_summary_table


# ─── Method registry ────────────────────────────────────────────────────────

def _build_method_registry() -> dict:
    """Return a dict of name -> (factory_fn, required_pkg)."""
    registry = {}

    # ---- Local packages ----
    def _make_tesseract():
        from ocr.methods.local_packages.tesseract_ocr import TesseractOCR
        return TesseractOCR()

    def _make_easyocr():
        from ocr.methods.local_packages.easyocr_method import EasyOCRMethod
        return EasyOCRMethod()

    def _make_paddleocr():
        from ocr.methods.local_packages.paddleocr_method import PaddleOCRMethod
        return PaddleOCRMethod()

    def _make_surya():
        from ocr.methods.local_packages.surya_method import SuryaOCRMethod
        return SuryaOCRMethod()

    def _make_doctr():
        from ocr.methods.local_packages.doctr_method import DocTRMethod
        return DocTRMethod()

    # ---- PDF extractors ----
    def _make_pymupdf():
        from ocr.methods.pdf_extractors.pymupdf_method import PyMuPDFMethod
        return PyMuPDFMethod()

    def _make_pdfplumber():
        from ocr.methods.pdf_extractors.pdfplumber_method import PDFPlumberMethod
        return PDFPlumberMethod()

    def _make_pypdf():
        from ocr.methods.pdf_extractors.pypdf_method import PyPDFMethod
        return PyPDFMethod()

    def _make_marker():
        from ocr.methods.pdf_extractors.marker_method import MarkerMethod
        return MarkerMethod()

    # ---- Ollama local models ----
    def _make_qwen25vl_7b():
        from ocr.methods.ollama_models.qwen25vl import Qwen25VLMethod
        return Qwen25VLMethod(size="7b")

    def _make_qwen25vl_3b():
        from ocr.methods.ollama_models.qwen25vl import Qwen25VLMethod
        return Qwen25VLMethod(size="3b")

    def _make_glm_ocr():
        from ocr.methods.ollama_models.glm_ocr import GLMOCRMethod
        return GLMOCRMethod()

    def _make_minicpm_v():
        from ocr.methods.ollama_models.minicpm_v import MiniCPMVMethod
        return MiniCPMVMethod()

    def _make_llama32_vision():
        from ocr.methods.ollama_models.llama32_vision import Llama32VisionMethod
        return Llama32VisionMethod(size="11b")

    def _make_gemma3():
        from ocr.methods.ollama_models.gemma3_vision import Gemma3VisionMethod
        return Gemma3VisionMethod(size="12b")

    def _make_deepseek_ocr():
        from ocr.methods.ollama_models.deepseek_ocr import DeepSeekOCRMethod
        return DeepSeekOCRMethod(version=1)

    def _make_deepseek_ocr2():
        from ocr.methods.ollama_models.deepseek_ocr import DeepSeekOCRMethod
        return DeepSeekOCRMethod(version=2)

    # ---- Cloud APIs ----
    def _make_mistral_ocr():
        from ocr.methods.apis.mistral_ocr import MistralOCRMethod
        return MistralOCRMethod()

    def _make_claude_sonnet():
        from ocr.methods.apis.anthropic_ocr import AnthropicOCRMethod
        return AnthropicOCRMethod(model="claude-3-5-sonnet-latest")

    def _make_claude_haiku():
        from ocr.methods.apis.anthropic_ocr import AnthropicOCRMethod
        return AnthropicOCRMethod(model="claude-3-5-haiku-latest")

    def _make_gpt4o():
        from ocr.methods.apis.openai_ocr import OpenAIOCRMethod
        return OpenAIOCRMethod(model="gpt-4o")

    def _make_gpt4o_mini():
        from ocr.methods.apis.openai_ocr import OpenAIOCRMethod
        return OpenAIOCRMethod(model="gpt-4o-mini")

    def _make_gemini_flash():
        from ocr.methods.apis.gemini_ocr import GeminiOCRMethod
        return GeminiOCRMethod(model="gemini-2.0-flash")

    def _make_azure():
        from ocr.methods.apis.azure_ocr import AzureDocIntelligenceMethod
        return AzureDocIntelligenceMethod()

    def _make_textract():
        from ocr.methods.apis.textract_ocr import TextractOCRMethod
        return TextractOCRMethod()

    # ---- Specialized ----
    def _make_camelot():
        from ocr.methods.specialized.camelot_method import CamelotMethod
        return CamelotMethod(flavor="lattice")

    def _make_tabula():
        from ocr.methods.specialized.tabula_method import TabulaMethod
        return TabulaMethod()

    def _make_img2table():
        from ocr.methods.specialized.img2table_method import Img2TableMethod
        return Img2TableMethod()

    def _make_unstructured():
        from ocr.methods.specialized.unstructured_method import UnstructuredMethod
        return UnstructuredMethod()

    def _make_mineru():
        from ocr.methods.specialized.mineru_method import MinerUMethod
        return MinerUMethod()

    def _make_docling():
        from ocr.methods.specialized.docling_method import DoclingMethod
        return DoclingMethod()

    registry = {
        # Local packages
        "tesseract":         _make_tesseract,
        "easyocr":           _make_easyocr,
        "paddleocr":         _make_paddleocr,
        "surya":             _make_surya,
        "doctr":             _make_doctr,
        # PDF extractors
        "pymupdf":           _make_pymupdf,
        "pdfplumber":        _make_pdfplumber,
        "pypdf":             _make_pypdf,
        "marker":            _make_marker,
        # Ollama
        "qwen2.5vl:7b":     _make_qwen25vl_7b,
        "qwen2.5vl:3b":     _make_qwen25vl_3b,
        "glm-ocr":           _make_glm_ocr,
        "minicpm-v":         _make_minicpm_v,
        "llama3.2-vision":   _make_llama32_vision,
        "gemma3":            _make_gemma3,
        "deepseek-ocr":      _make_deepseek_ocr,
        "deepseek-ocr2":     _make_deepseek_ocr2,
        # Cloud APIs
        "mistral-ocr":       _make_mistral_ocr,
        "claude-3-5-sonnet": _make_claude_sonnet,
        "claude-3-5-haiku":  _make_claude_haiku,
        "gpt-4o":            _make_gpt4o,
        "gpt-4o-mini":       _make_gpt4o_mini,
        "gemini-2.0-flash":  _make_gemini_flash,
        "azure":             _make_azure,
        "textract":          _make_textract,
        # Specialized
        "camelot":           _make_camelot,
        "tabula":            _make_tabula,
        "img2table":         _make_img2table,
        "unstructured":      _make_unstructured,
        "mineru":            _make_mineru,
        "docling":           _make_docling,
    }
    return registry


# ─── Sample discovery ────────────────────────────────────────────────────────

def _discover_samples(samples_dir: Path, task: str | None) -> list[BenchmarkSample]:
    """Auto-discover sample files under benchmarks/samples/."""
    samples = []
    suffixes_pdf = {".pdf"}
    suffixes_img = {".png", ".jpg", ".jpeg", ".tiff", ".tif", ".bmp", ".webp"}

    gt_dir = samples_dir.parent.parent / "benchmarks" / "ground_truth"

    def _load_gt(filename: str) -> tuple[str, list[dict]]:
        gt_text_path = gt_dir / (filename + ".txt")
        gt_table_path = gt_dir / (filename + "_tables.json")
        gt_text = gt_text_path.read_text(encoding="utf-8") if gt_text_path.exists() else ""
        gt_tables = []
        if gt_table_path.exists():
            gt_tables = json.loads(gt_table_path.read_text())
        return gt_text, gt_tables

    search_root = samples_dir if samples_dir.is_dir() else (
        Path(__file__).parent / "benchmarks" / "samples"
    )

    if task in (None, "pdf_text", "pdf_assets"):
        for subdir in ["pdf_text", "pdf_with_tables", ""]:
            d = search_root / subdir if subdir else search_root
            if not d.exists():
                continue
            for f in sorted(d.glob("*.pdf")):
                t = "pdf_assets" if "table" in subdir else "pdf_text"
                if task and task != t:
                    t = task
                gt_text, gt_tables = _load_gt(f.stem)
                samples.append(BenchmarkSample(
                    path=f, task=t,
                    ground_truth_text=gt_text,
                    ground_truth_tables=gt_tables,
                ))

    if task in (None, "image_text"):
        for subdir in ["images", ""]:
            d = search_root / subdir if subdir else search_root
            if not d.exists():
                continue
            for f in sorted(d.iterdir()):
                if f.suffix.lower() in suffixes_img:
                    gt_text, _ = _load_gt(f.stem)
                    samples.append(BenchmarkSample(
                        path=f, task="image_text",
                        ground_truth_text=gt_text,
                    ))

    return samples


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    registry = _build_method_registry()
    all_method_names = list(registry.keys())

    parser = argparse.ArgumentParser(
        description="OCR method comparison benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--methods", nargs="+", default=None,
        choices=all_method_names + ["all"],
        metavar="METHOD",
        help=f"Methods to run. Choices: {', '.join(all_method_names)}. Default: all available.",
    )
    parser.add_argument(
        "--task", choices=["pdf_text", "image_text", "pdf_assets", "all"],
        default="all",
        help="Task to benchmark. Default: all",
    )
    parser.add_argument(
        "--samples", type=Path, default=None,
        help="Directory containing sample files. Default: ocr/benchmarks/samples/",
    )
    parser.add_argument(
        "--output", type=Path, default=Path("ocr/results/raw"),
        help="Directory to save raw results JSON. Default: ocr/results/raw/",
    )
    parser.add_argument(
        "--report", type=Path, default=None,
        help="Generate report from existing JSON results file (skip running OCR)",
    )
    parser.add_argument(
        "--no-ollama", action="store_true",
        help="Skip Ollama-based methods (useful when Ollama is not running)",
    )
    parser.add_argument(
        "--only-free", action="store_true",
        help="Only run free/local methods (skip all cloud APIs)",
    )
    args = parser.parse_args()

    # ---- Report mode ----
    if args.report:
        data = json.loads(args.report.read_text())
        report_path = generate_report(data, output_dir=Path("ocr/results/reports"))
        print(f"Report generated: {report_path}")
        return

    # ---- Select methods ----
    selected_names = args.methods or all_method_names
    if "all" in selected_names:
        selected_names = all_method_names

    ollama_names = {"qwen2.5vl:7b", "qwen2.5vl:3b", "glm-ocr", "minicpm-v",
                    "llama3.2-vision", "gemma3", "deepseek-ocr", "deepseek-ocr2"}
    api_names = {"mistral-ocr", "claude-3-5-sonnet", "claude-3-5-haiku",
                 "gpt-4o", "gpt-4o-mini", "gemini-2.0-flash", "azure", "textract"}

    if args.no_ollama:
        selected_names = [n for n in selected_names if n not in ollama_names]
    if args.only_free:
        selected_names = [n for n in selected_names if n not in api_names]

    # Instantiate methods (skip unavailable)
    methods = []
    for name in selected_names:
        if name not in registry:
            print(f"Warning: unknown method '{name}', skipping.")
            continue
        try:
            m = registry[name]()
            methods.append(m)
        except Exception as e:
            print(f"Warning: could not load method '{name}': {e}")

    if not methods:
        print("No methods available. Check dependencies and try again.")
        sys.exit(1)

    print(f"\nMethods selected: {[m.name for m in methods]}")

    # ---- Discover samples ----
    samples_dir = args.samples or (Path(__file__).parent / "benchmarks" / "samples")
    task_filter = None if args.task == "all" else args.task
    samples = _discover_samples(samples_dir, task_filter)

    if not samples:
        print(f"\nNo samples found in {samples_dir}")
        print("Add PDF or image files under ocr/benchmarks/samples/ to run benchmarks.")
        print("\nYou can run a quick smoke test with --samples on any directory with PDFs/images.")
        sys.exit(0)

    print(f"Samples found: {len(samples)}")
    for s in samples:
        print(f"  {s.task:12s} {s.name}")

    # ---- Run benchmark ----
    runner = BenchmarkRunner(
        methods=methods,
        samples=samples,
        output_dir=args.output,
        verbose=True,
    )
    results = runner.run()
    summary = runner.summary()

    # ---- Print summary table ----
    print_summary_table(summary)

    # ---- Generate HTML/markdown report ----
    raw_data = [r.to_dict() for r in results]
    report_path = generate_report(raw_data, output_dir=Path("ocr/results/reports"))
    print(f"\nFull report: {report_path}")


if __name__ == "__main__":
    main()
