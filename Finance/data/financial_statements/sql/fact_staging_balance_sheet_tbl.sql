/*
RULES FOR BALANCE SHEET 
where stmt = 'BS' and period = ddate
*/
with cte as ( 
select 
distinct 
bs.company_bigint_key
,bs.tag_total_bigint_key
,bs.tag_sub_total_bigint_key
,bs.reported_period as date_key
,dc.company_name
,dc.company_stock_symbol
,bs.presented_label
,bs.terse_label  as terse_label
/*,dt.tag_level_3 as terse_label_tag_level_3*/
,dtx.tag_level_3 as presented_label_tag_level_3
/*,coalesce(dt.tag_level_3,dtx.tag_level_3) as tag_level_3_combined*/
,dtx.tag_level_3 as tag_level_3_combined

,case when bs.presented_label like '%Total%' then 1 
    when bs.presented_label like '%TOTAL' then 1 
    when bs.presented_label like '%total%' then 1 
    else 0 end as total_indicator /*Dont love this solution, but it seems to work for now*/

,bs.report_number
,bs.report_line_number
,bs.value
from 
operations.finance_staging.fact_staging_financial_statement_tbl bs
left join operations.finance.dim_company dc on dc.company_bigint_key = bs.company_bigint_key
/*left join operations.finance.dim_tag dt on dt.tag_bigint_key = bs.tag_sub_total_bigint_key*/
left join operations.finance.dim_tag dtx on dtx.tag_bigint_key = bs.tag_total_bigint_key
where 
financial_statement = 'BS'  and value_segment is null
and 
reported_period = end_reported_period 
and 
dc.sp_500_indicator = 1)


,pivot_cte AS (
    SELECT *
    FROM cte
    PIVOT (
        SUM(value) AS total
        FOR tag_level_3_combined IN (
            'Total Assets' as total_assets,
            'Total Liabilities' as total_liabilities,
            'Total Equity' as total_equity,
            'Total Liabilities & Equity' as total_liabilities_and_equity,
            'Total Current Assets' as total_current_assets,
            case when 'Total Noncurrent Assets' is null then '1' else 'Total Noncurrent Assets' end as total_noncurrent_assets
        )
    )
)
select distinct * from pivot_cte where company_stock_symbol = 'ADP' 









