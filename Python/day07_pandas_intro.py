#%%
"""Day 7 — pandas basics: load orders_raw.csv and explore."""

from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).parent / "data" / "orders_raw.csv"

df = pd.read_csv(
    CSV_PATH,
    encoding="utf-8-sig",
    na_values=["N/A", "NULL", "None", "-", "n/a"],
)

print("=== type and shape ===")
print(f"type(df) = {type(df).__name__}")
print(f"df.shape = {df.shape}  (rows, columns)")

print("\n=== columns and dtypes ===")
print(df.dtypes)

print("\n=== full frame ===")
print(df)



# %%
print("\n=== head(3) ===")
print(df.head(3))

print("\n=== tail(3) ===")
print(df.tail(3))

print("\n=== info() ===")
df.info()

print("\n=== describe() — numeric only ===")
print(df.describe())

print("\n=== describe() — all columns ===")
print(df.describe(include="all"))

print("\n=== columns and index ===")
print(f"columns: {list(df.columns)}")
print(f"index:   {list(df.index)}")

# Experiment: set order_id as the index and observe the change
print("\n=== after set_index('order_id') ===")
df_indexed = df.set_index("order_id")
print(df_indexed.head(3))
print(f"columns now: {list(df_indexed.columns)}")
print(f"index now:   {list(df_indexed.index)}")






# %%
# Exercise — Block 3

df = pd.read_csv(
    CSV_PATH,
    encoding="utf-8-sig",
    dtype={
        "order_id": "Int64",
        "region": "string",
        "category": "string",
    },
    # Note: not specifying dtype for amount — let pandas infer float64,
    # because NaN handling is cleaner with the default float column for now
    na_values=["N/A", "NULL", "-", "n/a"],
    on_bad_lines="warn",
)

print("\n=== dtypes after explicit spec ===")
print(df.dtypes)

print("\n=== first 5 rows ===")
print(df.head())



# %%
# Exercise — Block 4
# rebuild a chunk of Day 6's logic in pandas selection

print("\n=== rows with missing amount (Day 6's MissingField cases) ===")
print(df[df["amount"].isna()])

print("\n=== rows with negative amount (Day 6's invalid-value-after-parsing case) ===")
print(df[df["amount"] < 0])

print("\n=== ALL bad rows in one filter (Day 6's full quarantine condition) ===")
bad_mask = df["amount"].isna() | (df["amount"] < 0)
print(df[bad_mask])

print("\n=== valid rows only ===")
valid = df[~bad_mask]
print(valid)
print(f"\n{len(valid)} valid out of {len(df)} total")

print("\n=== from valid rows: only region, category, amount where region is North or East ===")
print(valid.loc[valid["region"].isin(["North", "East"]), ["region", "category", "amount"]])
# %%
