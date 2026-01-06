import streamlit as st
from data.lakehouse import sql_query, get_tickers

catalog = 'operations'
schema = 'finance_staging'
table_name = 'fact_staging_financial_statement_tbl'

st.title("Search For Financial Statements")

tickers = get_tickers()
selected_tickers = st.multiselect("Select Tickers",options=tickers,default=None)

if not selected_tickers:
    st.info("please select at least one ticker")
    st.stop()

ticker_filter = ", ".join(f"'{t}'" for t in selected_tickers)

query = f"""
SELECT *
FROM (
    SELECT
        presented_label,
        report_line_number,
        reported_period,
        value
    FROM {catalog}.{schema}.{table_name}
    WHERE ticker_symbol in ({ticker_filter})
      AND financial_statement = 'BS'
      AND value_segment IS NULL
      AND reported_period = end_reported_period
)
PIVOT (
    MAX(value)
    FOR reported_period IN (
        '20241231' AS `2024_12_31`,
        '20250331' AS `2025-03-31`

    )
)
ORDER BY report_line_number;


"""


df = sql_query(sql_query=query)
st.data_editor(df, use_container_width=True, hide_index=True)

