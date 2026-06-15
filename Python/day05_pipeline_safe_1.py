
# Exercise — Block 1
# Take this small fragment:

# def safe_amount(row):
#     """Return the amount as a float, or 0.0 if missing/unparseable."""
#     return float(row["amount"])

# Rewrite it to handle these three real failure modes correctly:
# 1. Row is missing the "amount" key entirely → return 0.0
# 2. Row has "amount" but the value is a string like "N/A" that can't be parsed → return 0.0
# 3. Row has "amount" and it's a valid number → return that as float

#%%

def safe_amount(row):
    """Return the amount as a float, or 0.0 if missing/unparseable."""
    try:
        return float(row["amount"])
    except (KeyError, ValueError):
        return 0.0

print(safe_amount({"order_id": 1, "amount": 1200}))    # → 1200.0
print(safe_amount({"order_id": 2, "amount": "N/A"}))   # → 0.0
print(safe_amount({"order_id": 3}))                    # → 0.0

# %%
# BaseException
#  └── Exception                ← catch this or narrower; never BaseException
#       ├── LookupError
#       │    ├── KeyError       ← dict["missing"]
#       │    └── IndexError     ← lst[99] on a 3-element list
#       ├── ValueError          ← int("abc"), datetime.strptime mismatch
#       ├── TypeError           ← "x" + 1, None.upper()
#       ├── ArithmeticError
#       │    └── ZeroDivisionError
#       ├── OSError             ← file I/O, network (FileNotFoundError is a subclass)
#       └── RuntimeError

#%%
# Exercise — Block 2
# Build a small DQ hierarchy and a row validator that uses it.
# Part 1. Define three exception classes:

# DataQualityError(Exception) — base
# MissingFieldError(DataQualityError) — accepts field and row_id in __init__, carries both as attributes
# InvalidValueError(DataQualityError) — accepts field, row_id, and value in __init__, carries all three

# Part 2. Write a function validate_order(row: dict) -> dict that:

# Raises MissingFieldError if any of order_id, region, category, amount is missing from the row
# Raises InvalidValueError if amount is present but unparseable as a float — chain from the original ValueError
# Raises InvalidValueError if amount parses but is negative
# Returns the row unchanged if all checks pass

from typing import Any

class DataQualityError(Exception):
    """Base class for data quality errors."""

class MissingFieldError(DataQualityError):
    """Raised when a required field is missing."""
    def __init__(self, field, row_id):
        super().__init__(f"Missing field '{field}' in row {row_id}")
        self.field = field
        self.row_id = row_id

class InvalidValueError(DataQualityError):
    """Raised when a field has an invalid value."""
    def __init__(self, field, row_id, value):
        super().__init__(f"Invalid value '{value}' for field '{field}' in row {row_id}")
        self.field = field
        self.row_id = row_id
        self.value = value

def validate_order(row: dict[str, Any]) -> dict[str, Any]:
    required_fields = ["order_id", "region", "category", "amount"]
    for field in required_fields:
        if field not in row:
            raise MissingFieldError(field, row.get("order_id", "unknown"))
    
    try:
        amount = float(row["amount"])
    except (ValueError, TypeError) as e:
        raise InvalidValueError("amount", row["order_id"], row["amount"]) from e
    
    if amount < 0:
        raise InvalidValueError("amount", row["order_id"], row["amount"])
    
    return row

#%%
validate_order({"order_id": 1, "region": "North", "category": "Electronics", "amount": 1200})
# → returns the row

# validate_order({"order_id": 2, "region": "North", "category": "Electronics"})
# → raises MissingFieldError (amount missing)

# validate_order({"order_id": 3, "region": "North", "category": "Electronics", "amount": "N/A"})
# # → raises InvalidValueError (chained from ValueError)

# validate_order({"order_id": 4, "region": "North", "category": "Electronics", "amount": -50})
# → raises InvalidValueError

# validate_order({"order_id": 5, "region": "North", "category": "Electronics", "amount": None})