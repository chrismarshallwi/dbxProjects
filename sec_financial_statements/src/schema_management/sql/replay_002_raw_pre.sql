CREATE or replace TABLE finance_staging.raw_pre_tbl (
  adsh STRING,
  report INT,
  line INT,
  stmt STRING,
  inpth INT,
  rfile STRING,
  tag STRING,
  version STRING,
  plabel STRING,
  negating INT,
  source_file STRING,
  source_file_description STRING)
USING delta