SELECT DISTINCT
     name_of_filing_company
    ,name_of_submitted_form
    ,filing_date
    ,fa.gaap_version
    ,reported_period
    ,financial_statement
    ,report_number
    ,report_line_number
    ,end_reported_period
    ,fa.terse_label
    ,fa.presented_label
    ,value_segment
    ,value
    ,filing_key
    ,dt.*

    /*
    ============================================================
    BS COMPONENT — Linkrole-specific hierarchy logic
    ============================================================
    All 5 linkroles share the same top-level signals for Assets
    and Liabilities and Equity, but differ on how Equity and
    Liabilities sit beneath that. Equity dedup rule: prefer the
    NCI-inclusive total; fall back to parent-only if NCI doesn't
    exist for the same filing.
    ============================================================
    */

    ,CASE

        /* -------------------------------------------------------
           TOTAL ASSETS
           Consistent across all 5 linkroles:
           terse_label self-references at level_4
           under Assets [Abstract] at level_3
        ------------------------------------------------------- */
        WHEN fa.terse_label = 'Assets'
             AND dt.terse_label_level_3 = 'Assets [Abstract]'
             AND dt.terse_label_level_4 = 'Assets'
             AND fa.value_segment IS NULL
        THEN 'Total Assets'

        /* -------------------------------------------------------
           TOTAL LIABILITIES
           All linkroles: terse_label self-references at level_5
           under Liabilities [Abstract] at level_4
        ------------------------------------------------------- */
        WHEN fa.terse_label = 'Liabilities'
             AND dt.terse_label_level_4 = 'Liabilities [Abstract]'
             AND dt.terse_label_level_5 = 'Liabilities'
             AND fa.value_segment IS NULL
        THEN 'Total Liabilities'

        /* -------------------------------------------------------
           TOTAL EQUITY — NCI-inclusive (preferred)
           All linkroles: self-references at level_5
           under Equity, Including Portion... [Abstract] at level_4
        ------------------------------------------------------- */
        WHEN fa.terse_label = 'Equity, Including Portion Attributable to Noncontrolling Interest'
             AND dt.terse_label_level_4 = 'Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]'
             AND dt.terse_label_level_5 = 'Equity, Including Portion Attributable to Noncontrolling Interest'
             AND fa.value_segment IS NULL
        THEN 'Total Equity'

        /* -------------------------------------------------------
           TOTAL EQUITY — Parent-only fallback (corporations)
           Only fires when the NCI-inclusive version does not
           exist for this specific filing
        ------------------------------------------------------- */
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
                     AND dt2.linkrole = dt.linkrole   -- same linkrole
                 WHERE fa2.filing_key = fa.filing_key
                   AND fa2.terse_label = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                   AND dt2.terse_label_level_4 = 'Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]'
                   AND dt2.terse_label_level_5 = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                   AND fa2.value_segment IS NULL
             )
        THEN 'Total Equity'

        /* -------------------------------------------------------
           TOTAL EQUITY — Partners' Capital (partnerships/REITs)
           RealEstateOperations linkrole only.
           Partners' Capital self-references at level_6
           under Partners' Capital, Including... [Abstract] at level_4
        ------------------------------------------------------- */
        WHEN fa.terse_label = 'Partners Capital, Including Portion Attributable to Noncontrolling Interest'
             AND dt.linkrole = 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
             AND dt.terse_label_level_4 = 'Partners Capital, Including Portion Attributable to Noncontrolling Interest [Abstract]'
             AND fa.value_segment IS NULL
        THEN 'Total Equity'

        /* -------------------------------------------------------
           TOTAL EQUITY — Limited Partners' Capital Account
           RealEstateOperations linkrole, partnerships without
           a rolled-up Partners' Capital total.
           Self-references at level_6 under Partners' Capital [Abstract]
        ------------------------------------------------------- */
        WHEN fa.terse_label = 'Limited Partners'' Capital Account'
             AND dt.linkrole = 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
             AND dt.terse_label_level_5 = 'Partners'' Capital [Abstract]'
             AND dt.terse_label_level_6 = 'Limited Partners'' Capital Account'
             AND fa.value_segment IS NULL
             AND NOT EXISTS (
                 SELECT 1
                 FROM operations.finance_staging.fact_staging_financial_statement fa2
                 JOIN operations.finance.dim_taxonomy dt2
                     ON dt2.terse_label = fa2.terse_label
                     AND dt2.gaap_version = fa2.gaap_version
                     AND dt2.linkrole = dt.linkrole
                 WHERE fa2.filing_key = fa.filing_key
                   AND fa2.terse_label = 'Partners Capital, Including Portion Attributable to Noncontrolling Interest'
                   AND fa2.value_segment IS NULL
             )
        THEN 'Total Equity'

        /* -------------------------------------------------------
           TOTAL LIABILITIES AND EQUITY
           Consistent across all linkroles:
           terse_label self-references at level_4
        ------------------------------------------------------- */
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
WHERE sp_500_indicator = 1
  --AND dc.company_sector = 'Financials'
  --AND dc.company_stock_symbol = 'AAPL'
  AND reported_period = end_reported_period
  AND name_of_submitted_form = '10-Q'
  AND financial_statement = 'BS'
  and value_segment is null
ORDER BY report_number, report_line_number