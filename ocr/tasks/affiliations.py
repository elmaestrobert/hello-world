"""
Task: Extract author affiliations from the first page of academic papers.

Strategy:
  1. Extract text from page 1 via each OCR method
  2. Apply affiliation-specific pattern matching to locate:
     - Lines following author names (^[A-Z][a-z]+ [A-Z][a-z]+, ...)
     - Lines with affiliation markers (superscript numbers, *, †, ‡)
     - Lines containing institutional keywords
  3. Return structured {author, affiliation, email} records

Usage:
  python -m ocr.tasks.affiliations --pdf path/to/paper.pdf
  python -m ocr.tasks.affiliations --dir ocr/benchmarks/samples/arxiv/
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ─── Regex patterns ───────────────────────────────────────────────────────────

# Lines that look like affiliation text
AFFIL_KEYWORDS = re.compile(
    r"(university|institute|department|school|college|laboratory|lab|center|centre|"
    r"research|group|foundation|company|corporation|inc\.|ltd\.|gmbh|"
    r"inria|cnrs|mpg|mpi|etf|eth|mit|caltech|nyu|ucl|epfl|kaist|"
    r"usa|uk|france|germany|china|japan|india|korea|italy|canada|australia)",
    re.IGNORECASE,
)

EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w{2,}")

# Superscript/footnote markers used in author lines
MARKER_RE = re.compile(r"^[\d,*†‡§¶]+$")

# Institutional address indicators
ADDRESS_RE = re.compile(
    r"\b(\d{4,6}|[A-Z]{2}\s+\d{5}|[A-Z][a-z]+\s+(Street|Ave|Road|Boulevard|"
    r"Way|Drive|Lane|Blvd|Rd|St|Ave)\b)",
    re.IGNORECASE,
)


def extract_affiliations_from_text(page1_text: str) -> dict:
    """
    Parse the first page text of an academic paper and return structured
    affiliation data.

    Returns:
        {
            "raw_affiliation_block": str,   # all candidate affiliation lines
            "emails": [str],
            "institutions": [str],          # unique institution lines
            "authors_line": str,            # best guess at the author name line
        }
    """
    lines = [ln.strip() for ln in page1_text.splitlines() if ln.strip()]

    # Find candidate affiliation block: lines after the first author-looking line
    # that contain institutional keywords or email addresses
    affil_lines = []
    emails = []
    institutions = []
    authors_line = ""

    # Scan for author + affiliation region (usually lines 3–30 on page 1)
    in_affil_zone = False
    for i, line in enumerate(lines[:60]):  # Only consider first 60 lines

        # Email detection
        found_emails = EMAIL_RE.findall(line)
        if found_emails:
            emails.extend(found_emails)
            affil_lines.append(line)
            in_affil_zone = True
            continue

        # Line with affiliation keywords
        if AFFIL_KEYWORDS.search(line):
            affil_lines.append(line)
            institutions.append(line)
            in_affil_zone = True
            continue

        # Address-like line (zip codes, street numbers)
        if ADDRESS_RE.search(line) and len(line) < 120:
            affil_lines.append(line)
            in_affil_zone = True
            continue

        # Short marker-only line (superscript keys) — part of affil block
        if MARKER_RE.match(line) and in_affil_zone:
            affil_lines.append(line)
            continue

        # Likely author names line: mixed Title-case words, commas, no verbs
        if (not authors_line and i > 1 and len(line) > 10
                and re.match(r"^[A-Z][a-z]", line)
                and "," in line
                and not AFFIL_KEYWORDS.search(line)
                and not any(c.isdigit() for c in line[:20])):
            authors_line = line

    return {
        "raw_affiliation_block": "\n".join(affil_lines),
        "emails": list(dict.fromkeys(emails)),   # unique, preserving order
        "institutions": list(dict.fromkeys(institutions)),
        "authors_line": authors_line,
    }


def run_extraction(pdf_path: Path, methods: list | None = None) -> dict:
    """
    Run affiliation extraction on a paper using one or more OCR methods.
    Returns a dict keyed by method name.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))

    results = {}

    # Always include PyMuPDF (fast, no API key needed)
    if methods is None or "pymupdf" in methods:
        try:
            import fitz
            with fitz.open(str(pdf_path)) as doc:
                page1_text = doc[0].get_text("text")
            parsed = extract_affiliations_from_text(page1_text)
            results["pymupdf"] = {"raw_text": page1_text[:2000], **parsed}
        except Exception as e:
            results["pymupdf"] = {"error": str(e)}

    # pdfplumber
    if methods is None or "pdfplumber" in methods:
        try:
            import pdfplumber
            with pdfplumber.open(str(pdf_path)) as pdf:
                page1_text = pdf.pages[0].extract_text() or ""
            parsed = extract_affiliations_from_text(page1_text)
            results["pdfplumber"] = {"raw_text": page1_text[:2000], **parsed}
        except Exception as e:
            results["pdfplumber"] = {"error": str(e)}

    # pypdf
    if methods is None or "pypdf" in methods:
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(pdf_path))
            page1_text = reader.pages[0].extract_text() or ""
            parsed = extract_affiliations_from_text(page1_text)
            results["pypdf"] = {"raw_text": page1_text[:2000], **parsed}
        except Exception as e:
            results["pypdf"] = {"error": str(e)}

    return results


def print_results(pdf_path: Path, results: dict, verbose: bool = False):
    print(f"\n{'='*70}")
    print(f"AFFILIATION EXTRACTION: {pdf_path.name}")
    print(f"{'='*70}")
    for method, data in results.items():
        print(f"\n--- {method.upper()} ---")
        if "error" in data:
            print(f"  ERROR: {data['error']}")
            continue
        if data.get("authors_line"):
            print(f"  Authors:      {data['authors_line'][:100]}")
        print(f"  Institutions ({len(data['institutions'])}):")
        for inst in data["institutions"][:8]:
            print(f"    • {inst[:90]}")
        if data["emails"]:
            print(f"  Emails:       {', '.join(data['emails'][:5])}")
        if verbose and data.get("raw_text"):
            print(f"\n  -- Raw page 1 text (first 500 chars) --")
            print(f"  {data['raw_text'][:500]}")


def main():
    parser = argparse.ArgumentParser(description="Extract author affiliations from papers")
    parser.add_argument("--pdf", type=Path, help="Single PDF to process")
    parser.add_argument("--dir", type=Path, help="Directory of PDFs to process")
    parser.add_argument("--methods", nargs="+", default=None,
                        help="Methods to use (default: pymupdf pdfplumber pypdf)")
    parser.add_argument("--output", type=Path, default=None, help="Save JSON results")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    pdfs = []
    if args.pdf:
        pdfs = [args.pdf]
    elif args.dir:
        pdfs = sorted(args.dir.glob("*.pdf"))
    else:
        # Default: arxiv samples
        pdfs = sorted((Path(__file__).parent.parent / "benchmarks" / "samples" / "arxiv").glob("*.pdf"))

    if not pdfs:
        print("No PDFs found.")
        sys.exit(1)

    all_results = {}
    for pdf in pdfs:
        res = run_extraction(pdf, methods=args.methods)
        print_results(pdf, res, verbose=args.verbose)
        all_results[pdf.name] = res

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(all_results, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")

    return all_results


if __name__ == "__main__":
    main()
