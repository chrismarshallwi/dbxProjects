CREATE or replace TABLE finance_staging.raw_tag_tbl (
  tag STRING,
  version STRING,
  custom INT,
  abstract INT,
  datatype STRING,
  iord STRING,
  crdr STRING,
  tlabel STRING,
  doc STRING,
  source_file STRING,
  source_file_description STRING)
USING delta