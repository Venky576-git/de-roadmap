"""Day 5 transforms: DQ exception hierarchy, per-row + batch validation, aggregation.

Builds on day04_transforms. Adds:
- DataQualityError exception hierarchy with structured attributes
- validate_order(): per-row schema + value validation
- validate_batch(): looped validator with logging and quarantine routing
- Input validation on summarize_orders' metric parameter
"""

import logging
from collections import defaultdict
from typing import Any

logger = logging.getLogger(__name__)


# ---- Exception hierarchy ----------------------------------------------------

class DataQualityError(Exception):
    """Base class for all data quality failures."""


class MissingFieldError(DataQualityError):
    """A required field was absent from the row."""

    def __init__(self, field: str, row_id: Any):
        super().__init__(f"Missing field {field!r} in row {row_id!r}")
        self.field = field
        self.row_id = row_id


class InvalidValueError(DataQualityError):
    """A field is present but the value is unusable."""

    def __init__(self, field: str, row_id: Any, value: Any):
        super().__init__(f"Invalid value {value!r} for field {field!r} in row {row_id!r}")
        self.field = field
        self.row_id = row_id
        self.value = value


# ---- Per-row validation -----------------------------------------------------

REQUIRED_FIELDS = ("order_id", "region", "category", "amount")


def validate_order(row: dict[str, Any]) -> dict[str, Any]:
    """Validate one order row. Returns the row unchanged on success.

    Raises:
        MissingFieldError: if a required field is absent.
        InvalidValueError: if 'amount' is unparseable or negative.
    """
    for field in REQUIRED_FIELDS:
        if field not in row:
            raise MissingFieldError(field, row.get("order_id", "unknown"))

    try:
        amount = float(row["amount"])
    except (ValueError, TypeError) as e:
        raise InvalidValueError("amount", row["order_id"], row["amount"]) from e

    if amount < 0:
        raise InvalidValueError("amount", row["order_id"], row["amount"])

    return row


# ---- Batch validation with quarantine --------------------------------------

def validate_batch(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[tuple[dict[str, Any], str]]]:
    """Validate a batch. Returns (valid_rows, quarantined_rows).

    Each quarantined entry is (row, error_message) — paired so downstream
    reporting can show both the offending data and the reason it was rejected.
    Unexpected exceptions are logged with full traceback and re-raised.
    """
    logger.info("Validating batch of %d rows", len(rows))
    valid: list[dict[str, Any]] = []
    quarantined: list[tuple[dict[str, Any], str]] = []
    for row in rows:
        try:
            validate_order(row)
            valid.append(row)
        except DataQualityError as e:
            logger.warning("Quarantining row %s: %s", e.row_id, e)
            quarantined.append((row, str(e)))
        except Exception:
            logger.exception("Unexpected failure validating row %r", row)
            raise
    logger.info("Validation complete: %d valid, %d quarantined", len(valid), len(quarantined))
    return valid, quarantined


# ---- Aggregation ------------------------------------------------------------

VALID_METRICS = {"total_revenue", "order_count", "avg_order_value"}


def summarize_orders(
    data: list[dict[str, Any]],
    *,
    metric: str = "total_revenue",
    top_n: int = 3,
    **filters: Any,
) -> list[tuple[tuple[str, str], dict[str, float]]]:
    """Aggregate orders by (region, category), return top-N groups by metric."""
    if metric not in VALID_METRICS:
        raise ValueError(f"metric must be one of {VALID_METRICS}, got {metric!r}")

    data = [row for row in data
            if all(row.get(k) == v for k, v in filters.items())]

    stats = defaultdict(lambda: {"total_revenue": 0, "order_count": 0})
    for row in data:
        key = (row["region"], row["category"])
        stats[key]["total_revenue"] += row["amount"]
        stats[key]["order_count"] += 1

    for stat in stats.values():
        stat["avg_order_value"] = stat["total_revenue"] / stat["order_count"]

    return sorted(stats.items(), key=lambda kv: kv[1][metric], reverse=True)[:top_n]