import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")

st.title("📊 Superstore Sales Dashboard")

# Connect to database
conn = sqlite3.connect('data/superstore.db')
df = pd.read_sql("SELECT * FROM sales", conn)
df['Order Date'] = pd.to_datetime(df['Order Date'])
conn.close()

# Sidebar filters
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[(df['Region'].isin(region)) & (df['Category'].isin(category))]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered_df['Order ID'].nunique():,}")
col3.metric("Avg Order Value", f"${filtered_df.groupby('Order ID')['Sales'].sum().mean():,.0f}")

# Sales by Category
st.subheader("Sales by Category")
cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
fig1 = px.bar(cat_sales, x='Category', y='Sales', color='Category')
st.plotly_chart(fig1, use_container_width=True)

# Monthly trend
st.subheader("Monthly Sales Trend")
filtered_df['Month'] = filtered_df['Order Date'].dt.to_period('M').astype(str)
monthly = filtered_df.groupby('Month')['Sales'].sum().reset_index()
fig2 = px.line(monthly, x='Month', y='Sales', markers=True)
st.plotly_chart(fig2, use_container_width=True)

# Top Sub-Categories
st.subheader("Top 10 Sub-Categories")
subcat = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
fig3 = px.bar(subcat, x='Sales', y='Sub-Category', orientation='h')
st.plotly_chart(fig3, use_container_width=True)

# Region breakdown
st.subheader("Sales by Region")
region_sales = filtered_df.groupby('Region')['Sales'].sum().reset_index()
fig4 = px.pie(region_sales, names='Region', values='Sales')
st.plotly_chart(fig4, use_container_width=True)

from prophet import Prophet

st.subheader("📈 7-Day Sales Forecast")

daily = df.groupby('Order Date')['Sales'].sum().reset_index()
daily.columns = ['ds', 'y']

model = Prophet()
model.fit(daily)

future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

fig5 = px.line(forecast, x='ds', y='yhat', title='Sales Forecast (Next 7 Days)')
fig5.add_scatter(x=daily['ds'], y=daily['y'], mode='lines', name='Actual Sales')
st.plotly_chart(fig5, use_container_width=True)

st.write("Forecasted values for next 7 days:")
st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(7).rename(
    columns={'ds': 'Date', 'yhat': 'Predicted Sales', 'yhat_lower': 'Lower Bound', 'yhat_upper': 'Upper Bound'}
))