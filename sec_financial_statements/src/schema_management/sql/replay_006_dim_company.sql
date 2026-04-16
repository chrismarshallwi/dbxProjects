CREATE or replace TABLE finance.dim_company (
  company_key_hash STRING,
  company_bigint_key BIGINT,
  company_identifier_key BIGINT,
  company_stock_symbol STRING,
  company_name STRING,
  exchange_listed_on STRING,
  sp_500_indicator INT,
  sp_500_company_sector STRING,
  sp_500_company_sub_industry STRING,
  sp_500_company_headquarters_location STRING,
  sp_500_company_date_added_to_sp_500 STRING,
  sp_500_company_year_founded STRING)
USING delta
comment "Dimensional table for attributes pertaining to publicly traded companies"
