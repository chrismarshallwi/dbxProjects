with sub as (
select 
adsh as filing_key
,sub.cik as company_identifier
,cik.ticker as ticker_symbol
,exchange.exchange as exchange_traded_on
,case when sp.CIK is null then 0 else 1 end as sp_500_indicator
,sub.name as name_of_filing_company
,form as name_of_submitted_form
,period as reported_period 
,fy as fiscal_year
,fp as fiscal_period
,filed as filing_date
from operations.finance_staging.raw_sub_tbl as sub
left join (select * from operations.finance_staging.raw_dim_cik) as cik on cik.cik = sub.cik
left join (select * from operations.finance_staging.raw_dim_exchange) as exchange on exchange.cik = sub.cik
left join (select * from operations.finance_staging.raw_dim_sp_500) as sp on sp.CIK = sub.cik

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
,sub.exchange_traded_on
,sub.sp_500_indicator
,sub.filing_key
,sub.name_of_submitted_form
,sub.filing_date
,pre.gaap_version
,try_cast(sub.reported_period as bigint) as reported_period
,sub.fiscal_year
,sub.fiscal_period
,pre.financial_statement
,pre.report_number
,pre.report_line_number
,cast(num.end_reported_period as bigint) as end_reported_period
,cast(num.reported_quarters as bigint) as reported_quarters
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
count(*)
from 
final where sp_500_indicator = 1

