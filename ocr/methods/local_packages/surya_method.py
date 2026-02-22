"""
Surya OCR – modern transformer-based OCR, 90+ languages.
Best for: complex document layouts, multi-column text, reading order.
Benchmark: 97.7% accuracy on invoices; top open-source model.
Speed: moderate (GPU preferred)
Cost: free (open-source, datalab-to/surya on GitHub)
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class SuryaOCRMethod(BaseOCR):
    name = "surya"
    category = "local_package"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = False

    def __init__(self, langs: list[str] | None = None):
        self.langs = langs or ["en"]

    def _run_surya(self, images: list) -> list[str]:
        from surya.recognition import batch_recognition
        from surya.model.recognition.model import load_model
        from surya.model.recognition.processor import load_processor

        model = load_model()
        processor = load_processor()
        langs_per_image = [self.langs] * len(images)
        predictions = batch_recognition(images, langs_per_image, model, processor)
        texts = []
        for pred in predictions:
            page_text = "\n".join(line.text for line in pred.text_lines)
            texts.append(page_text)
        return texts

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        from PIL import Image
        img = Image.open(image_path).convert("RGB")
        texts = self._run_surya([img])
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=texts[0], pages=1, cost_usd=0.0,
            metadata={"langs": self.langs},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        images = self._pdf_to_images(pdf_path)
        texts = self._run_surya([img.convert("RGB") for img in images])
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=len(images), cost_usd=0.0,
            metadata={"langs": self.langs},
        )
