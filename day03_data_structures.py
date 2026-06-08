## 1. Lists — your iterable rowset
# %%
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# Add / remove
nums.append(7)           # add to end
print(nums)
nums.extend([8, 9])      # add many
print(nums)
nums.insert(0, 99)       # insert at index
print(nums)
print(nums.pop())              # remove + return last
print(nums)
nums.remove(1)           # remove first occurrence of value 1
print(nums)

# Sort
nums.sort()
print(nums)

# %%

print(sorted(nums))
print(sorted(nums, reverse=True))
print(nums.sort(key=lambda x: x % 3)) # Python groups numbers according to their x % 3 value: # sort by a key (very common)
print(nums)

# %%

# Slicing — works on lists, tuples, strings
print(nums)
 
print(nums[:3])     # first 3

print(nums[-3:])    # last 3
    
print(nums[::-1] )  # reversed
  
print(nums[::2])    # every other one

print(nums)

##################################   2. Tuples — immutable records  ##############################
# Fixed shape, ordered, indexable. The two reasons you reach for them:
# Reason 1 — multiple return values. Functions can return tuples, which you unpack on the receiving side:

# Reason 2 — composite dict keys / set members. Tuples are hashable (lists aren't), 
# so you can use them as keys. This is the Python equivalent of a composite primary key: 
    # Why not use a list?
    # Lists are mutable ❌
    # Mutable objects are not hashable ❌
    # Dictionary keys must be hashable ✅


# %%

def stats(nums):
    return min(nums), max(nums), sum(nums) / len(nums)

lo, hi, avg = stats([1, 2, 3, 4, 5])

print(lo, hi, avg)

# %%
revenue = {
    ("APAC", 2024): 1.2,
    ("EMEA", 2024): 0.8,
}
revenue[("APAC", 2024)]   # 1.2
# %%
for name, age in [("Alice", 30), ("Bob", 25)]:
    print(name, age)




################################################### 3. Sets — your SQL set operations, natively #############################################
# Unordered, unique, O(1) membership tests. This one will feel like home — every SQL set operation has a direct operator:
# %%
emails_a = {"alice@x.com", "bob@x.com", "carol@x.com"}
emails_b = {"bob@x.com",   "dave@x.com"}

print(emails_a | emails_b)    # UNION         → all unique
print(emails_a & emails_b)    # INTERSECT     → in both
print(emails_a - emails_b)    # EXCEPT / MINUS → in a but not b
print(emails_a ^ emails_b)    # XOR           → in either, not both

# %%
# Two killer use cases:

#1. Deduplicate fast
# unique_ids = set(ids)        # done.

#2. Fast IN lookup — orders of magnitude faster than `in list`
# valid_regions = {"APAC", "EMEA", "AMER"}
# if row["region"] in valid_regions:    # O(1) — list would be O(n)
    
# If you ever build a filter against tens of thousands of values, 
# a set lookup vs list lookup is the difference between "instant" and "lunch break."

###########################################  4. Dicts — the workhorse  ###############################################

# Key → value. This is what you'll use most. Master these patterns:

# %%
row = {"id": 1, "name": "Alice", "amount": 100, "active": False}

# Safe access — no KeyError
print(row["id"])
# print(row["missing"])  ## Throws error as "missing" Key is not exists
print(row.get("missing"))          # None
print(row.get("missing", 0))        # default value

# %%
# Iterate
# for k, v in row.items():
#     ...

# Merge (Python 3.9+)
default = {"region": "APAC", "active": True}
combined = row | default  
print(combined)     # row's keys win on conflict
# Older syntax:
combined_Old = {**default, **row}
print(combined_Old)

# %%
# Conditional update
row.setdefault("active", True)   # only sets if "active" missing
print(row)
row.setdefault("state", "NA")   # only sets if "active" missing
print(row)

##################### 5. Comprehensions — your new SELECT … WHERE ######################

"""
# SELECT amount FROM sales WHERE amount > 100
big = [s["amount"] for s in sales if s["amount"] > 100]

# SELECT DISTINCT region FROM sales
regions = {s["region"] for s in sales}

# Build a lookup: {region_name: region_id}
lookup = {r["name"]: r["id"] for r in regions}

# CASE WHEN — note the if/else goes BEFORE `for` here
flags = ["high" if s["amount"] > 100 else "low" for s in sales]

# Nested — feels like a CROSS JOIN
pairs = [(x, y) for x in [1, 2, 3] for y in ["a", "b"]]

Two rules to remember about placement:

1. if after the for = filter (WHERE)
2. if/else before the for = conditional expression (CASE WHEN)

"""

###############################   Practice exercise  ######################################
# %%
sales = [
    {"region": "APAC", "rep": "Alice", "amount": 120, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 80,  "month": "Jan"},
    {"region": "APAC", "rep": "Alice", "amount": 50,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 200, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 30,  "month": "Feb"},
    {"region": "APAC", "rep": "Dan",   "amount": 75,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 150, "month": "Feb"},
]
defaults = {"region": "APAC", "active": True}

for K, Val in defaults.items():
    print(K, Val)

