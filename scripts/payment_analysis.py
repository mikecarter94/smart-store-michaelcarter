import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite DB
conn = sqlite3.connect(r'C:\Repos\smart-store-michaelcarter\Data\dw\smart_sales.db')

# Query for payment types in May
query = """
SELECT 
    sale_date,
    payment_type
FROM sale
WHERE sale_date LIKE '5/%'
"""

df = pd.read_sql(query, conn, parse_dates=['sale_date'])
print(df.head())
print(f"Number of rows returned: {len(df)}")

print(df)


# Count occurrences
payment_counts = df['payment_type'].value_counts()

# Output most common payment type
most_common = payment_counts.idxmax()
print(f"Most common payment type in May: {most_common}")
print(payment_counts)

# Optional: Save chart
plt.figure(figsize=(8, 5))
payment_counts.plot(kind='bar', title='Payment Type Usage in May')
plt.xlabel('Payment Type')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('charts/payment_type_may.png')  # optional image export
plt.show()

df.to_csv('Data/payment_types_may.csv', index=False)
