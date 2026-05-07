/*Where I last left off:
Discovered that interesting for one company (Fortinet) that they report in 2023 GROSS MARGIN as a terse label. This terse label does not show up in the dim taxonomy table. The standard label, is Gross Profit which does correspond to a child label in the Dim taxonomy table. When joining the dim taxonomy table, try joining on Standard Lable = Child and you will have to remove some characters from Child like us-gaap: to get the standard label match. 
*/

with base as (
select distinct 
dc.company_bigint_key
,dcc.company_name 
,dcc.company_stock_symbol
,fa.reported_period 
,fa.end_reported_period
,fa.value
,dt.terse_label
,fa.name_of_submitted_form as name_of_submitted_form
,fa.fiscal_period as fiscal_period
,fa.fiscal_year as fiscal_year
,fa.reported_quarters

from 
operations.finance_staging.fact_staging_financial_statement fa
LEFT JOIN 
     operations.finance.dim_taxonomy dt ON dt.terse_label = fa.terse_label AND dt.gaap_version = fa.gaap_version
    left join 
     operations.finance.dim_sector dc on 
    (
      dc.company_bigint_key = fa.company_bigint_key 
      and 
      dc.date_key = fa.reported_period
      and 
      dc.preferred_fasb_linkrole_income_statement = dt.linkrole
    )

left join operations.finance.dim_company dcc on dcc.company_bigint_key = fa.company_bigint_key

where financial_statement = 'IS'
and reported_period = end_reported_period
and value_segment is null
and name_of_submitted_form in ('10-Q','10-K')
and reported_quarters in (1,4)
and dc.preferred_fasb_linkrole_income_statement is not null
and fa.company_bigint_key = 436988458547446346

) 


,q4 as (
select distinct 

dc.company_bigint_key
,dcc.company_name 
,dcc.company_stock_symbol
,fa.reported_period 
,fa.end_reported_period
,fa.value
,dt.terse_label
,fa.name_of_submitted_form as name_of_submitted_form
,fa.fiscal_period as fiscal_period
,fa.fiscal_year as fiscal_year
,fa.reported_quarters
,case when fa.name_of_submitted_form = '10-K' and fa.fiscal_period = 'FY' then 1 else 0 end as q4_flag
from 
operations.finance_staging.fact_staging_financial_statement fa
LEFT JOIN 
     operations.finance.dim_taxonomy dt ON dt.terse_label = fa.terse_label AND dt.gaap_version = fa.gaap_version
    left join 
     operations.finance.dim_sector dc on 
    (
      dc.company_bigint_key = fa.company_bigint_key 
      and 
      dc.date_key = fa.reported_period
      and 
      dc.preferred_fasb_linkrole_income_statement = dt.linkrole
    )

left join operations.finance.dim_company dcc on dcc.company_bigint_key = fa.company_bigint_key

where financial_statement = 'IS'
and reported_period = end_reported_period
and value_segment is null
and name_of_submitted_form in ('10-Q','10-K')
and reported_quarters in (1,4)
and dc.preferred_fasb_linkrole_income_statement is not null
and fa.company_bigint_key = 436988458547446346
)





select * from base

