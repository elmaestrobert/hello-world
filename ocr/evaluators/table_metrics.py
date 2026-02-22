"""
Table extraction quality metrics.

Metrics:
  - table_count_match: bool – did we find the same number of tables as reference?
  - cell_accuracy: fraction of cells matching reference (after alignment)
  - structure_score: jaccard similarity of (row_count, col_count) pairs
"""
from __future__ import annotations


def _parse_markdown_table(md: str) -> list[list[str]]:
    """Parse a markdown table into a list of rows (each row is a list of cells)."""
    rows = []
    for line in md.strip().splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        if set(line.replace("|", "").replace("-", "").replace(" ", "")) == set():
            continue  # separator row
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def _cell_accuracy(pred_rows: list[list[str]], ref_rows: list[list[str]]) -> float:
    """Fraction of cells in predicted table that match reference (aligned by position)."""
    if not ref_rows:
        return 1.0 if not pred_rows else 0.0
    total = sum(len(r) for r in ref_rows)
    if total == 0:
        return 0.0
    matches = 0
    for r_idx, ref_row in enumerate(ref_rows):
        pred_row = pred_rows[r_idx] if r_idx < len(pred_rows) else []
        for c_idx, ref_cell in enumerate(ref_row):
            pred_cell = pred_row[c_idx] if c_idx < len(pred_row) else ""
            if ref_cell.lower().strip() == pred_cell.lower().strip():
                matches += 1
    return matches / total


def score_tables(predicted_tables: list[dict], reference_tables: list[dict]) -> dict:
    """
    Compare extracted tables against reference.
    Tables are matched by order (table 0 vs table 0, etc.).
    """
    n_pred = len(predicted_tables)
    n_ref = len(reference_tables)

    if n_ref == 0:
        return {
            "table_count_match": n_pred == 0,
            "cell_accuracy": 1.0 if n_pred == 0 else 0.0,
            "structure_score": 1.0 if n_pred == 0 else 0.0,
            "tables_predicted": n_pred,
            "tables_reference": n_ref,
        }

    cell_accuracies = []
    structure_scores = []
    for i in range(min(n_pred, n_ref)):
        pred_md = predicted_tables[i].get("markdown", "")
        ref_md = reference_tables[i].get("markdown", "")
        pred_rows = _parse_markdown_table(pred_md)
        ref_rows = _parse_markdown_table(ref_md)
        cell_accuracies.append(_cell_accuracy(pred_rows, ref_rows))
        # Structure: compare shape
        pred_shape = (len(pred_rows), max((len(r) for r in pred_rows), default=0))
        ref_shape = (len(ref_rows), max((len(r) for r in ref_rows), default=0))
        if pred_shape == ref_shape:
            structure_scores.append(1.0)
        else:
            # Partial credit
            row_sim = min(pred_shape[0], ref_shape[0]) / max(ref_shape[0], 1)
            col_sim = min(pred_shape[1], ref_shape[1]) / max(ref_shape[1], 1)
            structure_scores.append((row_sim + col_sim) / 2)

    return {
        "table_count_match": n_pred == n_ref,
        "cell_accuracy": round(sum(cell_accuracies) / max(len(cell_accuracies), 1), 4),
        "structure_score": round(sum(structure_scores) / max(len(structure_scores), 1), 4),
        "tables_predicted": n_pred,
        "tables_reference": n_ref,
    }
