"""
Anthropic Claude vision OCR.
Best for: complex reasoning over documents, imperfect image transcription.
Models: claude-3-5-sonnet-latest, claude-3-5-haiku-latest
Pricing (claude-3-5-sonnet): $3/MTok input, $15/MTok output
Pricing (claude-3-5-haiku): $0.80/MTok input, $4/MTok output
Image billing: images tokenized; 1024×1024 ≈ 1600 tokens
"""
from __future__ import annotations

import base64
import os
from pathlib import Path

from ..base import BaseOCR, OCRResult

# Per-token pricing (USD per token)
_PRICING = {
    "claude-3-5-sonnet-latest": {"input": 3.0 / 1e6, "output": 15.0 / 1e6},
    "claude-3-5-haiku-latest":  {"input": 0.80 / 1e6, "output": 4.0 / 1e6},
    "claude-3-7-sonnet-latest": {"input": 3.0 / 1e6, "output": 15.0 / 1e6},
}


def _estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p = _PRICING.get(model, {"input": 3.0 / 1e6, "output": 15.0 / 1e6})
    return input_tokens * p["input"] + output_tokens * p["output"]


class AnthropicOCRMethod(BaseOCR):
    name = "claude-3-5-sonnet"
    category = "api"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, api_key: str | None = None,
                 model: str = "claude-3-5-sonnet-latest",
                 max_tokens: int = 4096):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        self.max_tokens = max_tokens
        self.name = model.replace("-latest", "")

    def _get_client(self):
        import anthropic
        return anthropic.Anthropic(api_key=self.api_key)

    def _image_block(self, image_path: Path) -> dict:
        suffix = image_path.suffix.lower().lstrip(".")
        media_type = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                      "png": "image/png", "gif": "image/gif",
                      "webp": "image/webp"}.get(suffix, "image/png")
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return {
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": data},
        }

    def _call_api(self, content: list, prompt: str) -> tuple[str, int, int]:
        client = self._get_client()
        messages = [{"role": "user", "content": content + [{"type": "text", "text": prompt}]}]
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=messages,
        )
        text = response.content[0].text if response.content else ""
        return text, response.usage.input_tokens, response.usage.output_tokens

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        prompt = (
            "Extract all text from this image exactly as it appears. "
            "Preserve layout and structure. Output only the extracted text."
        )
        content = [self._image_block(image_path)]
        text, in_tok, out_tok = self._call_api(content, prompt)
        cost = _estimate_cost(self.model, in_tok, out_tok)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=cost,
            metadata={"model": self.model, "input_tokens": in_tok, "output_tokens": out_tok},
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        images = self._pdf_to_images(pdf_path)
        all_texts = []
        total_cost = 0.0
        total_in, total_out = 0, 0
        prompt = (
            "Extract all text from this page exactly as it appears. "
            "Preserve layout and structure. Output only the extracted text."
        )
        for img in images:
            import io, tempfile
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(buf.read())
                tmp_path = Path(tmp.name)
            content = [self._image_block(tmp_path)]
            text, in_tok, out_tok = self._call_api(content, prompt)
            tmp_path.unlink(missing_ok=True)
            all_texts.append(text)
            total_cost += _estimate_cost(self.model, in_tok, out_tok)
            total_in += in_tok
            total_out += out_tok

        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(all_texts),
            pages=len(images), cost_usd=total_cost,
            metadata={"model": self.model, "input_tokens": total_in, "output_tokens": total_out},
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        images = self._pdf_to_images(pdf_path)
        all_texts = []
        all_tables = []
        total_cost = 0.0
        prompt = (
            "Analyze this document page and:\n"
            "1. Extract all text preserving structure.\n"
            "2. Represent any tables in Markdown table format.\n"
            "3. Describe any figures/images found.\n\n"
            "Format your response as:\n"
            "TEXT:\n<extracted text>\n\n"
            "TABLES:\n<markdown tables>\n\n"
            "FIGURES:\n<figure descriptions>"
        )
        for page_num, img in enumerate(images):
            import io, tempfile
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(buf.read())
                tmp_path = Path(tmp.name)
            content = [self._image_block(tmp_path)]
            text, in_tok, out_tok = self._call_api(content, prompt)
            tmp_path.unlink(missing_ok=True)
            all_texts.append(text)
            total_cost += _estimate_cost(self.model, in_tok, out_tok)

            # Parse tables section
            if "TABLES:" in text:
                tables_section = text.split("TABLES:")[-1].split("FIGURES:")[0].strip()
                if tables_section and tables_section != "None":
                    all_tables.append({
                        "page": page_num + 1,
                        "markdown": tables_section,
                        "rows": [],
                    })

        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            text="\n\n".join(all_texts),
            tables=all_tables,
            pages=len(images), cost_usd=total_cost,
            metadata={"model": self.model},
        )
