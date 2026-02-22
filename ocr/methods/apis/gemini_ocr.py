"""
Google Gemini vision OCR.
Best for: large documents (1M context), cost-effective at scale.
Pricing (gemini-2.0-flash): $0.10/MTok input, $0.40/MTok output
Pricing (gemini-1.5-pro): $1.25/MTok input (<=128K), $5/MTok output
Images: ~1,290 tokens per 1024×1024 image; PDFs billed as images per page
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from ..base import BaseOCR, OCRResult

_PRICING = {
    "gemini-2.0-flash":          {"input": 0.10 / 1e6, "output": 0.40 / 1e6},
    "gemini-2.0-flash-lite":     {"input": 0.075 / 1e6, "output": 0.30 / 1e6},
    "gemini-1.5-pro":            {"input": 1.25 / 1e6, "output": 5.0 / 1e6},
    "gemini-1.5-flash":          {"input": 0.075 / 1e6, "output": 0.30 / 1e6},
}


def _estimate_cost(model: str, in_tok: int, out_tok: int) -> float:
    p = _PRICING.get(model, {"input": 0.10 / 1e6, "output": 0.40 / 1e6})
    return in_tok * p["input"] + out_tok * p["output"]


class GeminiOCRMethod(BaseOCR):
    name = "gemini-2.0-flash"
    category = "api"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, api_key: str | None = None,
                 model: str = "gemini-2.0-flash",
                 max_output_tokens: int = 4096):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        self.model = model
        self.max_output_tokens = max_output_tokens
        self.name = model

    def _get_model(self):
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        return genai.GenerativeModel(self.model)

    def _call_with_image(self, image_path: Path, prompt: str) -> tuple[str, int, int]:
        import google.generativeai as genai
        from PIL import Image

        model = self._get_model()
        img = Image.open(image_path)
        response = model.generate_content(
            [img, prompt],
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=self.max_output_tokens,
            ),
        )
        text = response.text or ""
        # Gemini returns token counts in usage_metadata
        usage = getattr(response, "usage_metadata", None)
        in_tok = getattr(usage, "prompt_token_count", 0) if usage else 0
        out_tok = getattr(usage, "candidates_token_count", 0) if usage else 0
        return text, in_tok, out_tok

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        prompt = "Extract all text from this image exactly as it appears. Output only the text."
        text, in_tok, out_tok = self._call_with_image(image_path, prompt)
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
            text, in_tok, out_tok = self._call_with_image(tmp_path, prompt)
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
            "3. Describe any figures.\n\n"
            "Format: TEXT:\n...\n\nTABLES:\n...\n\nFIGURES:\n..."
        )
        for page_num, img in enumerate(images):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(buf.read())
                tmp_path = Path(tmp.name)
            text, in_tok, out_tok = self._call_with_image(tmp_path, prompt)
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
