create or replace table operations.finance.dim_sector (
company_bigint_key bigint
,gics_sector string
) 
using delta
comment 'Dimension that explains by SIC codes what sectors companies roll up into';