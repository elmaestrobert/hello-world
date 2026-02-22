"""
Task: Find and extract the Executive Summary (or equivalent) from a report.

Strategy:
  1. Extract full text via each OCR method
  2. Locate the Executive Summary section by:
     - Exact heading match: "Executive Summary", "Résumé exécutif", "Zusammenfassung"
     - Fuzzy match: "exec summary", "key findings", "overview", "abstract"
     - Find the section boundaries (next heading or page break)
  3. Return the section text

Usage:
  python -m ocr.tasks.executive_summary --pdf path/to/report.pdf
  python -m ocr.tasks.executive_summary --dir ocr/benchmarks/samples/worldbank/
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ─── Heading patterns for executive summary and equivalents ──────────────────

EXEC_SUMMARY_RE = re.compile(
    r"(?:^|\n)\s*("
    r"executive\s+summ(?:ary)?|"
    r"exec(?:utive)?\s+sum|"
    r"r[eé]sum[eé]\s+ex[eé]cutif|"      # French
    r"zusammenfassung|"                    # German
    r"resumen\s+ejecutivo|"               # Spanish
    r"key\s+(?:findings|messages|points|takeaways)|"
    r"(?:main\s+)?overview|"
    r"highlights|"
    r"summary\s+(?:of\s+)?(?:findings|results|recommendations)"
    r")\s*\n",
    re.IGNORECASE | re.MULTILINE,
)

# Patterns that signal the end of the executive summary (next major section)
NEXT_SECTION_RE = re.compile(
    r"(?:^|\n)\s*(?:"
    r"chapter\s+\d+|"
    r"section\s+\d+|"
    r"\d+\.\s+[A-Z][a-z]{3,}|"          # "1. Introduction"
    r"introduction|"
    r"background|"
    r"motivation|"
    r"acknowledgements?|"
    r"table\s+of\s+contents"
    r")\s*\n",
    re.IGNORECASE | re.MULTILINE,
)


def extract_exec_summary(full_text: str, max_chars: int = 4000) -> dict:
    """
    Find and return the executive summary section from a document.

    Returns:
        {
            "found": bool,
            "heading": str,            # the heading text that was matched
            "text": str,               # the executive summary text
            "start_char": int,
            "char_count": int,
            "method_note": str,
        }
    """
    match = EXEC_SUMMARY_RE.search(full_text)

    if not match:
        # Fallback: check first 500 chars (some reports open with exec summary)
        if any(kw in full_text[:500].lower() for kw in
               ["executive summary", "key findings", "overview"]):
            return {
                "found": True,
                "heading": "Document opens with summary content",
                "text": full_text[:max_chars],
                "start_char": 0,
                "char_count": min(len(full_text), max_chars),
                "method_note": "first-page fallback",
            }
        return {
            "found": False,
            "heading": "",
            "text": "",
            "start_char": -1,
            "char_count": 0,
            "method_note": "no heading found",
        }

    start = match.end()
    heading = match.group(1).strip()

    # Find where the next major section begins
    remaining = full_text[start:]
    end_match = NEXT_SECTION_RE.search(remaining)
    if end_match:
        section_text = remaining[: end_match.start()].strip()
    else:
        section_text = remaining[:max_chars].strip()

    # Trim to max_chars if longer
    if len(section_text) > max_chars:
        section_text = section_text[:max_chars] + "\n[... truncated ...]"

    return {
        "found": True,
        "heading": heading,
        "text": section_text,
        "start_char": match.start(),
        "char_count": len(section_text),
        "method_note": "heading match",
    }


def run_extraction(pdf_path: Path, methods: list | None = None) -> dict:
    """Run executive summary extraction using multiple PDF reading methods."""
    results = {}

    # PyMuPDF – reads all pages
    if methods is None or "pymupdf" in methods:
        try:
            import fitz
            texts = []
            with fitz.open(str(pdf_path)) as doc:
                for page in doc:
                    texts.append(page.get_text("text"))
            full_text = "\n".join(texts)
            parsed = extract_exec_summary(full_text)
            results["pymupdf"] = {"pages": len(texts), "total_chars": len(full_text), **parsed}
        except Exception as e:
            results["pymupdf"] = {"error": str(e)}

    # pdfplumber
    if methods is None or "pdfplumber" in methods:
        try:
            import pdfplumber
            texts = []
            with pdfplumber.open(str(pdf_path)) as pdf:
                for page in pdf.pages:
                    texts.append(page.extract_text() or "")
            full_text = "\n".join(texts)
            parsed = extract_exec_summary(full_text)
            results["pdfplumber"] = {"pages": len(texts), "total_chars": len(full_text), **parsed}
        except Exception as e:
            results["pdfplumber"] = {"error": str(e)}

    # pypdf
    if methods is None or "pypdf" in methods:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_path))
            texts = [p.extract_text() or "" for p in reader.pages]
            full_text = "\n".join(texts)
            parsed = extract_exec_summary(full_text)
            results["pypdf"] = {"pages": len(texts), "total_chars": len(full_text), **parsed}
        except Exception as e:
            results["pypdf"] = {"error": str(e)}

    return results


def print_results(pdf_path: Path, results: dict, verbose: bool = False,
                  snippet_chars: int = 600):
    print(f"\n{'='*70}")
    print(f"EXECUTIVE SUMMARY EXTRACTION: {pdf_path.name}")
    print(f"{'='*70}")
    for method, data in results.items():
        print(f"\n--- {method.upper()} ---")
        if "error" in data:
            print(f"  ERROR: {data['error']}")
            continue
        print(f"  Pages read:   {data.get('pages', '?')}")
        print(f"  Total chars:  {data.get('total_chars', '?')}")
        print(f"  Found:        {'YES' if data['found'] else 'NO'}")
        if data["found"]:
            print(f"  Heading:      \"{data['heading']}\"")
            print(f"  Section size: {data['char_count']} chars")
            snippet = data["text"][:snippet_chars].replace("\n", "\n  ")
            print(f"\n  -- First {snippet_chars} chars of Executive Summary --")
            print(f"  {snippet}")
            if not verbose and len(data["text"]) > snippet_chars:
                print(f"\n  [... {data['char_count'] - snippet_chars} more chars ...]")
        if verbose and data.get("text"):
            print(f"\n  -- Full Executive Summary --")
            print(data["text"])


def main():
    parser = argparse.ArgumentParser(
        description="Extract executive summary from reports")
    parser.add_argument("--pdf", type=Path, help="Single PDF to process")
    parser.add_argument("--dir", type=Path, help="Directory of PDFs to process")
    parser.add_argument("--methods", nargs="+", default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--snippet", type=int, default=600,
                        help="Characters to show in preview (default 600)")
    args = parser.parse_args()

    pdfs = []
    if args.pdf:
        pdfs = [args.pdf]
    elif args.dir:
        pdfs = sorted(args.dir.glob("*.pdf"))
    else:
        pdfs = sorted(
            (Path(__file__).parent.parent / "benchmarks" / "samples" / "worldbank").glob("*.pdf")
        )

    if not pdfs:
        print("No PDFs found.")
        sys.exit(1)

    all_results = {}
    for pdf in pdfs:
        res = run_extraction(pdf, methods=args.methods)
        print_results(pdf, res, verbose=args.verbose, snippet_chars=args.snippet)
        all_results[pdf.name] = res

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(all_results, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")

    return all_results


if __name__ == "__main__":
    main()
