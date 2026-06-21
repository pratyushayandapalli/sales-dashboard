import pandas as pd
import sqlite3

# Load data
df = pd.read_csv('data/train.csv', encoding='latin1')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

# Create SQLite database and load data into it
conn = sqlite3.connect('data/superstore.db')
df.to_sql('sales', conn, if_exists='replace', index=False)

# Query 1
query1 = """
SELECT Category, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC
"""
print(pd.read_sql(query1, conn))

# Query 2
query2 = """
SELECT Region, COUNT(DISTINCT [Order ID]) as Num_Orders, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC
"""
print("\n", pd.read_sql(query2, conn))

# Query 3
query3 = """
SELECT strftime('%Y-%m', [Order Date]) as Month, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Month
ORDER BY Month
"""
print("\nMonthly Sales Trend:")
print(pd.read_sql(query3, conn))

# Query 4
query4 = """
SELECT [Sub-Category], SUM(Sales) as Total_Sales
FROM sales
GROUP BY [Sub-Category]
ORDER BY Total_Sales DESC
LIMIT 5
"""
print("\nTop 5 Sub-Categories:")
print(pd.read_sql(query4, conn))

# Close connection LAST
conn.close()