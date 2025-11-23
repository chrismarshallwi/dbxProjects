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
    operations.finance_staging.dim_balance_sheet_temp balance_sheet 
left join 

    (select 
    * 
    from 
    operations.finance_staging.fact_staging_financial_statement_tbl 
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

select * from cte

/*
,pivot_cte AS (
    SELECT *
    FROM cte
    PIVOT (
        SUM(value) AS total
        FOR report_label IN (
            'total_current_asset' as total_current_assets
            ,'total_non_current_assets' as total_non_current_assets
            ,'total_assets' as total_assets
        )
    )
)
select distinct 
company_bigint_key
,reported_period
,total_current_assets
,total_non_current_assets
,total_assets 
from pivot_cte  */

