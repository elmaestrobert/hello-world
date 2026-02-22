"""
Camelot – PDF table extraction using lattice or stream algorithms.
Best for: tables with visible borders (lattice) or whitespace-aligned (stream).
Requires: ghostscript for lattice mode
Cost: free
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class CamelotMethod(BaseOCR):
    name = "camelot"
    category = "specialized"
    supports_pdf_text = False
    supports_image_text = False
    supports_pdf_assets = True

    def __init__(self, flavor: str = "lattice"):
        """
        flavor: 'lattice' (ruled lines) or 'stream' (whitespace-based).
        """
        self.flavor = flavor
        self.name = f"camelot-{flavor}"

    def _extract_pdf_assets(self, pdf_path: Path) -> OCRResult:
        import camelot

        pages_count = self._pdf_page_count(pdf_path)
        tables_list = camelot.read_pdf(str(pdf_path), pages="all", flavor=self.flavor)
        tables = []
        for tbl in tables_list:
            df = tbl.df
            page = tbl.page
            md_lines = ["| " + " | ".join(str(c) for c in df.columns) + " |"]
            md_lines.append("|" + "|".join(["---"] * len(df.columns)) + "|")
            for _, row in df.iterrows():
                md_lines.append("| " + " | ".join(str(v) for v in row) + " |")
            tables.append({
                "page": page,
                "markdown": "\n".join(md_lines),
                "rows": df.values.tolist(),
                "shape": list(df.shape),
                "accuracy": tbl.accuracy,
                "whitespace": tbl.whitespace,
            })
        return OCRResult(
            method=self.name, task="pdf_assets",
            input_path=str(pdf_path),
            tables=tables,
            pages=pages_count, cost_usd=0.0,
            metadata={"flavor": self.flavor, "tables_found": len(tables)},
        )
