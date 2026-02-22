"""
MiniCPM-V via Ollama.
Best for: high-resolution OCR, compact deployment (5.5GB model).
OCRBench: beats GPT-4o at 8.1B params (v2.6).
Supports up to 1.8M pixel images (1344×1344).
Cost: free (local compute)
"""
from __future__ import annotations

from .base_ollama import BaseOllamaVision


class MiniCPMVMethod(BaseOllamaVision):
    name = "minicpm-v"

    def __init__(self, host: str = "http://localhost:11434", **kwargs):
        super().__init__(model="minicpm-v", host=host, **kwargs)
