"""
Docling (IBM Research) – enterprise document parsing.
Best for: corporate/enterprise documents; 97.9% complex table accuracy.
Architecture: DocLayNet layout analysis + TableFormer table recognition.
Speed: 3.1 sec/page (CPU), 0.49 sec/page (CUDA)
Cost: free, open-source (MIT)
GitHub: https://github.com/DS4SD/docling
"""
from __future__ import annotations

import re
from pathlib import Path

from ..base import BaseOCR, OCRResult


class DoclingMethod(BaseOCR):
    name = "docling"
    category = "specialized"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, ocr: bool = True, table_structure: bool = True):
        self.ocr = ocr
        self.table_structure = table_structure

    def _get_converter(self):
        from docling.document_converter import DocumentConverter
        from docling.datamodel.pipeline_options import PipelineOptions
        pipeline_options = PipelineOptions(
            do_ocr=self.ocr,
            do_table_structure=self.table_structure,
        )
        return DocumentConverter(pipeline_options=pipeline_options)

    def _process(self, path: Path) -> tuple[str, list, int]:
        converter = self._get_converter()
        result = converter.convert(str(path))
        doc = result.document

        # Export markdown
        md = doc.export_to_markdown()

        # Count pages
        pages = len(doc.pages) if hasattr(doc, "pages") and doc.pages else 1

        # Extract tables from markdown
        tables = []
        for m in re.finditer(r"(\|.+\|\n)+", md):
            tables.append({"page": None, "markdown": m.group().strip(), "rows": []})

        return md, tables, pages

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        text, tables, pages = self._process(pdf_path)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text=text, pages=pages, cost_usd=0.0,
            metadata={"output_format": "markdown"},
        )

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        text, tables, pages = self._process(image_path)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
            metadata={"output_format": "markdown"},
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        text, tables, pages = self._process(pdf_path)
        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            text=text, tables=tables,
            pages=pages, cost_usd=0.0,
            metadata={"output_format": "markdown", "tables_found": len(tables)},
        )
