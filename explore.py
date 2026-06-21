import pandas as pd

df = pd.read_csv('data/train.csv', encoding='latin1')

print(df.shape)
print(df.columns.tolist())
print(df.head())
print(df.info())
print(df.isnull().sum())

# Convert dates to proper datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

print(df['Order Date'].min(), "to", df['Order Date'].max())
print(df.dtypes)

# Total sales
print("Total Sales:", df['Sales'].sum())

# Sales by Category
print("\nSales by Category:")
print(df.groupby('Category')['Sales'].sum().sort_values(ascending=False))

# Sales by Region
print("\nSales by Region:")
print(df.groupby('Region')['Sales'].sum().sort_values(ascending=False))

# Top 5 Sub-Categories
print("\nTop 5 Sub-Categories by Sales:")
print(df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head())

# Monthly sales trend
df['Month'] = df['Order Date'].dt.to_period('M')
print("\nMonthly Sales (first 5):")
print(df.groupby('Month')['Sales'].sum().head())