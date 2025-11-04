/*
RULES FOR BALANCE SHEET 
where stmt = 'BS' and period = ddate
*/

select 
distinct *
from 
operations.finance_staging.fact_staging_financial_statement_tbl 

where 
financial_statement = 'BS' 
and 
reported_period = end_reported_period
