"""
Benchmark runner – orchestrates running all configured OCR methods
against test samples and computing evaluation metrics.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..methods.base import BaseOCR, OCRResult
from .text_metrics import score_text
from .table_metrics import score_tables


@dataclass
class BenchmarkSample:
    """A single test sample for the benchmark."""
    path: Path
    task: str                  # "pdf_text" | "image_text" | "pdf_assets"
    ground_truth_text: str = ""
    ground_truth_tables: list[dict] = field(default_factory=list)
    name: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = self.path.name


@dataclass
class BenchmarkResult:
    """Results from running one method on one sample."""
    method: str
    sample: str
    task: str
    ocr_result: OCRResult
    text_scores: dict = field(default_factory=dict)
    table_scores: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "sample": self.sample,
            "task": self.task,
            **self.ocr_result.to_dict(),
            "text_scores": self.text_scores,
            "table_scores": self.table_scores,
        }


class BenchmarkRunner:
    def __init__(self, methods: list[BaseOCR], samples: list[BenchmarkSample],
                 output_dir: Path | None = None, verbose: bool = True):
        self.methods = methods
        self.samples = samples
        self.output_dir = output_dir or Path("results/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        self.results: list[BenchmarkResult] = []

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def run(self) -> list[BenchmarkResult]:
        self.results = []
        total = len(self.methods) * len(self.samples)
        done = 0

        for sample in self.samples:
            for method in self.methods:
                done += 1
                self._log(f"[{done}/{total}] {method.name} | {sample.name} ({sample.task})")

                # Check method supports this task
                supports = {
                    "pdf_text": method.supports_pdf_text,
                    "image_text": method.supports_image_text,
                    "pdf_assets": method.supports_pdf_assets,
                }
                if not supports.get(sample.task, False):
                    self._log(f"  -> skipped (not supported)")
                    continue

                # Run OCR
                if sample.task == "pdf_text":
                    ocr_result = method.extract_pdf_text(sample.path)
                elif sample.task == "image_text":
                    ocr_result = method.extract_image_text(sample.path)
                else:
                    ocr_result = method.extract_pdf_assets(sample.path)

                if ocr_result.error:
                    self._log(f"  -> ERROR: {ocr_result.error}")

                # Evaluate
                text_scores = {}
                table_scores = {}
                if sample.ground_truth_text and ocr_result.text:
                    text_scores = score_text(ocr_result.text, sample.ground_truth_text)
                if sample.ground_truth_tables:
                    table_scores = score_tables(ocr_result.tables, sample.ground_truth_tables)

                bench_result = BenchmarkResult(
                    method=method.name,
                    sample=sample.name,
                    task=sample.task,
                    ocr_result=ocr_result,
                    text_scores=text_scores,
                    table_scores=table_scores,
                )
                self.results.append(bench_result)

                if text_scores:
                    self._log(
                        f"  CER={text_scores.get('cer', '-'):.3f}  "
                        f"WER={text_scores.get('wer', '-'):.3f}  "
                        f"sim={text_scores.get('char_similarity', '-'):.3f}  "
                        f"t={ocr_result.elapsed_s:.1f}s  "
                        f"cost=${ocr_result.cost_usd:.5f}"
                    )

        # Save raw results
        self._save_results()
        return self.results

    def _save_results(self):
        ts = int(time.time())
        out_file = self.output_dir / f"benchmark_{ts}.json"
        data = [r.to_dict() for r in self.results]
        with open(out_file, "w") as f:
            json.dump(data, f, indent=2, default=str)
        self._log(f"\nResults saved to {out_file}")
        return out_file

    def summary(self) -> dict[str, dict]:
        """Aggregate results by method."""
        agg: dict[str, dict[str, list]] = {}
        for r in self.results:
            if r.ocr_result.error:
                continue
            m = r.method
            if m not in agg:
                agg[m] = {
                    "cer": [], "wer": [], "char_similarity": [], "bleu1": [],
                    "elapsed_s": [], "cost_usd": [], "seconds_per_page": [], "cost_per_page": [],
                    "cell_accuracy": [], "structure_score": [],
                }
            agg[m]["elapsed_s"].append(r.ocr_result.elapsed_s)
            agg[m]["cost_usd"].append(r.ocr_result.cost_usd)
            agg[m]["seconds_per_page"].append(r.ocr_result.seconds_per_page)
            agg[m]["cost_per_page"].append(r.ocr_result.cost_per_page)
            for k in ["cer", "wer", "char_similarity", "bleu1"]:
                if k in r.text_scores:
                    agg[m][k].append(r.text_scores[k])
            for k in ["cell_accuracy", "structure_score"]:
                if k in r.table_scores:
                    agg[m][k].append(r.table_scores[k])

        summary = {}
        for method, vals in agg.items():
            summary[method] = {
                k: round(sum(v) / len(v), 4) if v else None
                for k, v in vals.items()
            }
        return summary
