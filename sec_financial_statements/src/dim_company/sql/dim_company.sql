INSERT OVERWRITE TABLE IDENTIFIER(:target_catalog || ".finance.dim_company") 

with dim_cik as (select * from operations.finance_staging.raw_dim_cik) 

,dim_exchange as (select * from operations.finance_staging.raw_dim_exchange)

,dim_sp as (select * from operations.finance_staging.raw_dim_sp_500)

/*Added 08/26/2026 to account for Index reporting in operations.finance.fact_price_daily table*/

,indices as (select 
null as company_key_hash
,1 as company_bigint_key 
,null as company_identifier_key
,'^GSPC' as company_stock_symbol
,'S&P 500' as company_name
,null as exchange_listed_on
,null as sp_500_indicator
,null as headquarter_country
,null as headquarter_state
,null as headquarter_city
,null as sp_500_company_date_added_to_sp_500
,null as sp_500_company_year_founded

union 
select 
null as company_key_hash
,2 as company_bigint_key 
,null as company_identifier_key
,'^IXIC' as company_stock_symbol
,'NASDAQ' as company_name
,null as exchange_listed_on
,null as sp_500_indicator
,null as headquarter_country
,null as headquarter_state
,null as headquarter_city
,null as sp_500_company_date_added_to_sp_500
,null as sp_500_company_year_founded

union 
select 
null as company_key_hash
,3 as company_bigint_key 
,null as company_identifier_key
,'^DJI' as company_stock_symbol
,'DOW JONES' as company_name
,null as exchange_listed_on
,null as sp_500_indicator
,null as headquarter_country
,null as headquarter_state
,null as headquarter_city
,null as sp_500_company_date_added_to_sp_500
,null as sp_500_company_year_founded

)

,sub as (select distinct cik
,countryba as headquarter_country
,stprba as headquarter_state 
,cityba as headquarter_city
from operations.finance_staging.raw_sub_tbl
)

,base as (
select 
  sha2(concat_ws('|', dim_cik.cik, dim_cik.ticker), 256)                         AS company_key_hash
  ,bigint(substr(xxhash64(concat_ws('|', dim_cik.cik, dim_cik.ticker)), 1, 18))   AS company_bigint_key
  ,dim_cik.cik                                                                     as company_identifier_key
  ,dim_cik.ticker                                                                  as company_stock_symbol
  ,dim_cik.title                                                                   as company_name
  ,dim_exchange.exchange                                                           as exchange_listed_on
  ,case when dim_sp.ticker is null then 0 else 1 end                              as sp_500_indicator
  ,sub.headquarter_country                                                          as headquarter_country
  ,sub.headquarter_state                                                            as headquarter_state
  ,sub.headquarter_city                                                             as headquarter_city
  ,dim_sp.date_added                                                               as sp_500_company_date_added_to_sp_500
  ,dim_sp.Founded                                                                  as sp_500_company_year_founded

from 
dim_cik 

left join dim_exchange on dim_exchange.cik = dim_cik.cik and dim_exchange.ticker = dim_cik.ticker
left join dim_sp on dim_sp.ticker = dim_cik.ticker and dim_sp.CIK = dim_cik.cik
left join sub on sub.cik = dim_cik.cik 
)

select * from base 
union 
select * from indices
