# %%
x = 10              # int
pi = 3.14           # float
name = "orders"    # str
is_active = True    # bool (capital T/F — not like SQL)
type(x)             # <class 'int'>

row_count = 1_000_000   # underscores allowed for readability
price = float(x)        # explicit cast
print(price, row_count)
print(row_count)

# %%
status = "failed"

if status == "success":
    print("ok")
elif status == "warning":
    print("check logs")
else:
    print("alert on-call")
# %%
# for is always "for each" — like a cursor in SQL, but idiomatic
for n in [1, 2, 3, 4, 5]:
    if n % 2 == 0:
        print("continue")
        continue          # skip
    if n > 4:
        print("Enters the BREAK")
        break             # stop
    print(n)
# %%
for i in range(5):   # 0 to 4
    print(i)1



# %%
def add(a, b):
    return a + b
# %%
print(add(3, 5))


# %%
## Default parameters — like optional SQL proc parameters:
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

print(greet("Sai"))                          # "Hello, Sai"
print(greet("Sai", greeting="Hi"))
print(greet("Sai", "Hi"))
           # "Hi, Sai"


# %%
# Multiple returns via tuple — Python returns one thing, but that one thing can be a tuple you unpack:
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([4, 9, 1, 7])
print(lo, hi)        # lo=1, hi=9

# %%
# Type hints don't enforce anything at runtime (they're documentation + IDE help)
def add(a: int, b: int) -> int:
    return a + b

# The type hints say:
# a should be an int
# b should be an int
# the function should return an int
# But Python won't stop you from doing this:

print(add("Hello, ", "world"))
print(add(13, 12))

# %%
# If you really want types enforced while the program runs, you need additional libraries or manual checks:
def add(a: int, b: int) -> int:
    if not isinstance(a, int):
        raise TypeError("a must be int")
    if not isinstance(b, int):
        raise TypeError("b must be int")
    return a + b

print(add("Hello, ", "world"))

# Type hints are mainly for humans and tools, not for Python itself.

# %%
#Step 4 — Docstrings
# A docstring is a string literal sitting as the first statement inside a function. 
# Triple-quoted. It's what help(your_function) prints. The community convention for DE work is Google style — clear sections, easy to read:
def add(a: int, b: int) -> int:
    """Return the sum of two integers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The integer sum of a and b.
    """
    return a + b

help(add)

# %%
"""Day 2 practice — three small functions with docstrings."""


def row_quality_score(total_rows: int, null_rows: int) -> float:
    """Compute the percentage of non-null rows in a dataset.

    Args:
        total_rows: Total number of rows ingested.
        null_rows: Number of rows containing at least one null in a key column.

    Returns:
        A float between 0 and 100 representing the percent of clean rows.
        Returns 0.0 when total_rows is 0 to avoid division by zero.
    """
    if total_rows == 0:
        return 0.0
    clean = total_rows - null_rows
    return (clean / total_rows) * 100


def classify_load_size(row_count: int) -> str:
    """Bucket a row count into a human-readable load size.

    Args:
        row_count: Number of rows in a single pipeline run.

    Returns:
        One of "small", "medium", "large", or "huge".
    """
    if row_count < 10_000:
        return "small"
    elif row_count < 1_000_000:
        return "medium"
    elif row_count < 100_000_000:
        return "large"
    else:
        return "huge"


def summarize_run(table_name: str, rows: int, seconds: float) -> dict:
    """Build a summary record for a pipeline run.

    Args:
        table_name: The target table that was loaded.
        rows: Number of rows written.
        seconds: Wall-clock duration of the run.

    Returns:
        A dict with the table name, row count, duration, throughput
        (rows per second), and a load-size bucket.
    """
    throughput = rows / seconds if seconds > 0 else 0
    return {
        "table": table_name,
        "rows": rows,
        "seconds": seconds,
        "rows_per_sec": round(throughput, 2),
        "size_bucket": classify_load_size(rows),
    }


if __name__ == "__main__":
    print(row_quality_score(1000, 23))
    print(classify_load_size(2_500_000))
    print(summarize_run("dim_customer", 500_000, 12.4))

# Claude link (https://claude.ai/share/f3d8aa79-7611-4713-9c20-d84badc1e290)