"""Day 8 — pandas pipeline: full rewrite of day06_pipeline.py in pandas."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd


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
SUMMARY_PATH = HERE / "output" / "summary_pandas.json"
QUARANTINE_PATH = HERE / "output" / "quarantine_pandas.json"


def main() -> None:
    logger.info("Pipeline starting")
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 1. LOAD — read_csv handles encoding, BOM, null tokens, type coercion, schema
    df = pd.read_csv(
        CSV_PATH,
        encoding="utf-8-sig",
        dtype={"order_id": "Int64", "region": "string", "category": "string"},
        na_values=["N/A", "NULL", "-", "n/a"],
    )
    logger.info("Read %d rows", len(df))

    # 2. CLASSIFY — vectorized CASE WHEN: which rows are bad, and why
    bad_mask = df["amount"].isna() | (df["amount"] < 0)
    quarantined = df[bad_mask].copy()
    quarantined["reason"] = np.select(
        [quarantined["amount"].isna(), quarantined["amount"] < 0],
        ["missing or null amount", "negative amount"],
        default="unknown",
    )
    valid = df[~bad_mask].copy()

    logger.info(
        "Validation complete: %d valid, %d quarantined", len(valid), len(quarantined)
    )

    if valid.empty:
        logger.critical("No valid rows; aborting")
        return

    # 3. AGGREGATE — groupby + named agg + top-N, one chained expression
    summary = (
        valid.groupby(["region", "category"])
             .agg(
                 total_revenue=("amount", "sum"),
                 order_count=("amount", "count"),
                 avg_order_value=("amount", "mean"),
             )
             .reset_index()
             .nlargest(3, "total_revenue")
    )

    # 4. WRITE — to_json with records orient gives a flat array of dicts
    summary.to_json(
        SUMMARY_PATH, orient="records", indent=2, force_ascii=False
    )
    quarantined.to_json(
        QUARANTINE_PATH, orient="records", indent=2, force_ascii=False
    )

    logger.info("Wrote summary (%d rows) to %s", len(summary), SUMMARY_PATH.name)
    logger.info("Wrote quarantine (%d rows) to %s", len(quarantined), QUARANTINE_PATH.name)
    logger.info("Pipeline complete")


if __name__ == "__main__":
    main()