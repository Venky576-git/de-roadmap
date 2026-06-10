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
from collections import defaultdict
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
stats = defaultdict(lambda: {"total_revenue": 0, "order_count": 0})

filtered= [order for order in orders if order["category"] == "Electronics"]

for s in filtered:
    print(s)
    
# %%
#The * is a separator with no value — it just means 
# "everything after me must be passed as keyword arguments." 
# It's purely a contract enforced at the call site.

def summarize_orders(data, *, metric = "total_revenue", top_n = 3, **filters):
    stats = defaultdict(lambda: {"total_revenue": 0, "order_count": 0})
    region = filters.get("region")
    category = filters.get("category")

    print(region, category)

    filtered= [order for order in orders if order["category"] == category and order["region"] == region] 

    for r in filtered:
        print(r)
# %%

summarize_orders(
    orders,
    metric="total_revenue",
    top_n=5,
    region="North"
    # ,
    # category="Electronics"
)

# %%
def filter(orders, **filters):
    print(filters)
    filtered = [
        row
        for row in orders
        if all (row.get(k) == v for k, v in filters.items())
    ]
    for r in filtered:
        print(r)

# %%
filter(
    orders,
    region="North"
)