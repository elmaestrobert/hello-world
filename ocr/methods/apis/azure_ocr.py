"""
Azure AI Document Intelligence (formerly Form Recognizer).
Best for: enterprise document processing, forms, invoices, ID documents.
Pricing: ~$1.50/1000 pages (Read/OCR), $1.25/100 pages (General Document).
Accuracy: 89.5% on diverse types (per Mistral internal benchmark).
"""
from __future__ import annotations

import os
from pathlib import Path

from ..base import BaseOCR, OCRResult

# Read model: $1.50 per 1,000 pages
_PRICE_PER_PAGE = 1.50 / 1000


class AzureDocIntelligenceMethod(BaseOCR):
    name = "azure-doc-intelligence"
    category = "api"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self, endpoint: str | None = None,
                 api_key: str | None = None,
                 model_id: str = "prebuilt-read"):
        self.endpoint = endpoint or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
        self.api_key = api_key or os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
        self.model_id = model_id

    def _get_client(self):
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential
        return DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key),
        )

    def _analyze_file(self, file_path: Path) -> tuple[str, list[dict], list[dict], int]:
        from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

        client = self._get_client()
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document(
                model_id=self.model_id,
                analyze_request=f,
                content_type="application/octet-stream",
            )
        result = poller.result()

        # Text
        pages_count = len(result.pages) if result.pages else 1
        texts = []
        for page in (result.pages or []):
            page_lines = [line.content for line in (page.lines or [])]
            texts.append("\n".join(page_lines))

        # Tables
        tables = []
        for tbl in (result.tables or []):
            rows_dict: dict[int, dict[int, str]] = {}
            for cell in (tbl.cells or []):
                rows_dict.setdefault(cell.row_index, {})[cell.column_index] = cell.content
            if not rows_dict:
                continue
            n_cols = max(max(r.keys()) for r in rows_dict.values()) + 1
            header = [rows_dict.get(0, {}).get(c, "") for c in range(n_cols)]
            md = ["| " + " | ".join(header) + " |",
                  "|" + "|".join(["---"] * n_cols) + "|"]
            for r_idx in sorted(rows_dict.keys())[1:]:
                row = [rows_dict[r_idx].get(c, "") for c in range(n_cols)]
                md.append("| " + " | ".join(row) + " |")
            tables.append({
                "page": tbl.bounding_regions[0].page_number if tbl.bounding_regions else None,
                "markdown": "\n".join(md),
                "rows": [],
            })

        images_info: list[dict] = []  # Azure Read model doesn't extract embedded images

        return "\n\n".join(texts), tables, images_info, pages_count

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        text, tables, images, pages = self._analyze_file(pdf_path)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text=text, tables=tables, images=images,
            pages=pages, cost_usd=pages * _PRICE_PER_PAGE,
            metadata={"model_id": self.model_id},
        )

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        text, tables, images, pages = self._analyze_file(image_path)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=_PRICE_PER_PAGE,
            metadata={"model_id": self.model_id},
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        result = self._extract_pdf_text(pdf_path)
        result.task = "pdf_assets"
        return result
