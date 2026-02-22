"""
EasyOCR – deep-learning OCR, 80+ languages.
Best for: multilingual text, scene text in images.
Speed: moderate (GPU preferred)
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class EasyOCRMethod(BaseOCR):
    name = "easyocr"
    category = "local_package"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = False

    def __init__(self, langs: list[str] | None = None, gpu: bool = False):
        self.langs = langs or ["en"]
        self.gpu = gpu
        self._reader = None  # lazy init

    def _reader_instance(self):
        if self._reader is None:
            import easyocr
            self._reader = easyocr.Reader(self.langs, gpu=self.gpu)
        return self._reader

    def _image_to_text(self, img_or_path) -> str:
        reader = self._reader_instance()
        results = reader.readtext(img_or_path, detail=0, paragraph=True)
        return "\n".join(results)

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        text = self._image_to_text(str(image_path))
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
            metadata={"langs": self.langs},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        import numpy as np

        images = self._pdf_to_images(pdf_path)
        texts = [self._image_to_text(np.array(img)) for img in images]
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=len(images), cost_usd=0.0,
            metadata={"langs": self.langs},
        )
