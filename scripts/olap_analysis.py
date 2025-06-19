import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect('smart_sales.db')

# Optional: Preview tables
print(pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn))

# Step 1: Write and execute SQL query to join product and sales
query = """
SELECT 
    s.sale_date,
    s.sale_amount,
    p.category
FROM sales s
JOIN product p ON s.product_id = p.product_id
WHERE p.category = 'Electronics'
"""

# Step 2: Load data into DataFrame
df = pd.read_sql(query, conn, parse_dates=['sale_date'])

# Step 3: Filter for the month of May
df['month'] = df['sale_date'].dt.month
may_electronics = df[df['month'] == 5]

# Step 4: Perform OLAP-style aggregations
average_sale = may_electronics['sale_amount'].mean()
total_sale = may_electronics['sale_amount'].sum()
count = may_electronics['sale_amount'].count()

# Step 5: Output the results
print(f"Total Sales in May (Electronics): ${total_sale:.2f}")
print(f"Average Sale Amount in May (Electronics): ${average_sale:.2f}")
print(f"Number of Transactions: {count}")

# OLAP-style cube: by category and month
df['month'] = df['sale_date'].dt.month
cube = df.groupby(['category', 'month']).agg(
    total_sales=('sale_amount', 'sum'),
    average_sale=('sale_amount', 'mean'),
    transactions=('sale_amount', 'count')
).reset_index()

# View May Electronics data for comparison
print(cube[(cube['category'] == 'Electronics') & (cube['month'] == 5)])

import matplotlib.pyplot as plt

# Group by category and sum sale amounts
revenue_by_category = df.groupby('category')['sale_amount'].sum().sort_values()

# Plot
revenue_by_category.plot(kind='barh', figsize=(10, 6), title="Total Revenue by Product Category")
plt.xlabel('Total Revenue')
plt.ylabel('Product Category')
plt.tight_layout()
plt.show()

# Ensure sale_date is datetime and set to month
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['month'] = df['sale_date'].dt.to_period('M')

# Group by month and sum sale_amount
sales_trend = df.groupby('month')['sale_amount'].sum()

# Plot
sales_trend.plot(kind='line', figsize=(10, 6), marker='o', title="Monthly Sales Trend")
plt.ylabel('Total Sales')
plt.xlabel('Month')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Create pivot table
pivot = pd.pivot_table(
    df,
    values='sale_amount',
    index='product_id',
    columns='region',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='Total'
)

print(pivot)
