# Day 4 — Functions & modules
# Today's scope (per the tracker): args/kwargs, type hints, imports, 
# splitting code into modules.

# Exercise — Block 1
# Write a function summarize_orders that:

# Takes a list of order dicts (use the same orders list from Problem 2)
# Has a keyword-only parameter metric defaulting to "total_revenue" — accepts one of "total_revenue", "order_count", "avg_order_value"
# Has a keyword-only parameter top_n defaulting to 3
# Accepts **filters — arbitrary field=value pairs to filter orders before aggregating (e.g. region="North", category="Electronics")
# Returns the top-N (region, category) pairs by the chosen metric, after applying filters


# %%
#The * is a separator with no value — it just means 
# "everything after me must be passed as keyword arguments." 
# It's purely a contract enforced at the call site.

from collections import defaultdict
from typing import Any

def summarize_orders(
    data: list[dict[str, Any]],     # list of dicts; keys are strings, values are heterogeneous
    *,
    metric: str = "total_revenue",
    top_n: int = 3,
    **filters: Any,                 # each filter value can be anything
) -> list[tuple[tuple[str, str], dict[str, float]]]:

    # for i in filters:
    #     data = [row for row in data if row.get(i) == filters.get(i)]
    
    data = [row for row in data                                 #all() returns True if every element in a given iterable is truthy
        if all(row.get(k) == v for k, v in filters.items())]    #if filters is empty, all() of an empty iterable is True, so every row passes through

    # Aggregate
    stats = defaultdict(lambda: {"total_revenue": 0, "order_count": 0})
    for row in data:
        key = (row["region"], row["category"])
        stats[key]["total_revenue"] += row["amount"]
        stats[key]["order_count"] += 1

    # Derive avg in a second pass
    for stat in stats.values():
        stat["avg_order_value"] = stat["total_revenue"] / stat["order_count"]

    # Sort by the chosen metric and slice
    return sorted(stats.items(),
                  key=lambda kv: kv[1][metric],
                  reverse=True)[:top_n]
# %%
if __name__ == "__main__":

    orders = [
        {"order_id": 1, "region": "North", "category": "Electronics", "amount": 1200},
        {"order_id": 2, "region": "South", "category": "Electronics", "amount": 800},
        {"order_id": 3, "region": "North", "category": "Apparel",     "amount": 300},
        {"order_id": 4, "region": "East",  "category": "Electronics", "amount": 1500},
        {"order_id": 5, "region": "North", "category": "Electronics", "amount": 600},
        {"order_id": 6, "region": "South", "category": "Apparel",     "amount": 450},
        {"order_id": 7, "region": "East",  "category": "Apparel",     "amount": 250},
        {"order_id": 8, "region": "North", "category": "Electronics", "amount": 900},
        {"order_id": 9, "region": "South", "category": "Electronics", "amount": 700},
        {"order_id": 10,"region": "East",  "category": "Electronics", "amount": 1100},
        {"order_id": 11,"region": "North", "category": "Apparel",     "amount": 350},
        {"order_id": 12,"region": "South", "category": "Apparel",     "amount": 200},
    ]

    for key, stats in summarize_orders(orders):
        print(" ", key, stats)

    # print(summarize_orders(orders))

    # summarize_orders(
    #     orders,
    #     metric="total_revenue",
    #     top_n=5,
    #     # region="North"
    #     # ,
    #     category="Electronics"
    # )

# %%
# Exercise — Block 2

# Add type hints to your summarize_orders exactly as shown above
# Add the docstring
# Save and watch Black auto-format the signature across multiple lines (Black formats long signatures vertically — recruiter-readable)
# Then try summarize_orders(orders, metric=99) and confirm Pylance puts a red squiggle on 99
# Hover over summarize_orders from a call site — see the docstring pop up