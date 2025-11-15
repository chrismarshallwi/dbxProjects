with company_main as 
(
    with dim_cik as (select * from operations.finance_staging.raw_dim_cik) 
    ,dim_exchange as (select * from operations.finance_staging.raw_dim_exchange)
    ,dim_sp as (select * from operations.finance_staging.raw_dim_sp_500)

    select 
      sha2(concat_ws('|', dim_cik.cik, dim_cik.ticker), 256) AS company_key_hash
      ,bigint(substr(xxhash64(concat_ws('|', dim_cik.cik, dim_cik.ticker)), 1, 18)) AS company_bigint_key
      ,dim_cik.cik as company_identifier_key
      ,dim_cik.ticker as company_stock_symbol
      ,dim_cik.title as company_name
      ,dim_exchange.exchange as exchange_listed_on
      ,case when dim_sp.ticker is null then 0 else 1 end as sp_500_indicator
      ,dim_sp.gics_sector as company_sector
      ,dim_sp.gics_sub_industry as company_sub_industry
      ,dim_sp.headquarters_location as company_headquarters_location
      ,dim_sp.date_added as company_date_added_to_sp_500
      ,dim_sp.Founded as company_year_founded
    from 
    dim_cik 
    left join dim_exchange on dim_exchange.cik = dim_cik.cik and dim_exchange.ticker = dim_cik.ticker
    left join dim_sp on dim_sp.ticker = dim_cik.ticker and dim_sp.CIK = dim_cik.cik 
)

,sub as (
select 
adsh as filing_key
,sub.cik as company_identifier
,dc.company_stock_symbol as ticker_symbol
,dc.exchange_listed_on as exchange_traded_on
,case when dc.company_identifier_key is null then 0 else 1 end as sp_500_indicator
,sub.name as name_of_filing_company
,form as name_of_submitted_form
,period as reported_period 
,fy as fiscal_year
,fp as fiscal_period
,filed as filing_date
,dc.company_key_hash
,dc.company_bigint_key
from operations.finance_staging.raw_sub_tbl as sub
left join company_main dc on dc.company_identifier_key = sub.cik
) 

,tag as (
select 
tag
,tlabel
,version as gaap_version
,sha2(concat_ws('|', tlabel), 256) AS tag_key_hash
,bigint(substr(xxhash64(concat_ws('|', tlabel)), 1, 18)) AS tag_bigint_key
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
sub.company_key_hash
,sub.company_bigint_key
,tag.tag_key_hash
,tag.tag_bigint_key
,sub.name_of_filing_company
,sub.ticker_symbol
,sub.company_identifier
,sub.exchange_traded_on
--,sub.sp_500_indicator -- removed because it was definitely incorrect
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
*
from 
final

