import streamlit as st


st.set_page_config(page_title="Streamlit Sales Lab", page_icon="📊", layout="wide")

pages = [
    st.Page("app_pages/chart_basics.py", title="Chart Basics", icon="📈"),
]

st.navigation(pages).run()
