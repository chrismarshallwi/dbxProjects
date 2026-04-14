insert overwrite TABLE IDENTIFIER(:target_catalog || ".finance.dim_sector") 

with base as (
select distinct
fa.company_bigint_key
,dc.company_name
,standard_industrial_code
,CASE

    -- 🟩 Energy
    WHEN standard_industrial_code BETWEEN 1200 AND 1399 THEN 'Energy'
    WHEN standard_industrial_code BETWEEN 2900 AND 2999 THEN 'Energy'

    -- 🟦 Materials
    WHEN standard_industrial_code BETWEEN 1000 AND 1099 THEN 'Materials'
    WHEN standard_industrial_code BETWEEN 1400 AND 1499 THEN 'Materials'
    WHEN standard_industrial_code BETWEEN 2600 AND 2699 THEN 'Materials'
    WHEN standard_industrial_code BETWEEN 2800 AND 2829 THEN 'Materials'
    WHEN standard_industrial_code BETWEEN 2840 AND 2899 THEN 'Materials'

    -- 🏭 Industrials
    WHEN standard_industrial_code BETWEEN 1500 AND 1799 THEN 'Industrials'
    WHEN standard_industrial_code BETWEEN 2400 AND 2599 THEN 'Industrials'
    WHEN standard_industrial_code BETWEEN 3000 AND 3499 THEN 'Industrials'
    WHEN standard_industrial_code BETWEEN 3500 AND 3569 THEN 'Industrials'
    WHEN standard_industrial_code BETWEEN 3580 AND 3629 THEN 'Industrials'
    WHEN standard_industrial_code BETWEEN 3700 AND 3799 THEN 'Industrials'
    WHEN standard_industrial_code BETWEEN 4000 AND 4799 THEN 'Industrials'

    -- ⚡ Utilities
    WHEN standard_industrial_code BETWEEN 4900 AND 4949 THEN 'Utilities'

    -- 🏢 Real Estate (MUST come before Financials)
    WHEN standard_industrial_code BETWEEN 6500 AND 6599 THEN 'Real Estate'

    -- 🏦 Financials
    WHEN standard_industrial_code BETWEEN 6000 AND 6999 THEN 'Financials'

    -- 💻 Information Technology
    WHEN standard_industrial_code BETWEEN 3570 AND 3579 THEN 'Information Technology'
    WHEN standard_industrial_code BETWEEN 3660 AND 3692 THEN 'Information Technology'
    WHEN standard_industrial_code BETWEEN 7370 AND 7379 THEN 'Information Technology'

    -- 📡 Communication Services
    WHEN standard_industrial_code BETWEEN 4800 AND 4899 THEN 'Communication Services'
    WHEN standard_industrial_code BETWEEN 7800 AND 7899 THEN 'Communication Services'

    -- 🛍️ Consumer Discretionary
    WHEN standard_industrial_code BETWEEN 2300 AND 2399 THEN 'Consumer Discretionary'
    WHEN standard_industrial_code BETWEEN 2500 AND 2519 THEN 'Consumer Discretionary'
    WHEN standard_industrial_code BETWEEN 3600 AND 3659 THEN 'Consumer Discretionary'
    WHEN standard_industrial_code BETWEEN 5000 AND 5999 THEN 'Consumer Discretionary'
    WHEN standard_industrial_code BETWEEN 7000 AND 7199 THEN 'Consumer Discretionary'
    WHEN standard_industrial_code BETWEEN 7500 AND 7599 THEN 'Consumer Discretionary'

    -- 🥤 Consumer Staples
    WHEN standard_industrial_code BETWEEN 0100 AND 0999 THEN 'Consumer Staples'
    WHEN standard_industrial_code BETWEEN 2000 AND 2099 THEN 'Consumer Staples'
    WHEN standard_industrial_code BETWEEN 2100 AND 2199 THEN 'Consumer Staples'
    WHEN standard_industrial_code BETWEEN 5400 AND 5499 THEN 'Consumer Staples'

    -- 🧬 Health Care
    WHEN standard_industrial_code BETWEEN 2830 AND 2839 THEN 'Health Care'
    WHEN standard_industrial_code = 3693 THEN 'Health Care'
    WHEN standard_industrial_code BETWEEN 8000 AND 8099 THEN 'Health Care'

    ELSE 'Unclassified'

END AS gics_sector

from 
operations.finance_staging.fact_staging_financial_statement fa
left join 
operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
where fa.company_bigint_key is not null
)


,filter_rows as (
select 
*
,CASE WHEN COUNT(*) OVER (PARTITION BY company_bigint_key) >= 2 THEN 1 ELSE 0 END AS has_multiple_rows
,dense_rank() over (partition by company_bigint_key order by gics_sector) dense_rank_sector
from 
base
)

select distinct 
company_bigint_key
,gics_sector

 from filter_rows
 where dense_rank_sector = 1




