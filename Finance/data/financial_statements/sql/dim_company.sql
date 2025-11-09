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
