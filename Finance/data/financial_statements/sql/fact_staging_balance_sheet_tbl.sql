/*
RULES FOR BALANCE SHEET 
where stmt = 'BS' and period = ddate
*/
with cte as ( 
select 
distinct 
    bs.reported_period as date_key
    ,dc.company_name
    ,dc.company_stock_symbol

    ,bs.presented_label as presented_label
    /*,bs.terse_label  as terse_label

    ,dpl.report_sub_class*/
    ,dbs.report_sub_class
    ,dbs.report_label

    /*,bs.report_number
    ,bs.report_line_number*/
    ,bs.value
from 
    operations.finance_staging.fact_staging_financial_statement_tbl bs
left join 
    operations.finance.dim_company dc on dc.company_bigint_key = bs.company_bigint_key
left join 
    operations.finance_staging.dim_presented_labels dpl on dpl.presented_label_bigint_key = bs.presented_label_bigint_key
left join 
    operations.finance_staging.dim_balance_sheet dbs on dbs.report_sub_class_bigint_key = dpl.report_sub_class_bigint_key
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
        FOR report_label IN (
            'total_current_asset' as total_current_assets
            ,'total_non_current_assets' as total_non_current_assets
            ,'total_assets' as total_assets
        )
    )
)
select distinct * from pivot_cte 

/*
select distinct presented_label, count(*) from cte where presented_label like '%Total%' group by presented_label 
*/







