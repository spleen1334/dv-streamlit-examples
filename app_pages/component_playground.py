"""Small, independent examples of common Streamlit components."""

import streamlit as st

from sales_data import load_sales


st.title("Component Playground")
st.write(
    "Try a few common components, then open the snippets to see how they work. "
    "Explore the full [Streamlit API reference](https://docs.streamlit.io/develop/api-reference)."
)
st.caption(
    "Widget keys on this page start with `playground_` so they stay separate "
    "from widgets on other pages."
)

sales = load_sales()

layout_tab, widgets_tab, data_tab, actions_tab = st.tabs(
    ["Text & layout", "Widgets", "Data", "Actions"]
)

with layout_tab:
    st.subheader("Put information side by side")
    st.write("Columns make it easy to compare a couple of numbers at a glance.")
    left, right = st.columns(2)
    left.metric("Sales records", len(sales))
    right.metric("Total revenue", f"${sales['revenue'].sum():,.2f}")
    with st.expander("Show layout source"):
        st.code(
            """left, right = st.columns(2)
left.metric("Sales records", len(sales))
right.metric("Total revenue", f"${sales['revenue'].sum():,.2f}")

layout_tab, widgets_tab, data_tab, actions_tab = st.tabs(
    ["Text & layout", "Widgets", "Data", "Actions"]
)
with layout_tab:
    st.write("Content for this tab")""",
            language="python",
        )

with widgets_tab:
    st.subheader("Make a preview interactive")
    st.write("Change the controls to update the message below.")
    region = st.selectbox(
        "Region", sorted(sales["region"].unique()), key="playground_region"
    )
    quantity = st.slider("Quantity", 1, 10, 3, key="playground_quantity")
    show_detail = st.toggle("Show detail", key="playground_show_detail")
    st.info(f"Preview: {quantity} units for {region}.")
    if show_detail:
        st.write(f"Detail: this preview is for the {region} region.")
    st.write("Returned values:")
    st.json({"region": region, "quantity": quantity, "show_detail": show_detail})
    with st.expander("Show widgets source"):
        st.code(
            """region = st.selectbox(
    "Region", sorted(sales["region"].unique()), key="playground_region"
)
quantity = st.slider("Quantity", 1, 10, 3, key="playground_quantity")
show_detail = st.toggle("Show detail", key="playground_show_detail")
st.info(f"Preview: {quantity} units for {region}.")
if show_detail:
    st.write(f"Detail: this preview is for the {region} region.")
st.json({"region": region, "quantity": quantity, "show_detail": show_detail})""",
            language="python",
        )

with data_tab:
    st.subheader("View and edit a small sample")
    st.write(
        "Edit quantities to update the total. Product and region are read-only; "
        "changes stay in this playground and never modify the source data."
    )
    sample = sales[["region", "product", "quantity"]].head(5).copy()
    edited = st.data_editor(
        sample,
        disabled=["region", "product"],
        column_config={
            "quantity": st.column_config.NumberColumn(
                "Quantity", min_value=0, step=1, required=True
            )
        },
        num_rows="fixed",
        hide_index=True,
        key="playground_editor",
    )
    st.metric("Edited quantity total", int(edited["quantity"].sum()))
    st.write("Original sample (read-only; select a column header to sort):")
    st.dataframe(sample, hide_index=True)
    with st.expander("Show data source"):
        st.code(
            """sample = sales[["region", "product", "quantity"]].head(5).copy()
edited = st.data_editor(
    sample,
    disabled=["region", "product"],
    column_config={
        "quantity": st.column_config.NumberColumn(
            "Quantity", min_value=0, step=1, required=True
        )
    },
    num_rows="fixed",
    hide_index=True,
    key="playground_editor",
)
st.metric("Edited quantity total", int(edited["quantity"].sum()))
st.dataframe(sample, hide_index=True)""",
            language="python",
        )

with actions_tab:
    st.subheader("Respond and download")
    st.write("The download contains the original five-row sample, not your edits.")
    if st.button("Say hello", key="playground_hello"):
        st.success("Hello! The button was clicked.")
    st.download_button(
        "Download original sample CSV",
        data=sample.to_csv(index=False),
        file_name="sales_sample_original.csv",
        mime="text/csv",
        key="playground_download",
    )
    with st.expander("Show actions source"):
        st.code(
            """if st.button("Say hello", key="playground_hello"):
    st.success("Hello! The button was clicked.")
st.download_button(
    "Download original sample CSV",
    data=sample.to_csv(index=False),
    file_name="sales_sample_original.csv",
    mime="text/csv",
    key="playground_download",
)""",
            language="python",
        )
