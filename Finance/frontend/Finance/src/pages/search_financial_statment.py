import streamlit as st
from data.lakehouse import sql_query, get_tickers
from pages.search_balance_sheet import SearchBalanceSheet

catalog = 'operations'
schema = 'finance_staging'
table_name = 'fact_staging_financial_statement_tbl'

page = st.radio(
    "Navigation",
    ["Balance Sheet", "Income Statement", "Statement of Cash Flows"],
    horizontal=True,
    label_visibility="collapsed"
)

if page == "Balance Sheet":
    SearchBalanceSheet()
elif page == "Income Statement":
    st.write("Forecast content")
elif page == "Statement of Cash Flows":
    st.write("Settings content")
else:
    st.write("Settings Content")


