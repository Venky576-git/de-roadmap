#%%
"""Day 9 — pandas cleaning: inspect the dirty orders dataset."""

from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).parent / "data" / "orders_dirty.csv"

# Note: NOT parsing dates here — Day 9 covers explicit date handling in Block 2
df = pd.read_csv(
    CSV_PATH,
    encoding="utf-8-sig",
    dtype={
        "order_id": "Int64",
        "region": "string",
        "category": "string",
        "customer_email": "string",
        "notes": "string",
        "order_date": "string",
    },
    na_values=["N/A", "NULL", "-", "n/a"],
)

print("=== shape ===")
print(df.shape)

print("\n=== head ===")
print(df.head(8))

print("\n=== info ===")
df.info()

print("\n=== missing per column — count ===")
print(df.isna().sum())

print("\n=== missing per column — fraction ===")
print(df.isna().mean().round(2))



# %%
print("\n=== before parsing — order_date dtype ===")
print(df["order_date"].dtype)
print(df["order_date"].head(8))

# Approach A: try ISO format, then US format, combine
parsed_iso = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
parsed_us  = pd.to_datetime(df["order_date"], format="%m/%d/%Y", errors="coerce")
df["order_date"] = parsed_iso.fillna(parsed_us)

print("\n=== after parsing — order_date dtype ===")
print(df["order_date"].dtype)
print(df["order_date"].head(8))

print("\n=== which rows still have unparseable dates? ===")
print(df[df["order_date"].isna()][["order_id", "order_date"]])

print("\n=== .dt accessor demo ===")
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["weekday_name"] = df["order_date"].dt.day_name()
print(df[["order_id", "order_date", "order_year", "order_month", "weekday_name"]].head(8))


# %%
print("\n=== duplication audit ===")
print(f"Total rows:                       {len(df)}")
print(f"Distinct order_ids:               {df['order_id'].nunique()}")
print(f"Fully duplicated rows (all cols): {df.duplicated().sum()}")
print(f"Duplicated by order_id alone:     {df.duplicated(subset=['order_id']).sum()}")

print("\n=== ALL rows involved in any order_id duplication ===")
print(
    df[df.duplicated(subset=["order_id"], keep=False)]
      .sort_values("order_id")
      [["order_id", "order_date", "region", "category", "amount"]]
)

# Dedup: most recent wins per order_id
df = (
    df.sort_values("order_date")
      .drop_duplicates(subset=["order_id"], keep="last")
      .reset_index(drop=True)
)

print(f"\n=== after dedup: {len(df)} rows ===")
print(df[["order_id", "order_date", "region", "amount"]].head(10))


#%%
print("\n=== string normalization ===")
print("Before — unique regions:    ", df["region"].unique())
print("Before — unique categories: ", df["category"].unique())

df["region"]         = df["region"].str.strip().str.lower()
df["category"]       = df["category"].str.strip().str.lower()
df["customer_email"] = df["customer_email"].str.strip().str.lower()
df["notes"]          = df["notes"].str.strip()

print("\nAfter — unique regions:    ", df["region"].unique())
print("After — unique categories: ", df["category"].unique())

# Build an email-domain column for downstream analysis
df["email_domain"] = df["customer_email"].str.split("@", expand=True)[1]

# Audit: which orders have NOREPLY emails (you'd typically exclude these from customer metrics)
noreply = df[df["customer_email"].str.startswith("noreply", na=False)]
print(f"\nNOREPLY orders found: {len(noreply)}")
print(noreply[["order_id", "customer_email"]])

# Audit: which orders are flagged RUSH or Refund in notes
flagged = df[df["notes"].str.contains("rush|refund", case=False, na=False)]
print(f"\nFlagged orders: {len(flagged)}")
print(flagged[["order_id", "notes"]])

print("\n=== final shape ===")
print(df.shape)
print("\n=== final head ===")
print(df.head(8))
# %%
