"""Day 6 I/O helpers: CSV loading, null normalization, JSON writing.

This module owns the boundary between disk and memory:
- load_orders_csv: read raw CSV into list of dicts
- normalize_nulls: convert common null-token strings into key absence
- reshape_summary_for_json: convert tuple-keyed summary into flat dicts
- write_summary_json, write_quarantine_json: persist outputs
"""

import csv
import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


NULL_TOKENS = frozenset({"", "N/A", "n/a", "NULL", "null", "None", "none", "-"})


# ---- CSV loading -----------------------------------------------------------

def load_orders_csv(path: Path) -> list[dict[str, Any]]:
    """Read a CSV of orders and return as a list of dicts.

    Uses utf-8-sig to handle BOM, and newline='' so the csv module
    correctly handles embedded newlines in quoted fields.
    """
    logger.info("Reading CSV: %s", path)
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    logger.info("Read %d rows from %s", len(rows), path.name)
    return rows


# ---- Null normalization ----------------------------------------------------

def normalize_nulls(
    row: dict[str, Any],
    *,
    null_tokens: frozenset[str] = NULL_TOKENS,
) -> dict[str, Any]:
    """Remove dict keys whose string values are recognized null tokens.

    Turns CSV's "empty string means null" convention into Python's
    "missing key means missing data" convention, so the existing
    validator's MissingFieldError path handles them cleanly.
    """
    return {
        k: v for k, v in row.items()
        if not (isinstance(v, str) and v.strip() in null_tokens)
    }


# ---- JSON output -----------------------------------------------------------

def reshape_summary_for_json(
    summary: list[tuple[tuple[str, str], dict[str, float]]],
) -> list[dict[str, Any]]:
    """[((region, category), stats), ...] → list of flat dicts.

    Promotes the composite tuple key to first-class region/category
    fields so the result is JSON-serializable and downstream-friendly.
    """
    return [
        {"region": region, "category": category, **stats}
        for (region, category), stats in summary
    ]


def write_summary_json(
    summary: list[tuple[tuple[str, str], dict[str, float]]],
    path: Path,
) -> None:
    """Reshape the summary and write it as pretty UTF-8 JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    reshaped = reshape_summary_for_json(summary)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(reshaped, f, indent=2, ensure_ascii=False, allow_nan=False)
    logger.info("Wrote summary (%d records) to %s", len(reshaped), path)


def write_quarantine_json(
    quarantined: list[tuple[dict[str, Any], str]],
    path: Path,
) -> None:
    """Write quarantined rows with their failure reasons as pretty JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    records = [{"row": row, "error": err} for row, err in quarantined]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False, allow_nan=False)
    logger.info("Wrote quarantine (%d records) to %s", len(records), path)