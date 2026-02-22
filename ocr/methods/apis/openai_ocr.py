"""
OpenAI GPT-4o / GPT-4o-mini vision OCR.
Best for: general vision tasks, document understanding with reasoning.
Pricing (gpt-4o): $2.50/MTok input, $10/MTok output
Pricing (gpt-4o-mini): $0.15/MTok input, $0.60/MTok output
Images: ~85 tokens (low detail) or 765–1105+ tokens (high detail) per tile
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from ..base import BaseOCR, OCRResult

_PRICING = {
    "gpt-4o":         {"input": 2.50 / 1e6, "output": 10.0 / 1e6},
    "gpt-4o-mini":    {"input": 0.15 / 1e6, "output": 0.60 / 1e6},
    "gpt-4.1":        {"input": 2.00 / 1e6, "output": 8.0 / 1e6},
    "gpt-4.1-mini":   {"input": 0.40 / 1e6, "output": 1.60 / 1e6},
}


def _estimate_cost(model: str, in_tok: int, out_tok: int) -> float:
    p = _PRICING.get(model, {"input": 2.50 / 1e6, "output": 10.0 / 1e6})
    return in_tok * p["input"] + out_tok * p["output"]


class OpenAIOCRMethod(BaseOCR):
    name = "gpt-4o"
    category = "api"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, api_key: str | None = None,
                 model: str = "gpt-4o",
                 detail: str = "high",
                 max_tokens: int = 4096):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.detail = detail
        self.max_tokens = max_tokens
        self.name = model

    def _get_client(self):
        from openai import OpenAI
        return OpenAI(api_key=self.api_key)

    def _image_url_block(self, image_path: Path) -> dict:
        suffix = image_path.suffix.lower().lstrip(".")
        media_type = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                      "png": "image/png"}.get(suffix, "image/png")
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:{media_type};base64,{b64}",
                "detail": self.detail,
            },
        }

    def _call_api(self, img_path: Path, prompt: str) -> tuple[str, int, int]:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{
                "role": "user",
                "content": [
                    self._image_url_block(img_path),
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        text = response.choices[0].message.content or ""
        usage = response.usage
        return text, usage.prompt_tokens, usage.completion_tokens

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        prompt = (
            "Extract all text from this image exactly as it appears. "
            "Preserve layout. Output only the extracted text."
        )
        text, in_tok, out_tok = self._call_api(image_path, prompt)
        cost = _estimate_cost(self.model, in_tok, out_tok)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=cost,
            metadata={"model": self.model, "input_tokens": in_tok, "output_tokens": out_tok},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        import io, tempfile
        images = self._pdf_to_images(pdf_path)
        texts = []
        total_cost = 0.0
        prompt = "Extract all text from this page exactly as it appears. Output only the text."
        for img in images:
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(buf.read())
                tmp_path = Path(tmp.name)
            text, in_tok, out_tok = self._call_api(tmp_path, prompt)
            tmp_path.unlink(missing_ok=True)
            texts.append(text)
            total_cost += _estimate_cost(self.model, in_tok, out_tok)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            pages=len(images), cost_usd=total_cost,
            metadata={"model": self.model},
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        import io, tempfile
        images = self._pdf_to_images(pdf_path)
        texts, tables = [], []
        total_cost = 0.0
        prompt = (
            "Analyze this document page:\n"
            "1. Extract all text with structure.\n"
            "2. Represent any tables in Markdown format.\n"
            "3. Describe figures/images.\n\n"
            "Format: TEXT:\n...\n\nTABLES:\n...\n\nFIGURES:\n..."
        )
        for page_num, img in enumerate(images):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(buf.read())
                tmp_path = Path(tmp.name)
            text, in_tok, out_tok = self._call_api(tmp_path, prompt)
            tmp_path.unlink(missing_ok=True)
            texts.append(text)
            total_cost += _estimate_cost(self.model, in_tok, out_tok)
            if "TABLES:" in text:
                tbl = text.split("TABLES:")[-1].split("FIGURES:")[0].strip()
                if tbl:
                    tables.append({"page": page_num + 1, "markdown": tbl, "rows": []})
        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            tables=tables,
            pages=len(images), cost_usd=total_cost,
            metadata={"model": self.model},
        )
