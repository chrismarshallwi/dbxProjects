insert overwrite IDENTIFIER(:target_catalog || '.finance.fact_balance_sheet')
WITH cte AS (
    SELECT DISTINCT
         dc.company_bigint_key
        ,reported_period as date_key
        ,value
        ,dt.terse_label
        ,name_of_submitted_form as name_of_submitted_form

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

            WHEN fa.terse_label = 'Equity, Attributable to Parent'
                 AND dt.terse_label_level_4 = 'Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]'
                 AND dt.terse_label_level_5 = 'Equity, Attributable to Parent [Abstract]'
                 AND dt.terse_label_level_6 = 'Equity, Attributable to Parent'
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

            WHEN fa.terse_label = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                 AND dt.terse_label_level_4 = 'Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]'
                 AND dt.terse_label_level_5 = 'Equity, Including Portion Attributable to Noncontrolling Interest'
                 AND dt.linkrole = dc.preferred_fasb_linkrole_balance_sheet
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            WHEN fa.terse_label = 'Partners Capital, Including Portion Attributable to Noncontrolling Interest'
                 AND dt.linkrole = 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            WHEN fa.terse_label = "Limited Partners' Capital Account"
                 AND dt.linkrole = 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            -- NEW: Stockholders' Equity taxonomy naming (prevalent in 2022/2023 data)

            WHEN fa.terse_label = "Stockholders' Equity, Including Portion Attributable to Noncontrolling Interest"
                 AND dt.terse_label_level_4 = "Stockholders' Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]"
                 AND dt.terse_label_level_5 = "Stockholders' Equity, Including Portion Attributable to Noncontrolling Interest"
                 AND fa.value_segment IS NULL
            THEN 'Total Equity'

            WHEN fa.terse_label = "Stockholders' Equity Attributable to Parent"
                 AND dt.terse_label_level_4 = "Stockholders' Equity, Including Portion Attributable to Noncontrolling Interest [Abstract]"
                 AND dt.terse_label_level_5 = "Stockholders' Equity Attributable to Parent [Abstract]"
                 AND dt.terse_label_level_6 = "Stockholders' Equity Attributable to Parent"
                 AND fa.value_segment IS NULL
                 AND NOT EXISTS (
                     SELECT 1
                     FROM operations.finance_staging.fact_staging_financial_statement fa2
                     JOIN operations.finance.dim_taxonomy dt2
                         ON dt2.terse_label = fa2.terse_label
                         AND dt2.gaap_version = fa2.gaap_version
                         AND dt2.linkrole = dt.linkrole
                     WHERE fa2.filing_key = fa.filing_key
                       AND fa2.terse_label = "Stockholders' Equity, Including Portion Attributable to Noncontrolling Interest"
                       AND fa2.value_segment IS NULL
                 )
            THEN 'Total Equity'

            WHEN fa.terse_label = 'Liabilities and Equity'
                 AND dt.terse_label_level_4 = 'Liabilities and Equity'
                 AND fa.value_segment IS NULL
            THEN 'Total Liabilities and Equity'

            -- Subtotals
            WHEN fa.terse_label = 'Assets, Current'
                 AND fa.value_segment IS NULL
            THEN 'Total Current Assets'

            WHEN fa.terse_label = 'Assets, Noncurrent'
                 AND fa.value_segment IS NULL
            THEN 'Total Non Current Assets'

            WHEN fa.terse_label = 'Liabilities, Current'
                 AND fa.value_segment IS NULL
            THEN 'Total Current Liabilities'

            WHEN fa.terse_label = 'Liabilities, Noncurrent'
                 AND fa.value_segment IS NULL
            THEN 'Total Non Current Liabilities'
            ELSE NULL
        END AS bs_component

    FROM operations.finance_staging.fact_staging_financial_statement fa
    LEFT JOIN operations.finance.dim_taxonomy dt ON dt.terse_label = fa.terse_label AND dt.gaap_version = fa.gaap_version
    --LEFT JOIN operations.finance.dim_company dc ON dc.company_bigint_key = fa.company_bigint_key AND dc.preferred_fasb_linkrole_balance_sheet = dt.linkrole
    left join operations.finance.dim_sector dc on 
    (
      dc.company_bigint_key = fa.company_bigint_key 
      and 
      dc.date_key = fa.reported_period
      and 
      dc.preferred_fasb_linkrole_balance_sheet = dt.linkrole
    )
    WHERE 
      reported_period = end_reported_period
      AND name_of_submitted_form in ('10-Q','10-K') --going to make change soon to include 10-K so that we get continuous reporting periods (4 times per year)
      AND financial_statement = 'BS'
      AND value_segment IS NULL

)


