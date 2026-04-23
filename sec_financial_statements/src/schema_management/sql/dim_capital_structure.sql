create or replace view operations.finance.dim_capital_structure as 
select 
0 as capital_structure_business_key
,"Regular" as capital_structure

union all 

select 
1 as capital_structure_business_key
,"Financial & Real Estate" as capital_structure


