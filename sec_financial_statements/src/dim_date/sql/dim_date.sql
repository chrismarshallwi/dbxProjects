CREATE OR REPLACE TABLE operations.finance.dim_date AS
SELECT
    CAST(date_format(d, 'yyyyMMdd') AS INT) AS date_key,
    year(d) AS year,
    quarter(d) AS quarter
    ,concat('Q',quarter(d)  ) as quarter_name
FROM (
    SELECT explode(
        sequence(to_date('2000-01-01'), to_date('2100-12-31'), interval 1 day)
    ) AS d
);