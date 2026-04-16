select distinct 

fa.*

from 
operations.finance_staging.fact_staging_financial_statement fa
left join 
operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key 
where 
financial_statement = 'IS'
and dc.sp_500_indicator = 1
and reported_quarters =1
and reported_period = end_reported_period
and value_segment is null
and name_of_submitted_form = '10-Q'

