"""
Base class for all OCR methods.
Each method must implement the three evaluation tasks:
  1. pdf_text   - Extract text from a PDF
  2. image_text - Extract text from an image
  3. pdf_assets - Extract images and tables from a PDF
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class OCRResult:
    """Standardized output from any OCR method."""
    method: str
    task: str                   # "pdf_text" | "image_text" | "pdf_assets"
    input_path: str
    text: str = ""              # Extracted text (for text tasks)
    tables: list[dict] = field(default_factory=list)   # [{page, markdown, rows}]
    images: list[dict] = field(default_factory=list)   # [{page, description, bytes}]
    elapsed_s: float = 0.0      # Wall-clock seconds
    cost_usd: float = 0.0       # Estimated cost in USD
    pages: int = 1              # Number of pages/images processed
    error: str | None = None    # Set if the method failed
    metadata: dict = field(default_factory=dict)  # Method-specific extras

    @property
    def cost_per_page(self) -> float:
        return self.cost_usd / max(self.pages, 1)

    @property
    def seconds_per_page(self) -> float:
        return self.elapsed_s / max(self.pages, 1)

    def to_dict(self) -> dict:
        return {
            "method": self.method,
            "task": self.task,
            "input_path": self.input_path,
            "text_length": len(self.text),
            "tables_count": len(self.tables),
            "images_count": len(self.images),
            "elapsed_s": round(self.elapsed_s, 3),
            "cost_usd": round(self.cost_usd, 6),
            "pages": self.pages,
            "seconds_per_page": round(self.seconds_per_page, 3),
            "cost_per_page": round(self.cost_per_page, 6),
            "error": self.error,
            "metadata": self.metadata,
        }


class BaseOCR(ABC):
    """Abstract base class all OCR methods must implement."""

    #: Set in subclass – human-readable name shown in reports
    name: str = "unnamed"
    #: Category for grouping in reports
    category: str = "unknown"  # "local_package" | "pdf_extractor" | "ollama" | "api" | "specialized"
    #: Which tasks this method supports
    supports_pdf_text: bool = True
    supports_image_text: bool = True
    supports_pdf_assets: bool = False  # tables + figures

    def extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        """Extract text from a PDF file."""
        if not self.supports_pdf_text:
            return OCRResult(
                method=self.name, task="pdf_text",
                input_path=str(pdf_path),
                error="Not supported by this method",
            )
        start = time.perf_counter()
        try:
            result = self._extract_pdf_text(pdf_path)
            result.elapsed_s = time.perf_counter() - start
            return result
        except Exception as exc:
            return OCRResult(
                method=self.name, task="pdf_text",
                input_path=str(pdf_path),
                elapsed_s=time.perf_counter() - start,
                error=str(exc),
            )

    def extract_image_text(self, image_path: Path) -> OCRResult:
        """Extract text from an image file."""
        if not self.supports_image_text:
            return OCRResult(
                method=self.name, task="image_text",
                input_path=str(image_path),
                error="Not supported by this method",
            )
        start = time.perf_counter()
        try:
            result = self._extract_image_text(image_path)
            result.elapsed_s = time.perf_counter() - start
            return result
        except Exception as exc:
            return OCRResult(
                method=self.name, task="image_text",
                input_path=str(image_path),
                elapsed_s=time.perf_counter() - start,
                error=str(exc),
            )

    def extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        """Extract tables and embedded images from a PDF."""
        if not self.supports_pdf_assets:
            return OCRResult(
                method=self.name, task="pdf_assets",
                input_path=str(pdf_path),
                error="Not supported by this method",
            )
        start = time.perf_counter()
        try:
            result = self._extract_pdf_assets(pdf_path)
            result.elapsed_s = time.perf_counter() - start
            return result
        except Exception as exc:
            return OCRResult(
                method=self.name, task="pdf_assets",
                input_path=str(pdf_path),
                elapsed_s=time.perf_counter() - start,
                error=str(exc),
            )

    # ------------------------------------------------------------------ #
    # Subclasses implement these                                           #
    # ------------------------------------------------------------------ #

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        raise NotImplementedError

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        raise NotImplementedError

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # Shared helpers                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _pdf_page_count(pdf_path: Path) -> int:
        try:
            import fitz  # PyMuPDF
            with fitz.open(str(pdf_path)) as doc:
                return len(doc)
        except ImportError:
            pass
        try:
            from pypdf import PdfReader
            return len(PdfReader(str(pdf_path)).pages)
        except ImportError:
            pass
        return 1

    @staticmethod
    def _pdf_to_images(pdf_path: Path, dpi: int = 150) -> list[Any]:
        """Render PDF pages to PIL Images. Returns list of PIL.Image."""
        try:
            import fitz
            from PIL import Image
            import io
            images = []
            with fitz.open(str(pdf_path)) as doc:
                for page in doc:
                    mat = fitz.Matrix(dpi / 72, dpi / 72)
                    pix = page.get_pixmap(matrix=mat)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    images.append(img)
            return images
        except ImportError as e:
            raise RuntimeError(f"PyMuPDF required for PDF-to-image: {e}") from e
