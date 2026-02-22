"""
Text quality metrics for OCR evaluation.

Metrics:
  - CER (Character Error Rate): edit_distance(pred, ref) / len(ref)
  - WER (Word Error Rate): word-level edit distance / len(ref_words)
  - Normalized similarity: 1 - CER (higher is better)
  - BLEU-1 (unigram): precision of predicted unigrams against reference

All metrics return values in [0, 1] unless noted.
CER/WER: lower is better. Similarity/BLEU: higher is better.
"""
from __future__ import annotations

import re
import unicodedata


def _normalize(text: str) -> str:
    """Lowercase, normalize unicode, collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _edit_distance(a: str, b: str) -> int:
    """Levenshtein distance between two strings."""
    if not a:
        return len(b)
    if not b:
        return len(a)
    # DP with two rows
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            if ca == cb:
                curr.append(prev[j - 1])
            else:
                curr.append(1 + min(prev[j], curr[j - 1], prev[j - 1]))
        prev = curr
    return prev[-1]


def cer(predicted: str, reference: str, normalize: bool = True) -> float:
    """Character Error Rate. Returns 0.0 if reference is empty."""
    if normalize:
        predicted = _normalize(predicted)
        reference = _normalize(reference)
    if not reference:
        return 0.0 if not predicted else 1.0
    return min(_edit_distance(predicted, reference) / len(reference), 1.0)


def wer(predicted: str, reference: str, normalize: bool = True) -> float:
    """Word Error Rate."""
    if normalize:
        predicted = _normalize(predicted)
        reference = _normalize(reference)
    pred_words = predicted.split()
    ref_words = reference.split()
    if not ref_words:
        return 0.0 if not pred_words else 1.0
    return min(_edit_distance(pred_words, ref_words) / len(ref_words), 1.0)


def character_similarity(predicted: str, reference: str) -> float:
    """1 - CER; higher is better."""
    return 1.0 - cer(predicted, reference)


def bleu1(predicted: str, reference: str, normalize: bool = True) -> float:
    """Unigram BLEU precision (no brevity penalty)."""
    if normalize:
        predicted = _normalize(predicted)
        reference = _normalize(reference)
    pred_words = predicted.split()
    ref_counts: dict[str, int] = {}
    for w in reference.split():
        ref_counts[w] = ref_counts.get(w, 0) + 1
    matches = 0
    for w in pred_words:
        if ref_counts.get(w, 0) > 0:
            matches += 1
            ref_counts[w] -= 1
    return matches / max(len(pred_words), 1)


def score_text(predicted: str, reference: str) -> dict[str, float]:
    """Compute all text quality metrics."""
    return {
        "cer": round(cer(predicted, reference), 4),
        "wer": round(wer(predicted, reference), 4),
        "char_similarity": round(character_similarity(predicted, reference), 4),
        "bleu1": round(bleu1(predicted, reference), 4),
    }
