"""Day 5 pipeline: validate → quarantine → aggregate, with structured logging.

Production-shaped version of day04_pipeline. Adds:
- Layered exception handling with a DQ-aware quarantine step
- Structured logging configured ONCE at the entry point
- Two-stage flow with explicit valid/quarantined separation
"""

import logging

from day05_transforms import summarize_orders, validate_batch


# ---- Logging configured ONCE here, never in a library module ---------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


orders = [
    {"order_id": 1, "region": "North", "category": "Electronics", "amount": 1200},
    {"order_id": 2, "region": "South", "category": "Electronics"},                    # missing amount
    {"order_id": 3, "region": "North", "category": "Apparel",     "amount": "N/A"},   # unparseable
    {"order_id": 4, "region": "East",  "category": "Electronics", "amount": 1500},
    {"order_id": 5, "region": "North", "category": "Electronics", "amount": 600},
    {"order_id": 6, "region": "South", "category": "Apparel",     "amount": -50},     # negative
    {"order_id": 7, "region": "East",  "category": "Apparel",     "amount": 250},
    {"order_id": 8, "region": "North", "category": "Electronics", "amount": 900},
    {"order_id": 9, "region": "South", "category": "Electronics", "amount": None},    # null
    {"order_id": 10,"region": "East",  "category": "Electronics", "amount": 1100},
    {"order_id": 11,"region": "North", "category": "Apparel",     "amount": 350},
    {"order_id": 12,"region": "South", "category": "Apparel",     "amount": 200},
]


def main() -> None:
    logger.info("Pipeline starting")

    # Stage 1: validate + route bad rows to quarantine
    valid, quarantined = validate_batch(orders)
    if not valid:
        logger.critical("No valid rows after validation; aborting")
        return

    # Stage 2: aggregate the clean rows
    top_groups = summarize_orders(valid, metric="total_revenue", top_n=3)

    logger.info("Top 3 (region, category) by total_revenue:")
    for key, stats in top_groups:
        logger.info("  %s -> %s", key, stats)

    logger.info(
        "Pipeline complete: %d valid, %d quarantined, %d output groups",
        len(valid), len(quarantined), len(top_groups),
    )


if __name__ == "__main__":
    main()