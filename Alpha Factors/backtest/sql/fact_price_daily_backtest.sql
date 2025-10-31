
with prices as (SELECT 
    symbol
    ,date_value
    ,close
FROM 
    operations.finance.fact_price_daily 
order by 
    symbol
    ,date_value desc
) 
select distinct * from prices





