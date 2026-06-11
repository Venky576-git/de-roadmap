# Block 3 — Modules and imports

# Every .py file IS a module
# That's the entire concept. There's no special "module" file type.
# The moment you save day04_transforms.py, that file is a module named day04_transforms that any other Python file can import from.

# Three import forms
# Given day04_transforms.py containing summarize_orders() and normalize_keys():

# Form 1 — import the whole module, access via dot notation
# import day04_transforms
# result = day04_transforms.summarize_orders(orders)

# # Form 2 — import specific names directly into the current namespace
# from day04_transforms import summarize_orders, normalize_keys
# result = summarize_orders(orders)

# # Form 3 — import with an alias (common for long or convention-named modules)
# import day04_transforms as t
# result = t.summarize_orders(orders)

"""Day 4 pipeline: exercise summarize_orders against the sample order dataset."""

from day04_transforms import summarize_orders


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


def main() -> None:
    print("=== Top 3 by total_revenue ===")
    for key, stats in summarize_orders(orders):
        print(key, stats)

    print("\n=== Top 5 by avg_order_value ===")
    for key, stats in summarize_orders(orders, metric="avg_order_value", top_n=5):
        print(key, stats)

    print("\n=== North region only — top 3 by order_count ===")
    for key, stats in summarize_orders(orders, metric="order_count", region="North"):
        print(key, stats)


if __name__ == "__main__":
    main()