"""Explore how forms batch filter changes before updating a chart."""

import altair as alt
import pandas as pd
import streamlit as st

from sales_data import load_sales


st.title("Interactive sales analysis")
st.write(
    "Compare monthly revenue by product. Choose your filters, then select "
    "**Apply filters** to update the results together."
)

sales = load_sales()
products = sorted(sales["product"].unique().tolist())
first_date = sales["date"].min().date()
last_date = sales["date"].max().date()

# Keep applied filters separate from the form's draft values.
if "analysis_applied" not in st.session_state:
    st.session_state.analysis_applied = (products, (first_date, last_date))

applied_products, applied_dates = st.session_state.analysis_applied
with st.form("analysis_filters"):
    st.subheader("Filters")
    selected_products = st.multiselect(
        "Products", products, default=applied_products, key="analysis_products"
    )
    selected_dates = st.date_input(
        "Date range",
        value=applied_dates,
        min_value=first_date,
        max_value=last_date,
        key="analysis_dates",
    )
    submitted = st.form_submit_button("Apply filters", type="primary")

if submitted:
    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        st.session_state.analysis_applied = (selected_products, tuple(selected_dates))
    else:
        st.warning("Choose both a start and an end date, then apply your filters.")

applied_products, (start_date, end_date) = st.session_state.analysis_applied
st.caption(
    f"Showing: {', '.join(applied_products) if applied_products else 'No products'}"
    f" · {start_date:%b %d, %Y} – {end_date:%b %d, %Y}"
)

filtered = sales[
    sales["product"].isin(applied_products)
    & sales["date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))
]

if not applied_products:
    st.info("No products selected. Choose at least one product and apply your filters.")
elif filtered.empty:
    st.info("No sales match this date range. Try a different range and apply your filters.")
else:
    monthly = (
        filtered.assign(month=filtered["date"].dt.to_period("M").dt.to_timestamp())
        .groupby(["month", "product"], as_index=False, observed=True)["revenue"]
        .sum()
        .sort_values(["month", "product"])
    )
    st.subheader("Monthly revenue by product")
    st.caption("Revenue is summed across regions for the selected dates, in US dollars.")
    chart = (
        alt.Chart(monthly)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("month:T", title="Month", axis=alt.Axis(format="%b %Y")),
            y=alt.Y("revenue:Q", title="Revenue (USD)", axis=alt.Axis(format="$,.0f")),
            color=alt.Color("product:N", title="Product"),
            tooltip=[
                alt.Tooltip("month:T", title="Month", format="%B %Y"),
                alt.Tooltip("product:N", title="Product"),
                alt.Tooltip("revenue:Q", title="Revenue (USD)", format="$,.2f"),
            ],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, width="stretch")
    with st.expander("View monthly totals"):
        st.dataframe(
            monthly.rename(columns={"month": "Month", "product": "Product", "revenue": "Revenue (USD)"}),
            hide_index=True,
            width="stretch",
        )
