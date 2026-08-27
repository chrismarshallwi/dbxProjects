import streamlit as st
from data.lakehouse import sql_query, get_tickers

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

        min_value_on_dataset = spark.sql(f"""
        select 
        min(dd.date_value) as min_date
        from 
        {catalog}.{schema}.{table_name} fa 
        left join {catalog}.{schema}.{table_name_dd} dd on dd.date_key = fa.date_key 
        left join {catalog}.{schema}.{table_name_dc} dc on dc.company_bigint_key = fa.company_bigint_key
        where dc.company_stock_symbol in ({ticker_filter}) """).first()['min_date']

        max_value_on_dataset = spark.sql(f"""
        select 
        max(dd.date_value) as max_value
        from 
        {catalog}.{schema}.{table_name} fa 
        left join {catalog}.{schema}.{table_name_dd} dd on dd.date_key = fa.date_key 
        left join {catalog}.{schema}.{table_name_dc} dc on dc.company_bigint_key = fa.company_bigint_key
        where dc.company_stock_symbol in ({ticker_filter}) """).first()['max_date']

        date_range = st.date_input(
            'Select Date Range', 
            value=None, 
            min_value=min_value_on_dataset, 
            max_value=max_value_on_dataset
            )

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
        """

        df = sql_query(sql_query=query)
        st.line_chart(df, x= 'date_value', y= 'adj_close')
        #st.data_editor(df, use_container_width=True, hide_index=True)