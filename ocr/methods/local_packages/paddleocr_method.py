"""
PaddleOCR – state-of-the-art open-source OCR, 80+ languages.
Best for: structured documents, mixed layouts, high accuracy.
Speed: fast (CPU/GPU)
Cost: free
Benchmark: ~92-97% accuracy on invoices/receipts
"""
from __future__ import annotations

import io
from pathlib import Path

from ..base import BaseOCR, OCRResult


class PaddleOCRMethod(BaseOCR):
    name = "paddleocr"
    category = "local_package"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = False

    def __init__(self, lang: str = "en", use_gpu: bool = False, use_angle_cls: bool = True):
        self.lang = lang
        self.use_gpu = use_gpu
        self.use_angle_cls = use_angle_cls
        self._ocr = None

    def _ocr_instance(self):
        if self._ocr is None:
            from paddleocr import PaddleOCR
            self._ocr = PaddleOCR(
                use_angle_cls=self.use_angle_cls,
                lang=self.lang,
                use_gpu=self.use_gpu,
                show_log=False,
            )
        return self._ocr

    def _image_to_text(self, img) -> str:
        """img can be a file path str, numpy array, or PIL Image."""
        import numpy as np
        if hasattr(img, "mode"):  # PIL Image
            img = np.array(img)
        ocr = self._ocr_instance()
        result = ocr.ocr(img, cls=self.use_angle_cls)
        if not result or result[0] is None:
            return ""
        lines = []
        for line in result[0]:
            if line and len(line) >= 2:
                lines.append(line[1][0])
        return "\n".join(lines)

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        text = self._image_to_text(str(image_path))
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
            metadata={"lang": self.lang},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        images = self._pdf_to_images(pdf_path)
        texts = [self._image_to_text(img) for img in images]
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=len(images), cost_usd=0.0,
            metadata={"lang": self.lang},
        )