SELECT
     cte.company_bigint_key
     ,cte.date_key
     ,case when ds.gics_sector in ('Financials', 'Real Estate') then 1 else 0 end as capital_structure_business_key
     ,case when cte.name_of_submitted_form = '10-Q' then 0 when cte.name_of_submitted_form = '10-K' then 1 else null end as submitted_form_business_key 

    ,MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) AS total_assets

    ,CASE 
        WHEN MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) IS NULL 
             AND MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) IS NOT NULL 
        THEN MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) 
             - MAX(CASE WHEN bs_component = 'Total Equity' THEN value END)
        ELSE MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) 
     END AS total_liabilities

     /*Total Equity*/

    ,CASE 
        WHEN MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) IS NULL 
             AND CASE 
                     WHEN MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) IS NULL 
                          AND MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) IS NOT NULL 
                     THEN MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) 
                          - MAX(CASE WHEN bs_component = 'Total Equity' THEN value END)
                     ELSE MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) 
                 END IS NOT NULL
        THEN MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) 
             - CASE 
                   WHEN MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) IS NULL 
                        AND MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) IS NOT NULL 
                   THEN MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) 
                        - MAX(CASE WHEN bs_component = 'Total Equity' THEN value END)
                   ELSE MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) 
               END
        ELSE MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) 
     END AS total_equity

    ,MAX(CASE WHEN bs_component = 'Total Liabilities and Equity' THEN value END) AS total_liabilities_and_equity

    -- Asset subtotals
    ,MAX(CASE WHEN bs_component = 'Total Current Assets' THEN value END) AS total_current_assets

    ,case when (MAX(CASE WHEN bs_component = 'Total Current Assets' THEN value END)) is not null 
    and 
    MAX(CASE WHEN bs_component = 'Total Non Current Assets' THEN value END) is null 
    then 
    ( MAX(CASE WHEN bs_component = 'Total Assets' THEN value END)) - (MAX(CASE WHEN bs_component = 'Total Current Assets' THEN value END))
    else 
    MAX(CASE WHEN bs_component = 'Total Non Current Assets' THEN value END)
    end AS total_non_current_assets

    -- Liability subtotals
    ,MAX(CASE WHEN bs_component = 'Total Current Liabilities' THEN value END) AS total_current_liabilities

    ,case when (MAX(CASE WHEN bs_component = 'Total Current Liabilities' THEN value END)) is not null 
    and 
    (MAX(CASE WHEN bs_component = 'Total Non Current Liabilities' THEN value END)) is null 
    then 
    ( CASE 
        WHEN MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) IS NULL 
             AND MAX(CASE WHEN bs_component = 'Total Equity' THEN value END) IS NOT NULL 
        THEN MAX(CASE WHEN bs_component = 'Total Assets' THEN value END) 
             - MAX(CASE WHEN bs_component = 'Total Equity' THEN value END)
        ELSE MAX(CASE WHEN bs_component = 'Total Liabilities' THEN value END) 
     END ) - (MAX(CASE WHEN bs_component = 'Total Current Liabilities' THEN value END))
    else 
    MAX(CASE WHEN bs_component = 'Total Non Current Liabilities' THEN value END)
    end AS total_non_current_liabilities

FROM 
cte  
LEFT JOIN 
operations.finance.dim_company dc oN dc.company_bigint_key = cte.company_bigint_key
left join operations.finance.dim_sector ds on 
(
ds.company_bigint_key = cte.company_bigint_key 
and 
ds.date_key = cte.date_key
)
WHERE 
bs_component IS NOT NULL
and
dc.company_bigint_key is not null 
GROUP BY
cte.company_bigint_key
,cte.date_key
,case when ds.gics_sector in ('Financials', 'Real Estate') then 1 else 0 end
,case when cte.name_of_submitted_form = '10-Q' then 0 when cte.name_of_submitted_form = '10-K' then 1 else null end
ORDER BY
cte.company_bigint_key
,cte.date_key




