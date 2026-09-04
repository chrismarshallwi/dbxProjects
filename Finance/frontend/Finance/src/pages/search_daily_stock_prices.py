import streamlit as st
import pandas as pd 
import plotly.express as px
from data.lakehouse import sql_query, get_tickers
from pages.strategy_mean_reversion import MeanReversion

class SearchDailyStockPrice:
    def __init__(self):
        
        catalog = 'operations'
        schema = 'finance'
        table_name = 'fact_price_daily'
        table_name_dc = 'dim_company'
        table_name_dd = 'dim_date'

        tickers = get_tickers()
        selected_tickers = st.multiselect("Select Tickers",options=tickers,default=None)

        if not selected_tickers:
            st.info("please select at least one ticker")
            st.stop()

        ticker_filter = ", ".join(f"'{t}'" for t in selected_tickers)

        min_value_on_dataset = sql_query(f"""
        select 
        min(dd.date_value) as min_date
        from 
        {catalog}.{schema}.{table_name} fa 
        left join {catalog}.{schema}.{table_name_dd} dd on dd.date_key = fa.date_key 
        left join {catalog}.{schema}.{table_name_dc} dc on dc.company_bigint_key = fa.company_bigint_key
        where dc.company_stock_symbol in ({ticker_filter}) """).iloc[0]['min_date']

        max_value_on_dataset = sql_query(f"""
        select 
        max(dd.date_value) as max_date
        from 
        {catalog}.{schema}.{table_name} fa 
        left join {catalog}.{schema}.{table_name_dd} dd on dd.date_key = fa.date_key 
        left join {catalog}.{schema}.{table_name_dc} dc on dc.company_bigint_key = fa.company_bigint_key
        where dc.company_stock_symbol in ({ticker_filter}) """).iloc[0]['max_date']

        date_range = st.date_input(
            "Select Date Range",
            value=(min_value_on_dataset, max_value_on_dataset),
            min_value=min_value_on_dataset,
            max_value=max_value_on_dataset
        )

        strategy = st.selectbox(
            "Select Strategy",
            ["Mean Reversion","Dollar Cost Average"],
            index = None, 
            placeholder = 'Select a strategy...'
        )

        if len(date_range) == 2:

            start_date = date_range[0]
            end_date = date_range[1]

            if strategy == "Mean Reversion":

                MeanReversion()
            
            elif strategy == "Dollar Cost Average":
                pass
            
            else:
                query = f"""
                select 
                dd.date_value,
                fa.adj_close
                from 
                {catalog}.{schema}.{table_name} fa
                left join 
                {catalog}.{schema}.{table_name_dc} dc on dc.company_bigint_key = fa.company_bigint_key
                left join 
                {catalog}.{schema}.{table_name_dd} dd on dd.date_key = fa.date_key
                where dc.company_stock_symbol in ({ticker_filter})
                and 
                dd.date_value >= '{start_date}' and dd.date_value <= '{end_date}'
                """
            

