"""
Report generation for OCR benchmark results.
Produces:
  - Console summary table (via print_summary_table)
  - Markdown report with per-task tables and cost analysis
"""
from __future__ import annotations

import json
import time
from pathlib import Path


# ─── Console summary ─────────────────────────────────────────────────────────

def print_summary_table(summary: dict[str, dict]):
    """Pretty-print a summary table to stdout."""
    if not summary:
        print("No results to summarize.")
        return

    cols = [
        ("Method",         "method",           20, "s"),
        ("CER ↓",          "cer",              8, ".3f"),
        ("WER ↓",          "wer",              8, ".3f"),
        ("Similarity ↑",   "char_similarity",  12, ".3f"),
        ("BLEU-1 ↑",       "bleu1",            9, ".3f"),
        ("Cell Acc ↑",     "cell_accuracy",    10, ".3f"),
        ("Sec/page ↓",     "seconds_per_page", 10, ".2f"),
        ("$/page ↓",       "cost_per_page",    10, ".6f"),
    ]

    header = "  ".join(f"{c[0]:<{c[2]}}" for c in cols)
    sep = "  ".join("-" * c[2] for c in cols)
    print("\n" + "=" * len(header))
    print("OCR BENCHMARK SUMMARY")
    print("=" * len(header))
    print(header)
    print(sep)

    for method, vals in sorted(summary.items()):
        row_parts = [f"{method:<20}"]
        for _, key, width, fmt in cols[1:]:
            val = vals.get(key)
            if val is None:
                row_parts.append(f"{'N/A':<{width}}")
            else:
                row_parts.append(f"{val:{fmt}}{'':<{width - len(f'{val:{fmt}}')}}".rstrip())
        print("  ".join(row_parts))

    print("=" * len(header))
    print("↓ = lower is better   ↑ = higher is better\n")


# ─── Markdown report ─────────────────────────────────────────────────────────

def _md_table(headers: list[str], rows: list[list[str]]) -> str:
    """Generate a markdown table."""
    header_row = "| " + " | ".join(headers) + " |"
    sep_row = "|" + "|".join(["---"] * len(headers)) + "|"
    data_rows = ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join([header_row, sep_row] + data_rows)


