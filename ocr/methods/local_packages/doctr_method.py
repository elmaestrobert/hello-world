"""
docTR (Document Text Recognition) by Mindee.
Best for: full document analysis pipeline, structured documents.
Speed: moderate (GPU preferred)
Cost: free (open-source)
"""
from __future__ import annotations

from pathlib import Path

from ..base import BaseOCR, OCRResult


class DocTRMethod(BaseOCR):
    name = "doctr"
    category = "local_package"
    supports_pdf_text = True
    supports_image_text = True
    supports_pdf_assets = False

    def __init__(self, det_arch: str = "db_resnet50", reco_arch: str = "crnn_vgg16_bn",
                 pretrained: bool = True):
        self.det_arch = det_arch
        self.reco_arch = reco_arch
        self.pretrained = pretrained
        self._model = None

    def _get_model(self):
        if self._model is None:
            from doctr.models import ocr_predictor
            self._model = ocr_predictor(
                det_arch=self.det_arch,
                reco_arch=self.reco_arch,
                pretrained=self.pretrained,
            )
        return self._model

    def _doc_to_text(self, result) -> str:
        lines = []
        for page in result.pages:
            for block in page.blocks:
                for line in block.lines:
                    lines.append(" ".join(word.value for word in line.words))
        return "\n".join(lines)

    def _extract_image_text(self, image_path: Path) -> OCRResult:
        from doctr.io import DocumentFile
        model = self._get_model()
        doc = DocumentFile.from_images([str(image_path)])
        result = model(doc)
        text = self._doc_to_text(result)
        return OCRResult(
            method=self.name, task="image_text",
            input_path=str(image_path),
            text=text, pages=1, cost_usd=0.0,
        )

    def _extract_pdf_text(self, pdf_path: Path) -> OCRResult:
        from doctr.io import DocumentFile
        model = self._get_model()
        doc = DocumentFile.from_pdf(str(pdf_path))
        result = model(doc)
        text = self._doc_to_text(result)
        pages = len(result.pages)
        return OCRResult(
            method=self.name, task="pdf_text",
            input_path=str(pdf_path),
            text=text, pages=pages, cost_usd=0.0,
        )
