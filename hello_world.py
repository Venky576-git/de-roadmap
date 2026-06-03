import pandas as pd

# Creating a simple DataFrame (the core data structure in Pandas)
data = {
    'Task': ['Install Python', 'Create venv', 'Install Pandas', 'Freeze Requirements'],
    'Status': ['Done', 'Done', 'Done', 1]
}

df = pd.DataFrame(data)

print("Hello, Data Engineering World! Here is my Day 1 progress:\n")
print(df)