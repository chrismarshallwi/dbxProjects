

insert overwrite IDENTIFIER(:target_catalog || '.finance.fact_income_statement')

with base as (
select distinct 
dc.company_name
,fa.company_bigint_key
,fa.reported_period 
,fa.end_reported_period
,fa.value_segment
,fa.value
,fa.terse_label
,fa.standard_label
,fa.name_of_submitted_form
,fa.filing_date
,fa.fiscal_period
,fa.fiscal_year
,fa.reported_quarters
,ds.preferred_fasb_linkrole_income_statement 
,dense_rank() over (partition by dt.terse_label order by dt.terse_label_level_3) as duplicate_roll_up_ranking --denotes whether a terse label rolls up into 2 different categories. 
,coalesce(dt.linkrole, dt2.linkrole) as linkrole 
,coalesce(dt.terse_label_level_1 , dt2.terse_label_level_1  ) as terse_label_level_1 
,coalesce(dt.terse_label_level_2 , dt2.terse_label_level_2  ) as terse_label_level_2
,coalesce(dt.terse_label_level_3  , dt2.terse_label_level_3  ) as terse_label_level_3 
,coalesce(dt.terse_label_level_4  , dt2.terse_label_level_4  ) as terse_label_level_4 
,coalesce(dt.terse_label_level_5  , dt2.terse_label_level_5  ) as terse_label_level_5 
,coalesce(dt.terse_label_level_6  , dt2.terse_label_level_6  ) as terse_label_level_6 
,coalesce(dt.terse_label_level_7 , dt2.terse_label_level_7  ) as terse_label_level_7
,coalesce(dt.terse_label_level_8  , dt2.terse_label_level_8  ) as terse_label_level_8 
,coalesce(dt.terse_label_level_9 , dt2.terse_label_level_9  ) as terse_label_level_9 
,coalesce(dt.terse_label_level_10  , dt2.terse_label_level_10  ) as terse_label_level_10 
--,coalesce(dt.linkrole, dt2.linkrole) as linkrole
,coalesce(dt.terse_label_level_11 , dt2.terse_label_level_11  ) as terse_label_level_11 
,coalesce(dt.terse_label_level_12 , dt2.terse_label_level_12  ) as terse_label_level_12
,coalesce(dt.terse_label_level_13  , dt2.terse_label_level_13  ) as terse_label_level_13 
,coalesce(dt.terse_label_level_14  , dt2.terse_label_level_14  ) as terse_label_level_14 
,coalesce(dt.terse_label_level_15  , dt2.terse_label_level_15  ) as terse_label_level_15 
,coalesce(dt.terse_label_level_16  , dt2.terse_label_level_16  ) as terse_label_level_16 
,coalesce(dt.terse_label_level_17 , dt2.terse_label_level_17  ) as terse_label_level_17
,coalesce(dt.terse_label_level_18  , dt2.terse_label_level_18  ) as terse_label_level_18 
,coalesce(dt.terse_label_level_19 , dt2.terse_label_level_19  ) as terse_label_level_19 

from 
operations.finance_staging.fact_staging_financial_statement fa
left join 
operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
left join 
operations.finance.dim_sector ds on 
(
    ds.company_bigint_key = fa.company_bigint_key
    and 
    ds.date_key = fa.reported_period
)
left join 
operations.finance.dim_taxonomy dt on 
(
    fa.terse_label = dt.terse_label
    and  
    fa.gaap_version = dt.gaap_version 
    and 
    dt.linkrole = ds.preferred_fasb_linkrole_income_statement
)

left join 
(select * from operations.finance.dim_taxonomy where linkrole like '%disclosure%') dt2 on 
(
    fa.terse_label = dt2.terse_label 
    and 
    fa.gaap_version = dt2.gaap_version 
)

where financial_statement = 'IS'
and reported_period = end_reported_period
and value_segment is null
and name_of_submitted_form in ('10-Q','10-K')
and reported_quarters in (1,4)
order by reported_period

) 

/*Input Logic below that condenses terse label conditions corresponding to highest level leaf node to compose the ins_component (income statement component) field*/
,staging as (
select distinct 
* 
,case when terse_label = 'Revenue from Contract with Customer, Excluding Assessed Tax' and terse_label_level_6 = 'Revenue from Contract with Customer, Excluding Assessed Tax' then 'Revenue'
when terse_label = 'Revenues' and terse_label_level_12 = 'Revenues' then 'Revenue'
else null 
end as ins_component
from base 
where company_bigint_key is not null
and duplicate_roll_up_ranking = 1
)


,final as (
select 
staging.company_bigint_key
,fiscal_year
,fiscal_period
,filing_date as date_key_filing
,reported_period as date_key_reported_period

,case when name_of_submitted_form = '10-Q' then 0 when name_of_submitted_form = '10-K' then 1 else null end as submitted_form_business_key 


,case when (ROW_NUMBER() over (partition by dc.company_name, dc.company_identifier_key, reported_period, reported_quarters, fiscal_period, fiscal_year 
                               order by dc.company_stock_symbol)) = 1 then 0 else 1 end as duplicate_stock_symbol_identifier

,reported_quarters

,MAX(CASE WHEN ins_component = 'Revenue' THEN value END) AS total_revenue

from 
staging 
left join operations.finance.dim_company dc on dc.company_bigint_key = staging.company_bigint_key
where 
ins_component is not null       
group by 
staging.company_bigint_key,
dc.company_name
,dc.company_identifier_key
,dc.company_stock_symbol
,reported_period 
,fiscal_year
,fiscal_period
,filing_date
,(case when name_of_submitted_form = '10-Q' then 0 when name_of_submitted_form = '10-K' then 1 else null end)
,reported_quarters
order by reported_period asc
)

,final_with_year_logic as (
select 
*
-- Previous 3 fiscal years
,lag(fiscal_year,1) over (partition by company_bigint_key order by date_key_reported_period) as prev_fiscal_year_1

,lag(fiscal_year,2) over (partition by company_bigint_key order by date_key_reported_period) as prev_fiscal_year_2

,lag(fiscal_year,3) over (partition by company_bigint_key order by date_key_reported_period) as prev_fiscal_year_3

from final 
)


,quarter_four_logic as (
select 
company_bigint_key
,fiscal_year
,fiscal_period
,date_key_filing
,date_key_reported_period 
,concat(case when fiscal_period = 'FY'
and fiscal_year < prev_fiscal_year_1
and fiscal_year < prev_fiscal_year_2
and fiscal_year < prev_fiscal_year_3
then fiscal_year + 1
else fiscal_year
end,'-',fiscal_period) as date_key_converted_period
,submitted_form_business_key
,duplicate_stock_symbol_identifier
,reported_quarters
,total_revenue

,case when (count(fiscal_period) over (partition by company_bigint_key, fiscal_year)) = 5 and (row_number() over (partition by company_bigint_key, fiscal_year order by date_key_reported_period)) = 4 then 1 else 0 end as quarter_four_report_flag
from 
final_with_year_logic 

) 


select 
company_bigint_key
,fiscal_year
,fiscal_period
,date_key_filing
,date_key_reported_period 
,date_key_converted_period
,submitted_form_business_key
,duplicate_stock_symbol_identifier
,reported_quarters
,total_revenue
from quarter_four_logic
where 
quarter_four_report_flag != 1
