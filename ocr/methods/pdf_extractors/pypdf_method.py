"""
pypdf – pure-Python PDF text extraction (no C dependencies).
Best for: simple digital PDFs, quick extraction without system deps.
Speed: fast
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class PyPDFMethod(BaseOCR):
    name = "pypdf"
    category = "pdf_extractor"
    supports_pdf_text = True
    supports_image_text = False
    supports_pdf_assets = False

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        from pypdf import PdfReader

        reader = PdfReader(str(pdf_path))
        pages = len(reader.pages)
        texts = [page.extract_text() or "" for page in reader.pages]
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=pages, cost_usd=0.0,
        )
