import streamlit as st

from data.lakehouse import sql_query

catalog = 'operations'
schema = 'finance_staging'
table_name = 'fact_staging_financial_statement_tbl'

# query = f"""
# select distinct 
# presented_label
# ,report_line_number
# ,reported_period
# ,value
# from 
# {catalog}.{schema}.{table_name}
# where ticker_symbol = 'DE'
# and financial_statement = 'BS' and value_segment is null and reported_period = end_reported_period
# order by report_line_number
# """


query = f"""
SELECT *
FROM (
    SELECT
        presented_label,
        report_line_number,
        reported_period,
        value
    FROM {catalog}.{schema}.{table_name}
    WHERE ticker_symbol = 'DE'
      AND financial_statement = 'BS'
      AND value_segment IS NULL
      AND reported_period = end_reported_period
)
PIVOT (
    MAX(value)
    FOR reported_period IN (
        '20250430' AS `2025_04_30`,
        '20250131' AS `2025-01-31`
    )
)
ORDER BY report_line_number;


"""


df = sql_query(sql_query=query)
st.data_editor(df, width= "content")

