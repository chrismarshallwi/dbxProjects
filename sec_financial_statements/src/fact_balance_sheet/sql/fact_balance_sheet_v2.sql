WITH cte AS (
    SELECT DISTINCT
         dc.company_bigint_key
        ,reported_period as date_key
        ,value
        ,dt.terse_label

        ,CASE
            WHEN fa.terse_label = 'Assets'
                 AND dt.terse_label_level_3 = 'Assets [Abstract]'
                 AND dt.terse_label_level_4 = 'Assets'
                 AND fa.value_segment IS NULL
            THEN 'Total Assets'

            WHEN fa.terse_label = 'Liabilities'
                 AND dt.terse_label_level_4 = 'Liabilities [Abstract]'
                 AND dt.terse_label_level_5 = 'Liabilities'
                 AND fa.value_segment IS NULL
            THEN 'Total Liabilities'

            WHEN fa.terse_label = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                 AND dt.terse_label_level_4 = 'Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]'
                 AND dt.terse_label_level_5 = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            WHEN fa.terse_label = 'Equity, Attributable to Parent'
                 AND dt.terse_label_level_4 = 'Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]'
                 AND dt.terse_label_level_5 = 'Equity, Attributable to Parent'
                 AND fa.value_segment IS NULL
                 AND NOT EXISTS (
                     SELECT 1
                     FROM operations.finance_staging.fact_staging_financial_statement fa2
                     JOIN operations.finance.dim_taxonomy dt2
                         ON dt2.terse_label = fa2.terse_label
                         AND dt2.gaap_version = fa2.gaap_version
                         AND dt2.linkrole = dt.linkrole
                     WHERE fa2.filing_key = fa.filing_key
                       AND fa2.terse_label = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                       AND fa2.value_segment IS NULL
                 )
            THEN 'Total Equity'

            WHEN fa.terse_label = 'Partners Capital, Including Portion Attributable to Noncontrolling Interest'
                 AND dt.linkrole = 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            WHEN fa.terse_label = 'Limited Partners'' Capital Account'
                 AND dt.linkrole = 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            WHEN fa.terse_label = 'Liabilities and Equity'
                 AND dt.terse_label_level_4 = 'Liabilities and Equity'
                 AND fa.value_segment IS NULL
            THEN 'Total Liabilities and Equity'

            ELSE NULL
        END AS bs_component

    FROM operations.finance_staging.fact_staging_financial_statement fa
    LEFT JOIN operations.finance.dim_taxonomy dt
        ON dt.terse_label = fa.terse_label
        AND dt.gaap_version = fa.gaap_version
    LEFT JOIN operations.finance.dim_company dc
        ON dc.company_bigint_key = fa.company_bigint_key
        AND dc.preferred_fasb_linkrole = dt.linkrole
    WHERE 
        --  sp_500_indicator = 1
      --AND 
      reported_period = end_reported_period
      AND name_of_submitted_form = '10-Q'
      AND financial_statement = 'BS'
      AND value_segment IS NULL
)

SELECT
    company_bigint_key,
    date_key,

    MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) AS total_assets,
    MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) AS total_liabilities,
    MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) AS total_equity,
    MAX(CASE WHEN bs_component = 'Total Liabilities and Equity' THEN value END) AS total_liabilities_and_equity

FROM cte
WHERE bs_component IS NOT NULL
GROUP BY
    company_bigint_key,
    date_key
ORDER BY
    company_bigint_key,
    date_key