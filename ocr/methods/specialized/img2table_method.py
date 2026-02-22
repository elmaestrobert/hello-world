"""
img2table – table extraction from images and PDFs.
Best for: scanned documents with tables (no digital text layer needed).
Can use an OCR backend (tesseract, easyocr) for cell content extraction.
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class Img2TableMethod(BaseOCR):
    name = "img2table"
    category = "specialized"
    supports_pdf_text = False
    supports_image_text = False
    supports_pdf_assets = True

    def __init__(self, ocr_backend: str = "tesseract", implicit_rows: bool = True):
        """
        ocr_backend: 'tesseract' | 'easyocr' | None (digital PDFs only)
        """
        self.ocr_backend = ocr_backend
        self.implicit_rows = implicit_rows

    def _get_ocr(self):
        if self.ocr_backend == "tesseract":
            from img2table.ocr import TesseractOCR
            return TesseractOCR()
        elif self.ocr_backend == "easyocr":
            from img2table.ocr import EasyOCR
            return EasyOCR(lang=["en"])
        return None

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        from img2table.document import PDF

        pages_count = self._pdf_page_count(pdf_path)
        ocr = self._get_ocr()
        doc = PDF(str(pdf_path), detect_rotation=False, pdf_text_extraction=True)
        extracted = doc.extract_tables(
            ocr=ocr,
            implicit_rows=self.implicit_rows,
            borderless_tables=False,
            min_confidence=50,
        )
        tables = []
        for page_idx, page_tables in (extracted or {}).items():
            for tbl in (page_tables or []):
                df = tbl.df
                md_lines = ["| " + " | ".join(str(c) for c in df.columns) + " |"]
                md_lines.append("|" + "|".join(["---"] * len(df.columns)) + "|")
                for _, row in df.iterrows():
                    md_lines.append("| " + " | ".join(str(v) for v in row) + " |")
                tables.append({
                    "page": page_idx + 1,
                    "markdown": "\n".join(md_lines),
                    "rows": df.values.tolist(),
                    "shape": list(df.shape),
                })
        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            tables=tables,
            pages=pages_count, cost_usd=0.0,
            metadata={"ocr_backend": self.ocr_backend, "tables_found": len(tables)},
        )
