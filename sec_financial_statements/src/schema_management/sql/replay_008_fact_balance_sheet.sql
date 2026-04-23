
CREATE or replace TABLE operations.finance.fact_balance_sheet (
  company_bigint_key BIGINT,
  date_key_reported_period BIGINT comment "Date key that is the reported period of financial reporting as sourced from EDGAR data.",
  date_key_converted_period bigint comment "Date key that has been fitted into a uniform 4-quarter year based on how the company reported fiscally. If a company reports Q4 for 2022 in the year 2023, this is fitted so that all companies uniformly appear as having the same quarters. This is important when comparing companies that might have different fiscal reporting periods.",
  capital_structure_business_key integer COMMENT "Signifies if financial companies, real estate companies as having different structured balance sheet versus regular companies with normal balance sheet",
  submitted_form_business_key integer comment "Signifies what form was submitted. Typically, 10-Q's are filed ever quarter and 10-K's are filed annually. Some (Most) companies file 3 10-Q's and 1 10-K per year.",
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

