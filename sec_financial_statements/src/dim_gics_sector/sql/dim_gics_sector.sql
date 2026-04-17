insert overwrite TABLE IDENTIFIER(:target_catalog || ".finance.dim_sector") 

with base as (
select distinct
fa.company_bigint_key
,dc.company_name
,dc.company_identifier_key
,fa.reported_period as date_key

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

,CASE

    -- 🟩 ENERGY
    WHEN standard_industrial_code BETWEEN 1310 AND 1389 THEN 'Oil & Gas Exploration & Production'
    WHEN standard_industrial_code BETWEEN 2910 AND 2999 THEN 'Oil & Gas Refining & Marketing'
    WHEN standard_industrial_code BETWEEN 1380 AND 1389 THEN 'Oil & Gas Equipment & Services'
    WHEN standard_industrial_code BETWEEN 4920 AND 4939 THEN 'Oil & Gas Storage & Transportation'
    WHEN standard_industrial_code BETWEEN 4900 AND 4911 THEN 'Independent Power Producers & Energy Traders'

    -- 🟦 MATERIALS
    WHEN standard_industrial_code BETWEEN 2810 AND 2829 THEN 'Commodity Chemicals'
    WHEN standard_industrial_code BETWEEN 2830 AND 2839 THEN 'Pharmaceuticals'
    WHEN standard_industrial_code BETWEEN 2840 AND 2899 THEN 'Specialty Chemicals'
    WHEN standard_industrial_code BETWEEN 2870 AND 2879 THEN 'Fertilizers & Agricultural Chemicals'
    WHEN standard_industrial_code BETWEEN 1000 AND 1049 THEN 'Gold'
    WHEN standard_industrial_code BETWEEN 1400 AND 1499 THEN 'Construction Materials'
    WHEN standard_industrial_code BETWEEN 2600 AND 2679 THEN 'Paper & Plastic Packaging Products & Materials'
    WHEN standard_industrial_code BETWEEN 3350 AND 3359 THEN 'Copper'
    WHEN standard_industrial_code BETWEEN 3310 AND 3319 THEN 'Steel'

    -- 🏭 INDUSTRIALS
    WHEN standard_industrial_code BETWEEN 3510 AND 3539 THEN 'Construction Machinery & Heavy Transportation Equipment'
    WHEN standard_industrial_code BETWEEN 3540 AND 3569 THEN 'Industrial Machinery & Supplies & Components'
    WHEN standard_industrial_code BETWEEN 3710 AND 3719 THEN 'Automotive Parts & Equipment'
    WHEN standard_industrial_code BETWEEN 3720 AND 3729 THEN 'Aerospace & Defense'
    WHEN standard_industrial_code BETWEEN 3730 AND 3739 THEN 'Industrial Conglomerates'
    WHEN standard_industrial_code BETWEEN 4000 AND 4099 THEN 'Rail Transportation'
    WHEN standard_industrial_code BETWEEN 4510 AND 4519 THEN 'Passenger Airlines'
    WHEN standard_industrial_code BETWEEN 4210 AND 4219 THEN 'Cargo Ground Transportation'
    WHEN standard_industrial_code BETWEEN 4730 AND 4739 THEN 'Air Freight & Logistics'
    WHEN standard_industrial_code BETWEEN 7360 AND 7369 THEN 'Human Resource & Employment Services'
    WHEN standard_industrial_code BETWEEN 8710 AND 8719 THEN 'Research & Consulting Services'

    -- ⚡ UTILITIES
    WHEN standard_industrial_code BETWEEN 4910 AND 4919 THEN 'Electric Utilities'
    WHEN standard_industrial_code BETWEEN 4920 AND 4929 THEN 'Gas Utilities'
    WHEN standard_industrial_code BETWEEN 4930 AND 4939 THEN 'Multi-Utilities'
    WHEN standard_industrial_code BETWEEN 4940 AND 4949 THEN 'Water Utilities'

    -- 🏢 REAL ESTATE
    WHEN standard_industrial_code BETWEEN 6510 AND 6519 THEN 'Multi-Family Residential REITs'
    WHEN standard_industrial_code BETWEEN 6520 AND 6529 THEN 'Office REITs'
    WHEN standard_industrial_code BETWEEN 6530 AND 6539 THEN 'Real Estate Services'
    WHEN standard_industrial_code BETWEEN 6540 AND 6549 THEN 'Self-Storage REITs'
    WHEN standard_industrial_code BETWEEN 6550 AND 6559 THEN 'Single-Family Residential REITs'
    WHEN standard_industrial_code BETWEEN 6798 AND 6798 THEN 'Other Specialized REITs'

    -- 🏦 FINANCIALS
    WHEN standard_industrial_code BETWEEN 6020 AND 6029 THEN 'Regional Banks'
    WHEN standard_industrial_code BETWEEN 6021 AND 6022 THEN 'Diversified Banks'
    WHEN standard_industrial_code BETWEEN 6030 AND 6039 THEN 'Consumer Finance'
    WHEN standard_industrial_code BETWEEN 6210 AND 6219 THEN 'Investment Banking & Brokerage'
    WHEN standard_industrial_code BETWEEN 6280 AND 6289 THEN 'Asset Management & Custody Banks'
    WHEN standard_industrial_code BETWEEN 6310 AND 6319 THEN 'Life & Health Insurance'
    WHEN standard_industrial_code BETWEEN 6330 AND 6339 THEN 'Property & Casualty Insurance'
    WHEN standard_industrial_code BETWEEN 6350 AND 6359 THEN 'Reinsurance'
    WHEN standard_industrial_code BETWEEN 6410 AND 6419 THEN 'Insurance Brokers'

    -- 💻 INFORMATION TECHNOLOGY
    WHEN standard_industrial_code BETWEEN 3570 AND 3579 THEN 'Technology Hardware, Storage & Peripherals'
    WHEN standard_industrial_code BETWEEN 3660 AND 3669 THEN 'Communications Equipment'
    WHEN standard_industrial_code BETWEEN 3670 AND 3679 THEN 'Semiconductors'
    WHEN standard_industrial_code BETWEEN 3820 AND 3829 THEN 'Electronic Equipment & Instruments'
    WHEN standard_industrial_code BETWEEN 7370 AND 7372 THEN 'Application Software'
    WHEN standard_industrial_code BETWEEN 7373 AND 7379 THEN 'IT Consulting & Other Services'
    WHEN standard_industrial_code BETWEEN 7374 AND 7374 THEN 'Data Processing & Outsourced Services'

    -- 📡 COMMUNICATION SERVICES
    WHEN standard_industrial_code BETWEEN 4810 AND 4819 THEN 'Integrated Telecommunication Services'
    WHEN standard_industrial_code BETWEEN 4820 AND 4829 THEN 'Wireless Telecommunication Services'
    WHEN standard_industrial_code BETWEEN 4830 AND 4839 THEN 'Broadcasting'
    WHEN standard_industrial_code BETWEEN 4840 AND 4849 THEN 'Cable & Satellite'
    WHEN standard_industrial_code BETWEEN 7375 AND 7375 THEN 'Interactive Media & Services'
    WHEN standard_industrial_code BETWEEN 7810 AND 7819 THEN 'Movies & Entertainment'
    WHEN standard_industrial_code BETWEEN 7820 AND 7829 THEN 'Interactive Home Entertainment'

    -- 🛍️ CONSUMER DISCRETIONARY
    WHEN standard_industrial_code BETWEEN 2300 AND 2399 THEN 'Apparel, Accessories & Luxury Goods'
    WHEN standard_industrial_code BETWEEN 2510 AND 2519 THEN 'Homefurnishing Retail'
    WHEN standard_industrial_code BETWEEN 3710 AND 3711 THEN 'Automobile Manufacturers'
    WHEN standard_industrial_code BETWEEN 5510 AND 5519 THEN 'Automotive Retail'
    WHEN standard_industrial_code BETWEEN 5600 AND 5699 THEN 'Apparel Retail'
    WHEN standard_industrial_code BETWEEN 5700 AND 5799 THEN 'Home Improvement Retail'
    WHEN standard_industrial_code BETWEEN 5800 AND 5819 THEN 'Restaurants'
    WHEN standard_industrial_code BETWEEN 7000 AND 7019 THEN 'Hotels, Resorts & Cruise Lines'
    WHEN standard_industrial_code BETWEEN 7990 AND 7999 THEN 'Casinos & Gaming'
    WHEN standard_industrial_code BETWEEN 5940 AND 5949 THEN 'Other Specialty Retail'

    -- 🥤 CONSUMER STAPLES
    WHEN standard_industrial_code BETWEEN 2000 AND 2049 THEN 'Packaged Foods & Meats'
    WHEN standard_industrial_code BETWEEN 2080 AND 2089 THEN 'Brewers'
    WHEN standard_industrial_code BETWEEN 2085 AND 2085 THEN 'Distillers & Vintners'
    WHEN standard_industrial_code BETWEEN 2090 AND 2099 THEN 'Food Distributors'
    WHEN standard_industrial_code BETWEEN 2100 AND 2199 THEN 'Tobacco'
    WHEN standard_industrial_code BETWEEN 5400 AND 5499 THEN 'Food Retail'
    WHEN standard_industrial_code BETWEEN 5600 AND 5699 THEN 'Consumer Staples Merchandise Retail'
    WHEN standard_industrial_code BETWEEN 2840 AND 2849 THEN 'Household Products'
    WHEN standard_industrial_code BETWEEN 2800 AND 2809 THEN 'Personal Care Products'

    -- 🧬 HEALTH CARE
    WHEN standard_industrial_code BETWEEN 2830 AND 2839 THEN 'Pharmaceuticals'
    WHEN standard_industrial_code BETWEEN 3840 AND 3849 THEN 'Health Care Equipment'
    WHEN standard_industrial_code BETWEEN 3850 AND 3859 THEN 'Health Care Supplies'
    WHEN standard_industrial_code BETWEEN 8000 AND 8099 THEN 'Health Care Services'
    WHEN standard_industrial_code BETWEEN 8060 AND 8069 THEN 'Health Care Facilities'
    WHEN standard_industrial_code BETWEEN 8070 AND 8079 THEN 'Life Sciences Tools & Services'
    WHEN standard_industrial_code BETWEEN 8090 AND 8099 THEN 'Managed Health Care'
    WHEN standard_industrial_code BETWEEN 8730 AND 8739 THEN 'Biotechnology'

    ELSE 'Unclassified'

END AS gics_sub_industry

,CASE

    -- 🏦 FINANCIALS (Income Statement Variants)
    WHEN gics_sector = 'Financials' AND gics_sub_industry IN (
        'Regional Banks','Diversified Banks','Consumer Finance'
    )
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfIncomeInterestBasedRevenue'

    WHEN gics_sector = 'Financials' AND gics_sub_industry IN (
        'Life & Health Insurance','Property & Casualty Insurance','Reinsurance'
    )
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfIncomeInsuranceBasedRevenue'

    WHEN gics_sector = 'Financials' AND gics_sub_industry IN (
        'Asset Management & Custody Banks','Investment Banking & Brokerage'
    )
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfIncomeSecuritiesBasedIncome'


    -- 🏢 REAL ESTATE
    WHEN gics_sector = 'Real Estate' AND gics_sub_industry LIKE '%REIT%'
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfIncomeRealEstateInvestmentTrusts'

    WHEN gics_sector = 'Real Estate'
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfIncomeRealEstateExcludingREITs'


    -- 🧾 BALANCE SHEET SPECIAL CASES

    -- Deposit-based (banks)
    WHEN gics_sector = 'Financials' AND gics_sub_industry IN (
        'Regional Banks','Diversified Banks'
    )
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'

    -- Securities-based (asset managers, brokers)
    WHEN gics_sector = 'Financials' AND gics_sub_industry IN (
        'Asset Management & Custody Banks','Investment Banking & Brokerage'
    )
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-SecuritiesBasedOperations'

    -- Real estate balance sheet
    WHEN gics_sector = 'Real Estate'
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'


    -- 🧠 FALLBACKS

    WHEN gics_sector IN ('Information Technology','Communication Services')
        THEN 'http://fasb.org/us-gaap/role/statement/StatementOfIncomeAlternateAggregations'

    -- Default standard statements
    ELSE 'http://fasb.org/us-gaap/role/statement/StatementOfIncome'

END AS preferred_fasb_linkrole_income_statement

from 
operations.finance_staging.fact_staging_financial_statement fa
left join 
operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
where fa.company_bigint_key is not null
)

