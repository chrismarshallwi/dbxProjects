CREATE or replace TABLE finance_staging.raw_num_tbl (
  adsh STRING,
  tag STRING,
  version STRING,
  ddate INT,
  qtrs INT,
  uom STRING,
  segments STRING,
  coreg STRING,
  value DOUBLE,
  footnote STRING,
  source_file STRING,
  source_file_description STRING)
USING delta
