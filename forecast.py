import pandas as pd
import sqlite3
from prophet import Prophet

conn = sqlite3.connect('data/superstore.db')
df = pd.read_sql("SELECT [Order Date], Sales FROM sales", conn)
conn.close()

df['Order Date'] = pd.to_datetime(df['Order Date'])

# Aggregate daily sales
daily = df.groupby('Order Date')['Sales'].sum().reset_index()
daily.columns = ['ds', 'y']  # Prophet requires these exact column names

# Train model
model = Prophet()
model.fit(daily)

# Forecast next 7 days
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7))