select distinct 
company_bigint_key
,date_key
,standard_industrial_code
,gics_sector
,gics_sub_industry


  ,case
    -- Financials: sub-industry specific
    when gics_sub_industry = 'Diversified Banks'                           then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'
    when gics_sub_industry = 'Regional Banks'                              then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'
    when gics_sub_industry = 'Consumer Finance'                            then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-DepositBasedOperations'
    when gics_sub_industry = 'Asset Management & Custody Banks'            then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
    when gics_sub_industry = 'Property & Casualty Insurance'               then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
    when gics_sub_industry = 'Life & Health Insurance'                     then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
    when gics_sub_industry = 'Multi-line Insurance'                        then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
    when gics_sub_industry = 'Reinsurance'                                 then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-InvestmentBasedOperations'
    when gics_sub_industry = 'Investment Banking & Brokerage'              then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-SecuritiesBasedOperations'
    when gics_sub_industry = 'Financial Exchanges & Data'                  then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionUnclassified-SecuritiesBasedOperations'
    when gics_sub_industry = 'Transaction & Payment Processing Services'   then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified'
    when gics_sub_industry = 'Insurance Brokers'                           then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified'
    -- Real Estate: sector level
    when gics_sector = 'Real Estate'                                       then 'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified-RealEstateOperations'
    -- All other sectors default to Classified
    else                                                                        'http://fasb.org/us-gaap/role/statement/StatementOfFinancialPositionClassified'
  end                                                                              as preferred_fasb_linkrole_balance_sheet

, preferred_fasb_linkrole_income_statement

 from base