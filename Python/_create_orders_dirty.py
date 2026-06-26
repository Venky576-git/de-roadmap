"""Generate a deliberately messy orders CSV for Day 9 cleaning exercises."""

from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

content = """\
order_id,order_date,region,category,amount,customer_email,notes
1,2024-01-15,North,Electronics,1200,alice@example.com,Big sale
1,2024-01-15,North,Electronics,1200,alice@example.com,Big sale
2,2024-01-16,South,Electronics,,bob@example.com,N/A
3,2024-01-17,North,apparel,N/A,Carol@Example.COM,
4,01/18/2024,East,Electronics,1500,dave@example.com,RUSH
5,2024-01-19,North ,Electronics,600,eve@example.com,
6,2024-01-20,South,Apparel,-50,frank@example.com,Refund
7,2024-01-21,East,"Apparel, Sale",250,grace@example.com,
8,2024-01-22,North,Electronics,900,henry@example.com,
8,2024-01-22,North,Electronics,900,henry@example.com,
9,2024-01-23,South,Electronics,NULL,ivan@example.com,
10,2024-01-24,East,Electronics,1100,judy@example.com,Bulk order
11,01/25/2024,North,Apparel,350,karen@example.com,
12,2024-01-26,south,Apparel,200,liam@example.com,
13,not-a-date,East,Electronics,800,mary@example.com,
14,2024-01-28,East,electronics,950,NOREPLY@example.com,
"""

(DATA_DIR / "orders_dirty.csv").write_text(content, encoding="utf-8-sig")
print(f"Wrote {DATA_DIR / 'orders_dirty.csv'}")