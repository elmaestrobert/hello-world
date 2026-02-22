"""
Base class for Ollama-hosted vision models.
All models share the same /api/generate endpoint with image payloads.
"""
from __future__ import annotations

import base64
import io
import json
import time
import urllib.request
from pathlib import Path
from typing import Any

from ..base import BaseOCR, OCRResult


def _image_to_b64(img_or_path) -> str:
    """Convert a file path or PIL Image to base64 string."""
    if isinstance(img_or_path, (str, Path)):
        with open(img_or_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    # PIL Image
    buf = io.BytesIO()
    img_or_path.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


class BaseOllamaVision(BaseOCR):
    category = "ollama"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = False

    def __init__(self, model: str, host: str = "http://localhost:11434",
                 prompt: str | None = None, timeout: int = 300):
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout
        self.prompt = prompt or (
            "You are an OCR assistant. Extract ALL text from this image exactly as it appears, "
            "preserving layout and structure. Output only the extracted text, nothing else."
        )

    def _call_ollama(self, b64_image: str) -> str:
        payload = {
            "model": self.model,
            "prompt": self.prompt,
            "images": [b64_image],
            "stream": False,
        }
        data = json.dumps(payload).encode()
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            result = json.loads(resp.read())
        return result.get("response", "").strip()

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        b64 = _image_to_b64(image_path)
        text = self._call_ollama(b64)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
            metadata={"model": self.model},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        images = self._pdf_to_images(pdf_path)
        texts = []
        for img in images:
            b64 = _image_to_b64(img)
            texts.append(self._call_ollama(b64))
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=len(images), cost_usd=0.0,
            metadata={"model": self.model},
        )
