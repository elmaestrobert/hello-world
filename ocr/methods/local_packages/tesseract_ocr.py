"""
Tesseract OCR via pytesseract.
Best for: simple printed text on clean backgrounds.
Speed: fast (CPU)
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class TesseractOCR(BaseOCR):
    name = "tesseract"
    category = "local_package"
    supports_pdf_text = True   # renders to image then OCRs
    supports_image_text = True
    supports_pdf_assets = False

    def __init__(self, lang: str = "eng", config: str = "--oem 3 --psm 3"):
        self.lang = lang
        self.config = config

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        import pytesseract
        from PIL import Image

        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=self.lang, config=self.config)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text.strip(),
            pages=1,
            cost_usd=0.0,
            metadata={"lang": self.lang},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        import pytesseract

        images = self._pdf_to_images(pdf_path)
        pages = len(images)
        texts = [pytesseract.image_to_string(img, lang=self.lang, config=self.config)
                 for img in images]
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(t.strip() for t in texts),
            pages=pages,
            cost_usd=0.0,
            metadata={"lang": self.lang},
        )
