"""
pdfplumber – precise PDF text and table extraction using pdfminer backend.
Best for: digital PDFs with tables, precise character-level positioning.
Speed: moderate
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class PDFPlumberMethod(BaseOCR):
    name = "pdfplumber"
    category = "pdf_extractor"
    supports_pdf_text = True
    supports_image_text = False
    supports_pdf_assets = True

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        import pdfplumber

        texts = []
        with pdfplumber.open(str(pdf_path)) as pdf:
            pages = len(pdf.pages)
            for page in pdf.pages:
                text = page.extract_text() or ""
                texts.append(text)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=pages, cost_usd=0.0,
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        import pdfplumber

        tables = []
        images_info = []

        with pdfplumber.open(str(pdf_path)) as pdf:
            pages = len(pdf.pages)
            for page_num, page in enumerate(pdf.pages):
                # Tables
                for tab in page.extract_tables() or []:
                    if not tab:
                        continue
                    header = tab[0]
                    rows = tab[1:]
                    md_lines = ["| " + " | ".join(str(c or "") for c in header) + " |"]
                    md_lines.append("|" + "|".join(["---"] * len(header)) + "|")
                    for row in rows:
                        md_lines.append("| " + " | ".join(str(c or "") for c in row) + " |")
                    tables.append({
                        "page": page_num + 1,
                        "markdown": "\n".join(md_lines),
                        "rows": tab,
                        "shape": [len(tab), len(header) if header else 0],
                    })

                # Images (metadata only – pdfplumber doesn't extract raw bytes by default)
                for img in page.images or []:
                    images_info.append({
                        "page": page_num + 1,
                        "width": img.get("width"),
                        "height": img.get("height"),
                        "x0": img.get("x0"),
                        "y0": img.get("y0"),
                        "description": f"Image on page {page_num+1}",
                    })

        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            tables=tables, images=images_info,
            pages=pages, cost_usd=0.0,
            metadata={"tables_found": len(tables), "images_found": len(images_info)},
        )
