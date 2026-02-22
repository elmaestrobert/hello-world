"""
Mistral OCR (mistral-ocr-latest / mistral-ocr-3).
Best for: comprehensive document understanding, tables, handwriting.
Pricing: $1/1000 pages (standard), $0.50/1000 pages (batch API)
Speed: up to 2000 pages/minute on single node
Accuracy: ~94.9% across document types; 96.6% on tables; 88.9% handwriting
Unique: extracts embedded images alongside text into interleaved markdown
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from ..base import BaseOCR, OCRResult

# Price per page (standard API)
_PRICE_PER_PAGE = 1.0 / 1000  # $0.001


class MistralOCRMethod(BaseOCR):
    name = "mistral-ocr"
    category = "api"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, api_key: str | None = None,
                 model: str = "mistral-ocr-latest",
                 include_image_base64: bool = False):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY", "")
        self.model = model
        self.include_image_base64 = include_image_base64

    def _get_client(self):
        from mistralai import Mistral
        return Mistral(api_key=self.api_key)

    def _process_document(self, document_payload: dict, pages: int) -> OCRResult:
        client = self._get_client()
        response = client.ocr.process(
            model=self.model,
            document=document_payload,
            include_image_base64=self.include_image_base64,
        )
        # Aggregate text and assets from all pages
        texts = []
        tables = []
        images = []
        for page in response.pages:
            texts.append(page.markdown)
            # Tables are embedded in markdown; images listed separately
            for img in (page.images or []):
                images.append({
                    "page": page.index + 1,
                    "id": img.id,
                    "description": f"Image {img.id} on page {page.index + 1}",
                })

        full_text = "\n\n".join(texts)
        cost = pages * _PRICE_PER_PAGE

        return OCRResult(
            method=self.name, task="pdf_text",
            input_path="",
            text=full_text,
            tables=tables, images=images,
            pages=pages, cost_usd=cost,
            metadata={"model": self.model, "pages_processed": pages},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        pages = self._pdf_page_count(pdf_path)
        with open(pdf_path, "rb") as f:
            pdf_b64 = base64.b64encode(f.read()).decode()
        document = {
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_b64}",
        }
        result = self._process_document(document, pages)
        result.task = "pdf_text"
        result.input_path = str(pdf_path)
        return result

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        suffix = image_path.suffix.lower().lstrip(".")
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                "gif": "image/gif", "webp": "image/webp"}.get(suffix, "image/png")
        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        document = {
            "type": "image_url",
            "image_url": f"data:{mime};base64,{img_b64}",
        }
        result = self._process_document(document, 1)
        result.task = "image_text"
        result.input_path = str(image_path)
        return result

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        result = self._extract_pdf_text(pdf_path)
        result.task = "pdf_assets"
        return result
