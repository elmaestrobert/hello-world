"""
tabula-py – PDF table extraction via Java tabula library.
Best for: simple tabular data in PDFs; Java-based so cross-platform.
Requires: Java JRE
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class TabulaMethod(BaseOCR):
    name = "tabula"
    category = "specialized"
    supports_pdf_text = False
    supports_image_text = False
    supports_pdf_assets = True

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        import tabula

        pages_count = self._pdf_page_count(pdf_path)
        dfs = tabula.read_pdf(str(pdf_path), pages="all", multiple_tables=True,
                              silent=True)
        tables = []
        for i, df in enumerate(dfs):
            if df.empty:
                continue
            df = df.fillna("")
            md_lines = ["| " + " | ".join(str(c) for c in df.columns) + " |"]
            md_lines.append("|" + "|".join(["---"] * len(df.columns)) + "|")
            for _, row in df.iterrows():
                md_lines.append("| " + " | ".join(str(v) for v in row) + " |")
            tables.append({
                "page": None,  # tabula doesn't always report page per table
                "table_index": i,
                "markdown": "\n".join(md_lines),
                "rows": df.values.tolist(),
                "shape": list(df.shape),
            })
        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            tables=tables,
            pages=pages_count, cost_usd=0.0,
            metadata={"tables_found": len(tables)},
        )
