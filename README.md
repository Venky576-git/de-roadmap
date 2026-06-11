# de-roadmap
Added 
Day 3 of the 100-Day Data Engineering Roadmap. Practiced Python data structures (lists, tuples, sets, dicts) and comprehensions by reimplementing common SQL GROUP BY and set operations in pure Python — no pandas, no libraries beyond collections.

Day 4
Write functions with positional, keyword, default, keyword-only, *args, and **kwargs parameters
Avoid the mutable default argument trap (sentinel None pattern)
Add type hints with modern collection syntax (list[dict[str, Any]], X | None)
Split working code into a module + script pair and import across files
Use the if __name__ == "__main__": guard to make modules self-testable without polluting imports
Read the SQL mapping: module ↔ schema, function ↔ stored proc, type hints ↔ column type declarations, keyword args ↔ @name= calls