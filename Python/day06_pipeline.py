"""Day 6 pipeline: read messy CSV → normalize → validate → aggregate → write JSON.

Five-stage pipeline. Each stage has a single responsibility:
  1. load CSV (strings, including null tokens like 'N/A' and '')
  2. normalize null tokens (remove keys representing missing data)
  3. validate + quarantine (Day 5 layered exception handling)
  4. coerce types (amount: str → float, ready for arithmetic)
  5. aggregate + write outputs
"""

import logging
from pathlib import Path

from day05_transforms import summarize_orders, validate_batch
from day06_io import (
    load_orders_csv,
    normalize_nulls,
    write_quarantine_json,
    write_summary_json,
)


# ---- Logging configured ONCE at the entry point ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


# ---- Paths -----------------------------------------------------------------
HERE = Path(__file__).parent
CSV_PATH = HERE / "data" / "orders_raw.csv"
SUMMARY_PATH = HERE / "output" / "summary.json"
QUARANTINE_PATH = HERE / "output" / "quarantine.json"


def main() -> None:
    logger.info("Pipeline starting")

    # 1. Load CSV (everything comes back as strings)
    raw_rows = load_orders_csv(CSV_PATH)

    # 2. Normalize null tokens — empty string, "N/A", "NULL" → key removed
    normalized = [normalize_nulls(row) for row in raw_rows]

    # 3. Validate and route bad rows to quarantine
    valid, quarantined = validate_batch(normalized)
    if not valid:
        logger.critical("No valid rows after validation; aborting")
        return

    # 4. Coerce amount from CSV string to float, in place
    #    Safe to do this post-validation: every row in `valid` has parseable amount
    for row in valid:
        row["amount"] = float(row["amount"])

    # 5. Aggregate the clean rows and persist outputs
    top_groups = summarize_orders(valid, metric="total_revenue", top_n=3)
    write_summary_json(top_groups, SUMMARY_PATH)
    write_quarantine_json(quarantined, QUARANTINE_PATH)

    logger.info(
        "Pipeline complete: read %d, valid %d, quarantined %d, output groups %d",
        len(raw_rows), len(valid), len(quarantined), len(top_groups),
    )


if __name__ == "__main__":
    main()