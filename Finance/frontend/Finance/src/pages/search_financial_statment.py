import streamlit as st

from data.lakehouse import load_table

catalog = 'operations'
schema = 'finance_staging'
table = 'fact_staging_financial_statement_tbl'

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


sql_query(query=query)

