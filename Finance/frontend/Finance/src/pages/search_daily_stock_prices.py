import streamlit as st
from data.lakehouse import sql_query, get_tickers

class SearchDailyStockPrice:
    def __init__(self):
        
        catalog = 'operations'
        schema = 'finance'
        table_name = 'fact_price_daily'
        table_name_dc = 'dim_company'

        tickers = get_tickers()
        selected_tickers = st.multiselect("Select Tickers",options=tickers,default=None)

        if not selected_tickers:
            st.info("please select at least one ticker")
            st.stop()

        ticker_filter = ", ".join(f"'{t}'" for t in selected_tickers)

        #dont think that sql pivot will be suffice here
        #consider using python in future

        query = f"""
        select 
        date_key,
        adj_close
        from 
        {catalog}.{schema}.{table_name} fa
        left join 
        {catalog}.{schema}.{table_name_dc} dc on dc.company_bigint_key = fa.company_bigint_key
        where dc.company_stock_symbol in ({ticker_filter})
        """


        df = sql_query(sql_query=query)
        st.data_editor(df, use_container_width=True, hide_index=True)