# %%
# List of Dicts
defaults = [{"region": "APAC", "active": True},
            {"region": "APA", "active": False}]

for d in defaults:
    for K, Val in d.items():
        print(K, Val)

# %%
defaults = {"region": "APAC", "active": True}
for i, row in enumerate(sales):
    sales[i] = defaults | row

print(sales)
# %%
# Level 1 — Basic GROUP BY (use defaultdict)

# SELECT region, SUM(amount) FROM sales GROUP BY region;
# %%
from collections import defaultdict, Counter

sales = [
    {"region": "APAC", "rep": "Alice", "amount": 120, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 80,  "month": "Jan"},
    {"region": "APAC", "rep": "Alice", "amount": 50,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 200, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 30,  "month": "Feb"},
    {"region": "APAC", "rep": "Dan",   "amount": 75,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 150, "month": "Feb"},
]

# defaultdict — auto-creates missing keys with a default. The GROUP BY accumulator.
totals = defaultdict(int)
# SELECT region, SUM(amount) FROM sales GROUP BY region;
for s in sales:
    totals[s["region"]] += s["amount"]
print(totals)

# %%
# Level 2 — Multi-aggregation (sum, count, avg per region)
# SELECT region, SUM(amount), COUNT(*), AVG(amount) FROM sales GROUP BY region;
from collections import defaultdict

sum = defaultdict(int)
count = defaultdict(int)

for s in sales:
    sum[s["region"]] += s["amount"]
    count[s["region"]] += 1 

print(sum, count)
type(sum)

for region in sum:
    avg = sum[region] / count[region]
    print(
        f"{region}: "
        f"sum={sum[region]}, "
        f"count={count[region]}, "
        f"avg={avg:.2f}"
    )  


# %%
agg = defaultdict(lambda: {"sum": 0, "count": 0})

for s in sales:
    r = agg[s["region"]]
    r["sum"]   += s["amount"]
    r["count"] += 1
    #print(id(r))
    
for region, v in agg.items():
    avg = v["sum"] / v["count"]
    print(f"{region}: sum={v['sum']}, count={v['count']}, avg={avg:.2f}")
    #print(id(agg[region]))

# %%
############ Level 3 —GROUP BY + HAVING. Find regions where SUM(amount) > 150.

# SELECT region, SUM(amount) FROM sales GROUP BY region HAVING SUM(amount) > 150;
from collections import defaultdict

sales = [
    {"region": "APAC", "rep": "Alice", "amount": 120, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 80,  "month": "Jan"},
    {"region": "APAC", "rep": "Alice", "amount": 50,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 200, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 30,  "month": "Feb"},
    {"region": "APAC", "rep": "Dan",   "amount": 75,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 150, "month": "Feb"},
]

TotalAmount = defaultdict(int)

for n in sales:
    TotalAmount[n["region"]] += n["amount"] 

print(TotalAmount)

for k, v in TotalAmount.items(): 
    if v  > 150:
        print(k, v)

result = [(k, v) for k, v in TotalAmount.items() if v > 150]
print(result)

result = {k : v for k, v in TotalAmount.items() if v > 150}
print(result)

print(type(result))



    
# %%

####################  Level 4 — composite key GROUP BY (the last main exercise).

# SELECT region, month, SUM(amount) FROM sales GROUP BY region, month;

# The trick: SQL lets you group by multiple columns natively. 
# Python needs a single key per group, so you compose one — using a tuple. 
# Remember tuples are hashable, so (region, month) works as a dict key.

# %%

from collections import defaultdict

sales = [
    {"region": "APAC", "rep": "Alice", "amount": 120, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 80,  "month": "Jan"},
    {"region": "APAC", "rep": "Alice", "amount": 50,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 200, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 30,  "month": "Feb"},
    {"region": "APAC", "rep": "Dan",   "amount": 75,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 150, "month": "Feb"},
]

total_amount = defaultdict(int)

for s in sales:
    total_amount[(s["region"], s["month"])] += s["amount"]
    
print(total_amount)

second_way = defaultdict(int)

for s in sales:
    key = (s["region"], s["month"])
    second_way[key] += s["amount"]
    
print(second_way)


################ 5. set difference

# Which reps sold in APAC but not in EMEA?

# SELECT DISTINCT rep FROM sales WHERE region = 'APAC'
# EXCEPT
# SELECT DISTINCT rep FROM sales WHERE region = 'EMEA';

from collections import defaultdict

sales = [
    {"region": "APAC", "rep": "Alice", "amount": 120, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 80,  "month": "Jan"},
    {"region": "APAC", "rep": "Alice", "amount": 50,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 200, "month": "Jan"},
    {"region": "EMEA", "rep": "Bob",   "amount": 30,  "month": "Feb"},
    {"region": "APAC", "rep": "Dan",   "amount": 75,  "month": "Feb"},
    {"region": "AMER", "rep": "Carol", "amount": 150, "month": "Feb"},
]


apac_reps = {s["rep"] for s in sales if s["region"] == "APAC"}
emea_reps = {s["rep"] for s in sales if s["region"] == "EMEA"}

# print(apac_reps)
# print(emea_reps)

print(apac_reps - emea_reps)
