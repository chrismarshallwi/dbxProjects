/*
RULES FOR INCOME STATEMENT 
where stmt = 'IS' and period = ddate and qtrs = 1 
*/

select 
distinct *
from 
operations.finance_staging.fact_staging_financial_statement_tbl 

where 
financial_statement = 'IS' 
and 
reported_period = end_reported_period
and
reported_quarters =1
