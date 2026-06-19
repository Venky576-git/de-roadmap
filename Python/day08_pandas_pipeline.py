#%%
"""Day 8 — pandas transforms: rebuild Day 6's pipeline."""

from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).parent / "data" / "orders_raw.csv"

df = pd.read_csv(
    CSV_PATH,
    encoding="utf-8-sig",
    dtype={"order_id": "Int64", "region": "string", "category": "string"},
    na_values=["N/A", "NULL", "-", "n/a"],
)

# Filter out rows that would be quarantined by Day 5 validation rules
valid = df[df["amount"].notna() & (df["amount"] >= 0)]

# Aggregate — replaces Day 4's defaultdict pattern entirely
summary = (
    valid.groupby(["region", "category"])
         .agg(
             total_revenue=("amount", "sum"),
             order_count=("amount", "count"),
             avg_order_value=("amount", "mean"),
         )
         .reset_index()
)

print("=== summary ===")
print(summary)
print(f"\nShape: {summary.shape}")
print(summary.columns.tolist())




# %%
# Exercise — Block 2
# nrich your summary with region metadata and demonstrate three join behaviors:

region_meta = pd.DataFrame({
    "region":    ["North", "South", "East", "West"],
    "manager":   ["Alice", "Bob", "Carol", "Dave"],
    "headcount": [12, 8, 15, 6],
})

print("\n=== INNER JOIN ===")
print(summary.merge(region_meta, on="region", how="inner"))

print("\n=== LEFT JOIN with validate='many_to_one' ===")
left_join = summary.merge(region_meta, on="region", how="left", validate="many_to_one")
print(left_join)

print("\n=== OUTER JOIN with indicator=True ===")
outer = summary.merge(region_meta, on="region", how="outer", indicator=True)
print(outer)

print("\n=== unmatched rows from the outer join ===")
print(outer[outer["_merge"] != "both"])



# %%
# Exercise — Block 3

# Top 3 — two ways, same result
print("\n=== top 3 via sort_values + head ===")
print(summary.sort_values("total_revenue", ascending=False).head(3))

print("\n=== top 3 via nlargest (faster on big frames) ===")
print(summary.nlargest(3, "total_revenue"))

# Pivot — region × category matrix of total_revenue (using the raw df)
print("\n=== pivot_table: region × category matrix ===")
pivot = df.pivot_table(
    index="region",
    columns="category",
    values="amount",
    aggfunc="sum",
    fill_value=0,
)
print(pivot)
# %%
