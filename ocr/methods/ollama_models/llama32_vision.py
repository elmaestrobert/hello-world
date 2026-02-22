"""
Llama 3.2 Vision via Ollama.
Best for: general vision tasks, instruction following.
OCR quality: good but outperformed by Qwen2.5-VL 7B on DocVQA.
Available: llama3.2-vision:11b, llama3.2-vision:90b
Cost: free (local compute)
"""
from __future__ import annotations

from .base_ollama import BaseOllamaVision


class Llama32VisionMethod(BaseOllamaVision):
    name = "llama3.2-vision"

    def __init__(self, size: str = "11b", host: str = "http://localhost:11434", **kwargs):
        model = f"llama3.2-vision:{size}"
        super().__init__(model=model, host=host, **kwargs)
        self.name = f"llama3.2-vision:{size}"
