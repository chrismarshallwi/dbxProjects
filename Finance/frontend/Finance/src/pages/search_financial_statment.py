import streamlit as st

from data.lakehouse import sql_query

catalog = 'operations'
schema = 'finance_staging'
table_name = 'fact_staging_financial_statement_tbl'

query = f"""
select distinct 
presented_label
,report_line_number
,reported_period
,value
from 
{catalog}.{schema}.{table_name}
where ticker_symbol = 'DE'
and financial_statement = 'BS'
order by report_line_number
"""


df = sql_query(sql_query=query)
st.data_editor(df)

