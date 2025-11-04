with sub as (
select 
adsh as filing_key
,sub.cik as company_identifier
,cik.ticker as ticker_symbol
,name as name_of_filing_company
,form as name_of_submitted_form
,period as reported_period 
,fy as fiscal_year
,fp as fiscal_period
,filed as filing_date
from operations.finance_staging.raw_sub_tbl as sub
left join (select * from operations.finance_staging.raw_dim_cik) as cik on cik.cik = sub.cik
inner join (select distinct symbol from operations.finance.fact_price_daily) as price_symbols on price_symbols.symbol = cik.ticker
) 

,tag as (
select 
tag
,tlabel
,version as gaap_version
from 
operations.finance_staging.raw_tag_tbl
)

,pre as (
select 
adsh as filing_key 
,stmt as financial_statement
,tag 
,plabel
,version as gaap_version
,report as report_number
,line as report_line_number
from 
operations.finance_staging.raw_pre_tbl
)

,num as (
select  
adsh as filing_key
,tag 
,version as gaap_version
,ddate as end_reported_period
,value as value
,qtrs as reported_quarters
,segments as value_segment
from 
operations.finance_staging.raw_num_tbl
) 
,
final as (
select distinct 
sub.name_of_filing_company
,sub.ticker_symbol
,sub.filing_key
,sub.name_of_submitted_form
,sub.filing_date
,pre.gaap_version
,sub.reported_period 
,sub.fiscal_year
,sub.fiscal_period
,pre.financial_statement
,pre.report_number
,pre.report_line_number
,num.end_reported_period
,num.reported_quarters
,num.tag as standard_label
,pre.plabel as presented_label
,tag.tlabel as terse_label
,num.value_segment
,num.value

from 
sub
left join pre on pre.filing_key = sub.filing_key
left join num on num.filing_key = sub.filing_key and num.tag = pre.tag and num.gaap_version = pre.gaap_version 
left join tag on tag.tag = num.tag and tag.gaap_version  = pre.gaap_version 
) 

select distinct 
*
from 
final 

