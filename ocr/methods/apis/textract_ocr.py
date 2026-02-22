"""
Amazon Textract OCR.
Best for: AWS-native pipelines, forms, tables, ID documents.
Pricing: $0.0015/page (text only), $0.015/page (with tables), $0.025/page (queries)
Accuracy: 84.8% on tables (per Mistral benchmark); strong on forms.
"""
from __future__ import annotations

import os
from pathlib import Path

from ..base import BaseOCR, OCRResult

# Pricing tiers
_PRICE_TEXT_ONLY = 0.0015    # per page, first 1M
_PRICE_WITH_TABLES = 0.015   # per page, first 1M (Analyze Tables)


class TextractOCRMethod(BaseOCR):
    name = "aws-textract"
    category = "api"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = True

    def __init__(self,
                 aws_access_key_id: str | None = None,
                 aws_secret_access_key: str | None = None,
                 region_name: str = "us-east-1",
                 extract_tables: bool = True):
        self.aws_access_key_id = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID", "")
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        self.region_name = region_name
        self.extract_tables = extract_tables

    def _get_client(self):
        import boto3
        kwargs = {"region_name": self.region_name}
        if self.aws_access_key_id:
            kwargs["aws_access_key_id"] = self.aws_access_key_id
        if self.aws_secret_access_key:
            kwargs["aws_secret_access_key"] = self.aws_secret_access_key
        return boto3.client("textract", **kwargs)

    def _detect_text(self, image_bytes: bytes) -> str:
        client = self._get_client()
        response = client.detect_document_text(Document={"Bytes": image_bytes})
        lines = [b["Text"] for b in response.get("Blocks", []) if b["BlockType"] == "LINE"]
        return "\n".join(lines)

    def _analyze_document(self, image_bytes: bytes) -> tuple[str, list[dict]]:
        client = self._get_client()
        feature_types = ["TABLES"]
        response = client.analyze_document(
            Document={"Bytes": image_bytes},
            FeatureTypes=feature_types,
        )
        blocks = {b["Id"]: b for b in response.get("Blocks", [])}
        lines = [b["Text"] for b in blocks.values() if b["BlockType"] == "LINE"]
        text = "\n".join(lines)

        # Parse tables
        tables = []
        for block in blocks.values():
            if block["BlockType"] != "TABLE":
                continue
            cells: dict[tuple[int, int], str] = {}
            max_row, max_col = 0, 0
            for rel in block.get("Relationships", []):
                if rel["Type"] != "CHILD":
                    continue
                for cell_id in rel["Ids"]:
                    cell = blocks.get(cell_id, {})
                    if cell.get("BlockType") != "CELL":
                        continue
                    r, c = cell.get("RowIndex", 1), cell.get("ColumnIndex", 1)
                    max_row, max_col = max(max_row, r), max(max_col, c)
                    words = []
                    for w_rel in cell.get("Relationships", []):
                        if w_rel["Type"] == "CHILD":
                            for w_id in w_rel["Ids"]:
                                w = blocks.get(w_id, {})
                                if w.get("BlockType") == "WORD":
                                    words.append(w.get("Text", ""))
                    cells[(r, c)] = " ".join(words)
            if not cells:
                continue
            header = [cells.get((1, c), "") for c in range(1, max_col + 1)]
            md = ["| " + " | ".join(header) + " |",
                  "|" + "|".join(["---"] * max_col) + "|"]
            for r in range(2, max_row + 1):
                row = [cells.get((r, c), "") for c in range(1, max_col + 1)]
                md.append("| " + " | ".join(row) + " |")
            tables.append({"page": None, "markdown": "\n".join(md), "rows": []})

        return text, tables

    def _process_image_bytes(self, image_bytes: bytes) -> tuple[str, list[dict]]:
        if self.extract_tables:
            return self._analyze_document(image_bytes)
        return self._detect_text(image_bytes), []

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        text, tables = self._process_image_bytes(image_bytes)
        price = _PRICE_WITH_TABLES if self.extract_tables else _PRICE_TEXT_ONLY
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, tables=tables,
            pages=1, cost_usd=price,
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        import io
        images = self._pdf_to_images(pdf_path, dpi=200)
        texts, all_tables = [], []
        price_per_page = _PRICE_WITH_TABLES if self.extract_tables else _PRICE_TEXT_ONLY
        for page_num, img in enumerate(images):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            text, tables = self._process_image_bytes(buf.getvalue())
            texts.append(text)
            for t in tables:
                t["page"] = page_num + 1
            all_tables.extend(tables)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text="\n\n".join(texts),
            tables=all_tables,
            pages=len(images), cost_usd=len(images) * price_per_page,
        )

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        result = self._extract_pdf_text(pdf_path)
        result.task = "pdf_assets"
        return result
