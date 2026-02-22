"""
MinerU / MinerU2.5 (Shanghai AI Lab / OpenDataLab).
Best for: end-to-end PDF to Markdown/JSON for RAG pipelines.
Benchmark: 90.67 on OmniDocBench (CVPR 2025) — highest open-source score,
           beating Gemini-2.5 Pro on that benchmark.
Architecture (MinerU2.5): 1.2B VLM (NaViT encoder from Qwen2-VL + Qwen2-Instruct 0.5B decoder)
Speed: 2.12 pages/sec (A100 80G), 1.70 pages/sec (RTX 4090), 0.21 sec/page (CUDA)
Features: 84 languages, multi-column, LaTeX math, HTML tables, footnotes
Cost: free, open-source (Apache 2.0)
GitHub: https://github.com/opendatalab/MinerU
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class MinerUMethod(BaseOCR):
    name = "mineru"
    category = "specialized"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, output_format: str = "markdown", backend: str = "pipeline"):
        """
        output_format: 'markdown' | 'json'
        backend: 'pipeline' (default) | 'vlm-transformers' | 'vlm-sglang'
        """
        self.output_format = output_format
        self.backend = backend

    def _run_mineru(self, file_path: Path) -> tuple[str, list, list, int]:
        """Run MinerU on a file and return (text, tables, images, page_count)."""
        from magic_pdf.data.data_reader_writer import FileBasedDataWriter
        from magic_pdf.data.dataset import PymuPDFDataset
        from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
        from magic_pdf.config.enums import SupportedPdfParseMethod
        import json

        # Read file bytes
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()

        # Use in-memory writer for output
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmpdir:
            writer = FileBasedDataWriter(tmpdir)
            reader = PymuPDFDataset(pdf_bytes)

            # Parse via pipeline (or VLM if vlm backend selected)
            if self.backend.startswith("vlm"):
                from magic_pdf.pipe.UnicodeDetectPipe import UnicodeDetectPipe
                pipe = UnicodeDetectPipe(reader, {}, writer)
            else:
                from magic_pdf.pipe.StandardJsonPipe import StandardJsonPipe
                pipe = StandardJsonPipe(reader, {}, writer)

            pipe.pipe_classify()
            pipe.pipe_analyze()
            pipe.pipe_parse()

            # Collect markdown output
            md_path = os.path.join(tmpdir, "output.md")
            if os.path.exists(md_path):
                text = open(md_path).read()
            else:
                # fallback: collect from pipe result
                text = pipe.get_markdown("") if hasattr(pipe, "get_markdown") else ""

            pages = reader.__len__() if hasattr(reader, "__len__") else 1

        # Extract tables from markdown
        import re
        tables = []
        for m in re.finditer(r"(\|.+\|\n)+", text):
            tables.append({"page": None, "markdown": m.group().strip(), "rows": []})

        return text, tables, [], pages

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        text, tables, images, pages = self._run_mineru(pdf_path)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text=text, pages=pages, cost_usd=0.0,
            metadata={"backend": self.backend, "output_format": self.output_format},
        )

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        # MinerU works on PDFs natively; convert image to single-page PDF first
        try:
            from PIL import Image
            import fitz
            import io, tempfile

            img = Image.open(image_path).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="PDF")
            buf.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(buf.read())
                tmp_pdf = Path(tmp.name)
            text, tables, images, pages = self._run_mineru(tmp_pdf)
            tmp_pdf.unlink(missing_ok=True)
        except Exception as e:
            return OCRResult(
                method=self.name, task="image_text",
                input_path=str(image_path),
                error=f"Image conversion failed: {e}",
            )
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
            metadata={"backend": self.backend},
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        text, tables, images, pages = self._run_mineru(pdf_path)
        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            text=text, tables=tables, images=images,
            pages=pages, cost_usd=0.0,
            metadata={"backend": self.backend, "tables_found": len(tables)},
        )
