insert overwrite IDENTIFIER(:target_catalog || '.finance.fact_balance_sheet')

/*
RULES FOR BALANCE SHEET 
where stmt = 'BS' and period = ddate
*/

with cte as ( 
select distinct 
    balance_sheet.report_label
    ,balance_sheet.report_label_bigint_key
    ,balance_sheet.company_bigint_key
    ,balance_sheet.date_key
    ,fact.reported_period
    ,fact.value
from 
    operations.finance_staging.dim_balance_sheet balance_sheet 
left join 

    (select 
    * 
    from 
    operations.finance_staging.fact_staging_financial_statement
    where 
    financial_statement = 'BS'  and value_segment is null
    and 
    reported_period = end_reported_period 
    ) fact on 
            (fact.company_bigint_key = balance_sheet.company_bigint_key 
            and 
            fact.presented_label_bigint_key = balance_sheet.presented_label_bigint_key
            and 
            fact.reported_period = balance_sheet.date_key)
)

,pivot_cte AS (
    SELECT *
    FROM cte
    PIVOT (
        SUM(value) AS total
        FOR report_label IN (
            'total_current_asset' as total_current_assets
            ,'total_non_current_assets' as total_non_current_assets
            ,'total_assets' as total_assets
            ,'total_current_liabilities' as total_current_liabilities
            ,'total_non_current_liabilities' as total_non_current_liabilities
            ,'total_liabilities' as total_liabilities
            ,'total_shareholder_equity' as total_shareholder_equity
            
        )
    )
)

SELECT
    pivot_cte.company_bigint_key

    ,reported_period as date_key

    ,MAX(total_current_assets) AS total_current_assets

    ,(case when MAX(total_non_current_assets) is null then MAX(total_assets) - MAX(total_current_assets) 
    else MAX(total_non_current_assets) end) as total_non_current_assets

    ,MAX(total_assets) AS total_assets

    ,max(total_current_liabilities) as total_current_liabilities 

    ,(case when MAX(total_non_current_liabilities) is null then MAX(total_liabilities) - MAX(total_current_liabilities) 
    else MAX(total_non_current_liabilities) end) as total_non_current_liabilities

    ,max(total_liabilities) as total_liabilities
    ,max(total_shareholder_equity) as total_shareholder_equity

FROM 
    pivot_cte
left join 
    operations.finance.dim_company dc on dc.company_bigint_key = pivot_cte.company_bigint_key
where 
    reported_period is not null
GROUP BY
    pivot_cte.company_bigint_key,
    reported_period,
    dc.company_stock_symbol
ORDER BY
    pivot_cte.company_bigint_key,
    reported_period