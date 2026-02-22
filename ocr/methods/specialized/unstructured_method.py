"""
unstructured (unstructured-io) – universal document parsing.
Best for: heterogeneous document pipelines (PDF, DOCX, HTML, email, etc.).
Extracts text elements, tables, and image descriptions in a unified API.
Cost: free (open-source) or cloud API
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class UnstructuredMethod(BaseOCR):
    name = "unstructured"
    category = "specialized"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, strategy: str = "hi_res",
                 languages: list[str] | None = None):
        """
        strategy: 'fast' | 'ocr_only' | 'hi_res' | 'auto'
        'hi_res' uses layout detection + OCR for best quality.
        """
        self.strategy = strategy
        self.languages = languages or ["eng"]

    def _parse(self, file_path: Path) -> list:
        from unstructured.partition.auto import partition
        elements = partition(
            filename=str(file_path),
            strategy=self.strategy,
            languages=self.languages,
        )
        return elements

    def _elements_to_result(self, elements: list, task: str, file_path: Path,
                             pages: int) -> OCRResult:
        texts = []
        tables = []
        images = []

        for el in elements:
            el_type = type(el).__name__
            if el_type == "Table":
                md = getattr(el.metadata, "text_as_html", None) or el.text
                page_num = getattr(el.metadata, "page_number", None)
                tables.append({
                    "page": page_num,
                    "markdown": md,
                    "rows": [],
                })
            elif el_type == "Image":
                page_num = getattr(el.metadata, "page_number", None)
                images.append({
                    "page": page_num,
                    "description": el.text or "embedded image",
                })
            else:
                if el.text:
                    texts.append(el.text)

        return OCRResult(
            method=self.name, task=task,
            input_path=str(file_path),
            text="\n\n".join(texts),
            tables=tables, images=images,
            pages=pages, cost_usd=0.0,
            metadata={"strategy": self.strategy, "element_count": len(elements)},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        elements = self._parse(pdf_path)
        pages = self._pdf_page_count(pdf_path)
        return self._elements_to_result(elements, "pdf_text", pdf_path, pages)

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        elements = self._parse(image_path)
        return self._elements_to_result(elements, "image_text", image_path, 1)

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        elements = self._parse(pdf_path)
        pages = self._pdf_page_count(pdf_path)
        return self._elements_to_result(elements, "pdf_assets", pdf_path, pages)
