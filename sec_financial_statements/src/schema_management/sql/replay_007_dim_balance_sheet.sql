CREATE or replace TABLE finance_staging.dim_balance_sheet (
  report_label_bigint_key BIGINT,
  presented_label_bigint_key BIGINT,
  company_bigint_key BIGINT,
  report_label STRING,
  date_key BIGINT,
  presented_label STRING,
  company_stock_symbol STRING)
USING delta