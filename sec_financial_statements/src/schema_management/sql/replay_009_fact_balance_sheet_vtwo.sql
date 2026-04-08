CREATE or replace TABLE operations.finance.fact_balance_sheet_vtwo (
  company_bigint_key BIGINT,
  date_key BIGINT,
  total_assets DOUBLE,
  total_liabilities DOUBLE,
  total_equity DOUBLE,
  total_liabilities_and_equity DOUBLE)
USING delta
COMMENT 'The table contains balance sheet data for publicly traded companies as reported to the SEC. It includes information on total assets for specific reporting periods. This data can be used for financial analysis, assessing company liquidity, and understanding asset composition over time.'