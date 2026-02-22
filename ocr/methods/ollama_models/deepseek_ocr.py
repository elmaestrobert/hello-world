"""
DeepSeek-OCR / DeepSeek-OCR 2 via Ollama.
Best for: token-efficient, high-throughput PDF OCR.
Architecture: Custom DeepEncoder (compresses images up to 16x), MoE decoder.
  - 3B total params (570M active), requires Ollama >= 0.13.0
  - DeepSeek-OCR 2 (Jan 2026): replaces CLIP ViT with Qwen2-0.5B as vision
    encoder, introduces "visual causal flow"
Speed: Claimed 2,500 tokens/sec on A100 40GB; ~200,000 pages/day
Accuracy: 97% precision at <10x compression; degrades at 20x+
Cost: free (local compute)
"""
from __future__ import annotations

from .base_ollama import BaseOllamaVision


class DeepSeekOCRMethod(BaseOllamaVision):
    name = "deepseek-ocr"

    def __init__(self, version: int = 2, host: str = "http://localhost:11434", **kwargs):
        """
        version: 1 (deepseek-ocr) or 2 (deepseek-ocr2, Jan 2026)
        """
        model = "deepseek-ocr2" if version == 2 else "deepseek-ocr"
        super().__init__(model=model, host=host, **kwargs)
        self.name = model
        self.version = version
