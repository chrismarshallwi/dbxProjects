create or replace view operations.finance.dim_submitted_form as 
select 
0 as submitted_form_business_key
,"10-Q" as submitted_form

union all 

select 
1 as submitted_form_business_key
,"10-K" as submitted_form


