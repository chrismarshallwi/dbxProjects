import streamlit as st
from data.lakehouse import sql_query, get_tickers

class SearchBalanceSheet:
    def __init__(self):
        
        catalog = 'operations'
        schema = 'finance_staging'
        table_name = 'fact_staging_financial_statement_tbl'

        tickers = get_tickers()
        selected_tickers = st.multiselect("Select Tickers",options=tickers,default=None)

        if not selected_tickers:
            st.info("please select at least one ticker")
            st.stop()

        ticker_filter = ", ".join(f"'{t}'" for t in selected_tickers)

        #dont think that sql pivot will be suffice here
        #consider using python in future

        # query = f"""
        # SELECT *
        # FROM (
        #     SELECT
        #         presented_label,
        #         report_line_number,
        #         reported_period,
        #         value
        #     FROM {catalog}.{schema}.{table_name}
        #     WHERE ticker_symbol in ({ticker_filter})
        #     AND financial_statement = 'BS'
        #     AND value_segment IS NULL
        #     AND reported_period = end_reported_period
        # )
        # PIVOT (
        #     MAX(value)
        #     FOR reported_period IN (
        #         '20241231' AS `2024_12_31`,
        #         '20250331' AS `2025-03-31`

        #     )
        # )
        # ORDER BY report_line_number;
        # """

        reported_periods_query = f"""
        SELECT DISTINCT reported_period
FROM operations.finance_staging.fact_staging_financial_statement fa
LEFT JOIN operations.finance.dim_company dc 
    ON dc.company_bigint_key = fa.company_bigint_key 
WHERE dc.company_stock_symbol in ({tickers})
    AND financial_statement = 'BS'
    AND reported_period = end_reported_period
    AND value_segment IS NULL
    AND name_of_submitted_form = '10-Q'
ORDER BY reported_period
        """

        periods_df = sql_query(sql_query = reported_periods_query)

        periods = periods_df['reported_period'].tolist()

        pivot_list = ", ".join([f"'{p}'" for p in periods])

        query = f"""
        SELECT *
        FROM (
            select 
                terse_label,
                reported_period,
                value
            from operations.finance_staging.fact_staging_financial_statement fa
            left join operations.finance.dim_company dc 
                on dc.company_bigint_key = fa.company_bigint_key 
            WHERE dc.company_stock_symbol = ({ticker_filter})
                and financial_statement = 'BS'
                and reported_period = end_reported_period
                and value_segment is null
                and name_of_submitted_form = '10-Q'
        ) src
        PIVOT (
            MAX(value)
            FOR reported_period IN ({pivot_list})
        )
        ORDER BY terse_label
        """

        #spark.sql(query)

        df = sql_query(sql_query=query)
        st.data_editor(df, use_container_width=True, hide_index=True)