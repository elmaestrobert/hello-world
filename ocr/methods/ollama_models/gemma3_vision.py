"""
Gemma 3 (Google) via Ollama.
Best for: general multimodal tasks, vision reasoning.
Available: gemma3:4b, gemma3:12b, gemma3:27b (vision variants)
Cost: free (local compute)
"""
from __future__ import annotations

from .base_ollama import BaseOllamaVision


class Gemma3VisionMethod(BaseOllamaVision):
    name = "gemma3"

    def __init__(self, size: str = "12b", host: str = "http://localhost:11434", **kwargs):
        model = f"gemma3:{size}"
        super().__init__(model=model, host=host, **kwargs)
        self.name = f"gemma3:{size}"
