"""
GLM-OCR (THUDM/GLM-4) via Ollama.
Best for: complex document understanding, Chinese/multilingual text.
Purpose-built OCR model on the GLM-V encoder-decoder architecture.
Cost: free (local compute)
"""
from __future__ import annotations

from .base_ollama import BaseOllamaVision


class GLMOCRMethod(BaseOllamaVision):
    name = "glm-ocr"

    def __init__(self, host: str = "http://localhost:11434", **kwargs):
        super().__init__(model="glm-ocr", host=host, **kwargs)
