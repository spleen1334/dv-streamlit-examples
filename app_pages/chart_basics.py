import pandas as pd
import streamlit as st

from sales_data import load_sales


st.title("Chart basics")
st.write("Explore sales data, then turn a few pandas summaries into charts.")

sales = load_sales()
region = st.selectbox(
    "Region",
    ["All regions", *sorted(sales["region"].unique())],
    key="basics_region",
)

if region == "All regions":
    filtered_sales = sales
else:
    filtered_sales = sales[sales["region"] == region]

st.caption("Choose a region to rerun the app and update the table, metrics, and charts.")

revenue, units = st.columns(2)
revenue.metric("Revenue", f"${filtered_sales['revenue'].sum():,.2f}")
units.metric("Units sold", f"{filtered_sales['quantity'].sum():,}")

st.subheader("Sales data")
st.dataframe(filtered_sales, hide_index=True, width="stretch")

st.subheader("Revenue over time")
st.write("Group the filtered rows by month and sum revenue with pandas.")
monthly_revenue = filtered_sales.groupby(pd.Grouper(key="date", freq="MS"))[
    "revenue"
].sum()
st.line_chart(
    monthly_revenue,
    x_label="Month",
    y_label="Revenue (USD)",
)

st.subheader("Revenue by product")
st.write("Group the same rows by product to compare their revenue.")
product_revenue = filtered_sales.groupby("product")["revenue"].sum().sort_values(ascending=False)
st.bar_chart(
    product_revenue,
    x_label="Product",
    y_label="Revenue (USD)",
)
