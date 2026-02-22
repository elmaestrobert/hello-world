"""
Marker – converts PDF/images to high-quality Markdown.
Best for: scientific PDFs, mixed content (text + math + tables + images).
Speed: moderate (GPU preferred for full quality)
Cost: free (open-source, datalab-to/marker)
Benchmark: 76.1 on olmOCR-Bench (competitive with specialized tools)
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class MarkerMethod(BaseOCR):
    name = "marker"
    category = "pdf_extractor"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True  # outputs tables in markdown, extracts figures

    def __init__(self, langs: list[str] | None = None, batch_multiplier: int = 2):
        self.langs = langs
        self.batch_multiplier = batch_multiplier

    def _run_marker(self, file_path: str, is_pdf: bool = True):
        from marker.convert import convert_single_pdf
        from marker.models import load_all_models

        model_lst = load_all_models()
        full_text, images, out_meta = convert_single_pdf(
            file_path,
            model_lst,
            langs=self.langs,
            batch_multiplier=self.batch_multiplier,
        )
        return full_text, images, out_meta

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        full_text, images, meta = self._run_marker(str(pdf_path))
        pages = meta.get("pages", 1)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text=full_text,
            pages=pages, cost_usd=0.0,
            metadata={"output_format": "markdown", **meta},
        )

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        full_text, images, meta = self._run_marker(str(image_path), is_pdf=False)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=full_text,
            pages=1, cost_usd=0.0,
            metadata={"output_format": "markdown", **meta},
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        import re

        full_text, extracted_images, meta = self._run_marker(str(pdf_path))
        pages = meta.get("pages", 1)

        # Parse markdown tables from output text
        tables = []
        table_pattern = re.compile(r"(\|.+\|\n)+", re.MULTILINE)
        for match in table_pattern.finditer(full_text):
            tables.append({
                "page": None,  # marker doesn't always report page per table
                "markdown": match.group().strip(),
                "rows": [],
            })

        images = [
            {"page": None, "description": name, "size_bytes": len(data)}
            for name, data in (extracted_images or {}).items()
        ]

        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            text=full_text,
            tables=tables, images=images,
            pages=pages, cost_usd=0.0,
            metadata={"output_format": "markdown"},
        )
