create or replace table operations.finance.dim_sector (
company_bigint_key bigint
,date_key integer
,gics_sector string
,gics_sub_industry string
) 
using delta
comment 'Dimension that explains by SIC codes what sectors companies roll up into. This also provides a GICS sub industry. The granularity is company, date_key';