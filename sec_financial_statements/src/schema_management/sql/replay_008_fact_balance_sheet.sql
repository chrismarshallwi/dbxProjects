
CREATE or replace TABLE finance.fact_balance_sheet (
  company_bigint_key BIGINT,
  date_key BIGINT,
  capital_structure_business_key integer COMMENT "Signifies if financial companies, real estate companies as having different structured balance sheet versus regular companies with normal balance sheet",
  total_assets DOUBLE,
  total_liabilities DOUBLE,
  total_equity DOUBLE,
  total_liabilities_and_equity DOUBLE,
  total_current_assets double,
  total_non_current_assets double,
  total_current_liabilities double,
  total_non_current_liabilities double)
USING delta
COMMENT 'The table contains balance sheet data for publicly traded companies as reported to the SEC. It includes information on total assets for specific reporting periods. This data can be used for financial analysis, assessing company liquidity, and understanding asset composition over time.';

