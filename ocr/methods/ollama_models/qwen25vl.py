"""
Qwen2.5-VL via Ollama.
Best for: OCR, document understanding, charts, general vision tasks.
DocVQA: 95.7 (top open-source 7B)
Available sizes: qwen2.5vl:3b, qwen2.5vl:7b, qwen2.5vl:72b
Requires: Ollama >= 0.7.0
Cost: free (local compute)
"""
from __future__ import annotations

from .base_ollama import BaseOllamaVision


class Qwen25VLMethod(BaseOllamaVision):
    name = "qwen2.5vl"

    def __init__(self, size: str = "7b", host: str = "http://localhost:11434", **kwargs):
        model = f"qwen2.5vl:{size}"
        super().__init__(model=model, host=host, **kwargs)
        self.name = f"qwen2.5vl:{size}"
