INSERT OVERWRITE TABLE IDENTIFIER(:target_catalog || ".finance.dim_company") 

with dim_cik as (select * from operations.finance_staging.raw_dim_cik) 

,dim_exchange as (select * from operations.finance_staging.raw_dim_exchange)

,dim_sp as (select * from operations.finance_staging.raw_dim_sp_500)

,sub as (select distinct cik
,countryba as headquarter_country
,stprba as headquarter_state 
,cityba as headquarter_city
from operations.finance_staging.raw_sub_tbl
)

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
 
 /*,dim_sp.gics_sector                                                              as sp_500_company_sector
  ,dim_sp.gics_sub_industry                                                        as sp_500_company_sub_industry
  ,dim_sp.headquarters_location                                                    as sp_500_company_headquarters_location*/
  ,dim_sp.date_added                                                               as sp_500_company_date_added_to_sp_500
  ,dim_sp.Founded                                                                  as sp_500_company_year_founded

  -- ,case
  --   -- Financials: sub-industry specific
  --   when dim_sp.gics_sub_industry = 'Diversified Banks'                           then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Regional Banks'                              then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Consumer Finance'                            then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Asset Management & Custody Banks'            then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Property & Casualty Insurance'               then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Life & Health Insurance'                     then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Multi-line Insurance'                        then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Reinsurance'                                 then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Investment Banking & Brokerage'              then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-SecuritiesBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Financial Exchanges & Data'                  then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-SecuritiesBasedOperations'
  --   when dim_sp.gics_sub_industry = 'Transaction & Payment Processing Services'   then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified'
  --   when dim_sp.gics_sub_industry = 'Insurance Brokers'                           then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified'
  --   -- Real Estate: sector level
  --   when dim_sp.gics_sector = 'Real Estate'                                       then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
  --   -- All other sectors default to Classified
  --   else                                                                                'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified'
  -- end                                                                              as preferred_fasb_linkrole

from 
dim_cik 
left join dim_exchange on dim_exchange.cik = dim_cik.cik and dim_exchange.ticker = dim_cik.ticker
left join dim_sp on dim_sp.ticker = dim_cik.ticker and dim_sp.CIK = dim_cik.cik
left join sub on sub.cik = dim_cik.cik 
