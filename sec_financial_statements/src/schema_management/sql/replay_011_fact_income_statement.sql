create or replace table operations.finance.fact_income_statement (
    
    company_bigint_key bigint
    ,date_key_reported_period BIGINT comment "Date key that is the reported period of financial reporting as sourced from EDGAR data."
    ,date_key_converted_period bigint comment "Date key that has been fitted into a uniform 4-quarter year based on how the company reported fiscally. If a company reports Q4 for 2022 in the year 2023, this is fitted so that all companies uniformly appear as having the same quarters. This is important when comparing companies that might have different fiscal reporting periods."
    ,submitted_form_business_key integer comment "Signifies what form was submitted. Typically, 10-Q's are filed ever quarter and 10-K's are filed annually. Some (Most) companies file 3 10-Q's and 1 10-K per year."
    ,reported_quarters integer comment "Signifies how many quarters are reported in the financial statement. This is typically 4 quarters for 10-K's and 1 for 10-Q's"
    ,total_revenue double comment "Total revenue as reported in the income statement including all segments."
    
)
using delta 
comment "This table contains income statement data for publicly traded companies as reported to the SEC. It includes data pertaining to high level line items on the income statement. This can be used for financial analysis, Profitibility analysis, and growth analysis."
