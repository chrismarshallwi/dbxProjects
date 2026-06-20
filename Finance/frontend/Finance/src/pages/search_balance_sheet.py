import streamlit as st
from data.lakehouse import sql_query, get_tickers

class SearchBalanceSheet:
    def __init__(self):
        
        catalog = 'operations'
        schema = 'finance'
        table_name = 'fact_balance_sheet'

        tickers = get_tickers()
        selected_tickers = st.multiselect("Select Tickers",options=tickers,default=None)

        if not selected_tickers:
            st.info("please select at least one ticker")
            st.stop()

        ticker_filter = ", ".join(f"'{t}'" for t in selected_tickers)

        #dont think that sql pivot will be suffice here
        #consider using python in future

        query = f"""
        /*SELECT *
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
        ORDER BY report_line_number;*/

WITH base AS (
    SELECT 
        fa.date_key_converted_period,
        fa.total_assets,
        fa.total_liabilities,
        fa.total_liabilities_and_equity
    FROM {catalog}.{schema}.{table_name} fa
    LEFT JOIN {operations}.{schema}.dim_company dc ON dc.company_bigint_key = fa.company_bigint_key
    WHERE dc.ticker_symbol in ({ticker_filter})
),
unpivoted AS (
    SELECT 
        date_key_converted_period,
        metric,
        value
    FROM base
    UNPIVOT (
        value FOR metric IN (
            total_assets,
            total_liabilities,
            total_liabilities_and_equity
        )
    )
)
SELECT *
FROM unpivoted
PIVOT (
    MAX(value)
    FOR date_key_converted_period IN (
        20240301 AS `2024_03`,
        20240601 AS `2024_06`,
        20240901 AS `2024_09`,
        20241201 AS `2024_12`,
        20250301 AS `2025_03`,
        20250601 AS `2025_06`,
        20250901 AS `2025_09`,
        20251201 AS `2025_12`
    )
)
ORDER BY metric;
        """


        df = sql_query(sql_query=query)
        st.data_editor(df, use_container_width=True, hide_index=True)