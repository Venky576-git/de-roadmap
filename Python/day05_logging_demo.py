# Block 3 — The logging module

# The five log levels

# import logging
# logging.debug("Detailed info, typically only visible while diagnosing")
# logging.info("Confirmation that things are working as expected")
# logging.warning("Something unexpected — pipeline can continue, but worth noting")
# logging.error("A failure — some operation couldn't be completed")
# logging.critical("Severe failure — pipeline likely cannot continue")

# When to use each in DE work — concrete heuristics:
# DEBUG — per-row processing detail, intermediate values, "about to call this API." Off in production by default.
# INFO — pipeline lifecycle events. "Started ingestion. Processed 47,832 rows. Finished in 3m 12s." The operational story of a healthy run.
# WARNING — recoverable anomalies. "Row 19384 had missing region, defaulted to 'UNKNOWN'." Pipeline continues.
# ERROR — operation failed but pipeline keeps going for the rest. "Row 5921 quarantined: invalid amount." Single-row failures are usually ERROR.
# CRITICAL — pipeline cannot continue. "Database connection lost, aborting." Reserve for "page someone at 3 a.m." conditions.

#%%
import logging
from typing import Any


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

class DataQualityError(Exception):
    """Base class for data quality errors."""

class MissingFieldError(DataQualityError):
    """Raised when a required field is missing."""
    def __init__(self, field, row_id):
        super().__init__(f"Missing field '{field}' in row {row_id}")
        self.field = field
        self.row_id = row_id

class InvalidValueError(DataQualityError):
    """Raised when a field has an invalid value."""
    def __init__(self, field, row_id, value):
        super().__init__(f"Invalid value '{value}' for field '{field}' in row {row_id}")
        self.field = field
        self.row_id = row_id
        self.value = value

def validate_order(row: dict[str, Any]) -> dict[str, Any]:
    required_fields = ["order_id", "region", "category", "amount"]
    for field in required_fields:
        if field not in row:
            raise MissingFieldError(field, row.get("order_id", "unknown"))
    
    try:
        amount = float(row["amount"])
    except (ValueError, TypeError) as e:
        raise InvalidValueError("amount", row["order_id"], row["amount"]) from e
    
    if amount < 0:
        raise InvalidValueError("amount", row["order_id"], row["amount"])
    
    return row

def process_orders(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    logger.info("Processing batch of %d rows", len(rows))
    valid, quarantined = [], []
    for row in rows:
        try:
            validate_order(row)
            valid.append(row)
        except DataQualityError as e:
            logger.warning("Data quality issue at row %s: %s", e.row_id, e)
            quarantined.append(row)
        except Exception:
            logger.exception("Something went wrong while processing row %r", row)
            raise
    
    logger.info("Finished processing batch: %d valid, %d quarantined", len(valid), len(quarantined))
    return valid, quarantined


#%%
test_orders = [
    {"order_id": 1, "region": "North", "category": "Electronics", "amount": 1200},
    {"order_id": 2, "region": "South", "category": "Electronics"},
    {"order_id": 3, "region": "North", "category": "Apparel",     "amount": "N/A"},
    {"order_id": 4, "region": "East",  "category": "Electronics", "amount": -500},
    {"order_id": 5, "region": "South", "category": "Apparel",     "amount": None},
    {"order_id": 6, "region": "North", "category": "Electronics", "amount": 850},
]

valid_orders, quarantined_orders = process_orders(test_orders)
# %%
