"""
PyMuPDF (fitz) – fast native PDF text and asset extraction.
Best for: digitally created PDFs (not scanned). Extracts text, images, tables.
Speed: very fast
Cost: free (AGPL / commercial license available)
"""
from __future__ import annotations

import io
from pathlib import Path

from ..base import BaseOCR, OCRResult


class PyMuPDFMethod(BaseOCR):
    name = "pymupdf"
    category = "pdf_extractor"
    supports_pdf_text = True
    supports_image_text = False
    supports_pdf_assets = True

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        import fitz

        texts = []
        with fitz.open(str(pdf_path)) as doc:
            pages = len(doc)
            for page in doc:
                texts.append(page.get_text("text"))
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=pages, cost_usd=0.0,
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        import fitz

        tables = []
        images = []

        with fitz.open(str(pdf_path)) as doc:
            pages = len(doc)
            for page_num, page in enumerate(doc):
                # Extract tables using PyMuPDF's built-in table detection
                try:
                    tab_finder = page.find_tables()
                    for tab in tab_finder.tables:
                        df = tab.to_pandas()
                        tables.append({
                            "page": page_num + 1,
                            "markdown": df.to_markdown(index=False),
                            "rows": df.values.tolist(),
                            "shape": list(df.shape),
                        })
                except Exception:
                    pass  # table detection not always available

                # Extract embedded images
                for img_info in page.get_images(full=True):
                    xref = img_info[0]
                    try:
                        base_image = doc.extract_image(xref)
                        images.append({
                            "page": page_num + 1,
                            "ext": base_image["ext"],
                            "width": base_image["width"],
                            "height": base_image["height"],
                            "size_bytes": len(base_image["image"]),
                            "description": f"Embedded image xref={xref}",
                        })
                    except Exception:
                        pass

        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            tables=tables, images=images,
            pages=pages, cost_usd=0.0,
            metadata={"tables_found": len(tables), "images_found": len(images)},
        )
