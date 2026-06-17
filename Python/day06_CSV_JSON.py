#%%
"""Smoke test for Block 1 — paths, with statements, encodings."""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

# Ensure output dir exists (idempotent)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Write a tiny file with explicit UTF-8 encoding
sample_path = OUTPUT_DIR / "hello.txt"
with open(sample_path, "w", encoding="utf-8") as f:
    f.write("Hello, José\n")
    f.write("Second line\n")

# Read it back
with open(sample_path, "r", encoding="utf-8") as f:
    content = f.read()

print(f"Wrote to: {sample_path}")
print(f"Path metadata: name={sample_path.name}, stem={sample_path.stem}, suffix={sample_path.suffix}")
print(f"Parent dir: {sample_path.parent}")
print(f"File size: {sample_path.stat().st_size} bytes")
print("---")
print(content)

# Experiment: what does the default encoding do on your machine?
print("\n--- Default encoding test ---")
import locale
print(f"Platform default encoding: {locale.getencoding()}")

print(sample_path.read_bytes())  # raw bytes






#%%
# run once to generate the test input
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

csv_content = """\
order_id,region,category,amount
1,North,Electronics,1200
2,South,Electronics,
3,North,Apparel,N/A
4,East,Electronics,1500
5,North,Electronics,600
6,South,Apparel,-50
7,East,"Apparel, Sale",250
8,North,Electronics,900
9,South,Electronics,NULL
10,East,Electronics,1100
11,North,Apparel,350
12,South,Apparel,200
"""

# Write with a BOM prefix (simulates an Excel export)
csv_path = DATA_DIR / "orders_raw.csv"
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    f.write(csv_content)

print(f"Wrote {csv_path} ({csv_path.stat().st_size} bytes)")
print(f"First 20 raw bytes: {csv_path.read_bytes()[:20]}")







# %%
"""Demo: read orders_raw.csv and observe how DictReader handles it."""

import csv
from pathlib import Path

CSV_PATH = Path(__file__).parent / "data" / "orders_raw.csv"

with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    headers = reader.fieldnames

print(f"Read {len(rows)} rows.")
print(f"Headers: {headers}")
print()
for r in rows:
    print(r)










# %%
"""Reshape Day 5 summary output and write it as JSON."""

import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Pretend this came from summarize_orders(valid_rows) — using Day 5's expected output
summary = [
    (("North", "Electronics"), {"total_revenue": 2700, "order_count": 3, "avg_order_value": 900.0}),
    (("East",  "Electronics"), {"total_revenue": 2600, "order_count": 2, "avg_order_value": 1300.0}),
    (("North", "Apparel"),     {"total_revenue": 350,  "order_count": 1, "avg_order_value": 350.0}),
]


def reshape_summary_for_json(summary):
    """[((region, category), stats), ...] → [{"region": ..., "category": ..., **stats}, ...]"""
    return [
        {"region": region, "category": category, **stats}
        for (region, category), stats in summary
    ]


reshaped = reshape_summary_for_json(summary)
print("Reshaped (in-memory):")
print(reshaped)
print()

# Write JSON file — pretty, no NaN allowed, international-friendly
summary_path = OUTPUT_DIR / "summary.json"
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(reshaped, f, indent=2, ensure_ascii=False, allow_nan=False)

print(f"Wrote {summary_path}")
print(f"File size: {summary_path.stat().st_size} bytes")
print()

# Read it back and confirm round-trip
with open(summary_path, "r", encoding="utf-8") as f:
    roundtripped = json.load(f)

print("Round-tripped (from disk):")
print(roundtripped)
print()
print(f"Round-trip preserves equality? {reshaped == roundtripped}")