def generate_report(results: list[dict], output_dir: Path) -> Path:
    """Generate a markdown report from raw benchmark results."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    out_path = output_dir / f"report_{ts}.md"

    # Aggregate by method
    by_method: dict[str, list[dict]] = {}
    for r in results:
        m = r.get("method", "unknown")
        by_method.setdefault(m, []).append(r)

    lines = ["# OCR Benchmark Report", f"", f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
             "", f"**Methods evaluated:** {len(by_method)}",
             f"**Total runs:** {len(results)}", ""]

    # Per-task sections
    tasks = sorted({r.get("task", "") for r in results})
    for task in tasks:
        task_results = [r for r in results if r.get("task") == task]
        if not task_results:
            continue

        lines.append(f"## Task: {task.replace('_', ' ').title()}")
        lines.append("")

        # Build comparison table
        methods_in_task = sorted({r["method"] for r in task_results})

        # Text quality table
        text_headers = ["Method", "CER ↓", "WER ↓", "Similarity ↑", "BLEU-1 ↑",
                         "Sec/page ↓", "Cost/page ($) ↓", "Samples"]
        text_rows = []
        for method in methods_in_task:
            m_results = [r for r in task_results if r["method"] == method and not r.get("error")]
            if not m_results:
                continue
            ts_data = [r.get("text_scores", {}) for r in m_results]
            def avg(key):
                vals = [d.get(key) for d in ts_data if d.get(key) is not None]
                return f"{sum(vals)/len(vals):.4f}" if vals else "N/A"
            def avg_num(key):
                vals = [r.get(key, 0) for r in m_results]
                return f"{sum(vals)/len(vals):.4f}" if vals else "N/A"

            text_rows.append([
                method,
                avg("cer"), avg("wer"), avg("char_similarity"), avg("bleu1"),
                avg_num("seconds_per_page"),
                avg_num("cost_per_page"),
                str(len(m_results)),
            ])

        if text_rows:
            lines.append("### Text Extraction Quality")
            lines.append("")
            lines.append(_md_table(text_headers, text_rows))
            lines.append("")

        # Table quality table (if any table scores present)
        table_results = [r for r in task_results
                         if r.get("table_scores") and not r.get("error")]
        if table_results:
            tbl_headers = ["Method", "Cell Accuracy ↑", "Structure Score ↑",
                            "Tables Found", "Tables Reference"]
            tbl_rows = []
            for method in methods_in_task:
                m_t = [r for r in table_results if r["method"] == method]
                if not m_t:
                    continue
                def avg_ts(key):
                    vals = [r["table_scores"].get(key) for r in m_t
                            if r["table_scores"].get(key) is not None]
                    return f"{sum(vals)/len(vals):.4f}" if vals else "N/A"
                def sum_ts(key):
                    return str(sum(r["table_scores"].get(key, 0) for r in m_t))
                tbl_rows.append([
                    method,
                    avg_ts("cell_accuracy"), avg_ts("structure_score"),
                    sum_ts("tables_predicted"), sum_ts("tables_reference"),
                ])
            if tbl_rows:
                lines.append("### Table Extraction Quality")
                lines.append("")
                lines.append(_md_table(tbl_headers, tbl_rows))
                lines.append("")

        # Per-sample details
        lines.append("### Per-Sample Results")
        lines.append("")
        sample_headers = ["Method", "Sample", "CER", "WER", "Sec", "Cost ($)", "Error"]
        sample_rows = []
        for r in sorted(task_results, key=lambda x: (x.get("sample",""), x.get("method",""))):
            ts_data = r.get("text_scores", {})
            sample_rows.append([
                r.get("method", ""),
                r.get("sample", ""),
                f"{ts_data.get('cer', 'N/A')}",
                f"{ts_data.get('wer', 'N/A')}",
                f"{r.get('elapsed_s', 0):.2f}",
                f"{r.get('cost_usd', 0):.6f}",
                r.get("error") or "",
            ])
        lines.append(_md_table(sample_headers, sample_rows))
        lines.append("")

    # Cost comparison section
    lines.append("## Cost Comparison")
    lines.append("")
    lines.append("Estimated costs per 1,000 pages (based on pricing as of 2025-2026):")
    lines.append("")

    PRICING_TABLE = [
        ["mistral-ocr",       "API",      "$1.00", "$0.50 (batch)",   "~2000 pages/min"],
        ["mistral-ocr-3",     "API",      "$2.00", "$1.00 (batch)",   "~2000 pages/min"],
        ["claude-3-5-sonnet", "API",      "~$4.80*","N/A",            "~30 pages/min"],
        ["claude-3-5-haiku",  "API",      "~$1.28*","N/A",            "~60 pages/min"],
        ["gpt-4o",            "API",      "~$3.00*","N/A",            "~40 pages/min"],
        ["gpt-4o-mini",       "API",      "~$0.18*","N/A",            "~80 pages/min"],
        ["gemini-2.0-flash",  "API",      "~$0.13*","N/A",            "~100 pages/min"],
        ["azure-doc-intel",   "API",      "$1.50",  "N/A",            "~50 pages/min"],
        ["aws-textract",      "API",      "$1.50",  "$15.00 (tables)","~20 pages/min"],
        ["tesseract",         "Local",    "$0.00",  "$0.00",          "~120 pages/min (CPU)"],
        ["paddleocr",         "Local",    "$0.00",  "$0.00",          "~200 pages/min (CPU)"],
        ["surya",             "Local",    "$0.00",  "$0.00",          "~60 pages/min (GPU)"],
        ["easyocr",           "Local",    "$0.00",  "$0.00",          "~30 pages/min (CPU)"],
        ["doctr",             "Local",    "$0.00",  "$0.00",          "~60 pages/min (GPU)"],
        ["marker",            "Local",    "$0.00",  "$0.00",          "~30 pages/min (GPU)"],
        ["qwen2.5vl:7b",      "Ollama",   "$0.00",  "$0.00",          "Depends on GPU"],
        ["glm-ocr",           "Ollama",   "$0.00",  "$0.00",          "Depends on GPU"],
        ["minicpm-v",         "Ollama",   "$0.00",  "$0.00",          "Depends on GPU"],
        ["llama3.2-vision",   "Ollama",   "$0.00",  "$0.00",          "Depends on GPU"],
        ["camelot",           "Local",    "$0.00",  "$0.00",          "~500 pages/min"],
        ["tabula",            "Local",    "$0.00",  "$0.00",          "~300 pages/min"],
        ["unstructured",      "Local",    "$0.00",  "$0.00",          "~30 pages/min (hi_res)"],
    ]
    cost_headers = ["Method", "Type", "$/1K pages", "Batch", "Speed estimate"]
    lines.append(_md_table(cost_headers, PRICING_TABLE))
    lines.append("")
    lines.append("*Estimated based on token consumption (~1600 tokens/page for vision models)")
    lines.append("")

    # Benchmark scores reference
    lines.append("## Known Benchmark Scores (2025)")
    lines.append("")
    lines.append("Reference scores from public benchmarks (not from this run):")
    lines.append("")
    bench_data = [
        ["surya",             "97.70%",   "—",      "—",          "Open-source, 90+ langs"],
        ["paddleocr",         "92.96%",   "—",      "—",          "Fast CPU, 80+ langs"],
        ["qwen2.5vl:7b",      "—",        "95.7",   "—",          "Best 7B open-source VLM"],
        ["minicpm-v (2.6)",   "SOTA*",    "—",      "—",          "Beats GPT-4o on OCRBench"],
        ["glm-ocr",           "—",        "—",      "—",          "Purpose-built doc OCR"],
        ["mistral-ocr-3",     "94.9%",    "—",      "96.6%",      "Tables: 96.6%, HW: 88.9%"],
        ["azure-doc-intel",   "89.5%",    "—",      "—",          "Per Mistral benchmark"],
        ["aws-textract",      "—",        "—",      "84.8%",      "Per Mistral table benchmark"],
        ["olmOCR-2",          "—",        "—",      "82.4",       "olmOCR-Bench (specialized)"],
        ["marker",            "—",        "—",      "76.1",       "olmOCR-Bench"],
        ["tesseract",         "87.74%",   "—",      "—",          "Invoice benchmark"],
    ]
    bench_headers = ["Method", "Overall Accuracy", "DocVQA", "Table Acc.", "Notes"]
    lines.append(_md_table(bench_headers, bench_data))
    lines.append("")
    lines.append("*SOTA = State-of-the-Art on OCRBench at time of release")
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
