
CREATE or replace TABLE finance.fact_balance_sheet (
  company_bigint_key BIGINT,
  date_key BIGINT,
  total_current_assets DOUBLE,
  total_non_current_assets DOUBLE,
  total_assets DOUBLE,
  total_current_liabilities DOUBLE,
  total_non_current_liabilities DOUBLE,
  total_liabilities DOUBLE,
  total_shareholder_equity DOUBLE,
  total_liabilities_and_shareholder_equity DOUBLE)
USING delta
COMMENT 'The table contains balance sheet data for publicly traded companies as reported to the SEC. It includes information on total current assets, total non-current assets, and total assets for specific reporting periods. This data can be used for financial analysis, assessing company liquidity, and understanding asset composition over time.'