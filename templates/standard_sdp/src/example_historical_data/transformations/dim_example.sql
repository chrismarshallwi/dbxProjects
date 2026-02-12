-- TIPS:
-- Create one materialized view per .sql file and name it after the file name (e.g. dim_example.sql -> dim_example)
-- The default target catalog and schema are defined in the *.pipeline.yml file
-- Use ${staging_schema} variable to read or write from/to the staging schema
-- Use ${ops_catalog} variable to read from the operations catalog if needed
-- Use ${edw_catalog} variable to read from the EDW catalog if needed

CREATE MATERIALIZED VIEW dim_example
SELECT DISTINCT
  invoice_number,
  po_number AS purchase_order_number,
  voucher
FROM
  ${staging_schema}.dim_example_source
WHERE
  voucher IS NOT NULL