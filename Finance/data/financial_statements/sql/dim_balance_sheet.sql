with balance_sheet_schema as (
select 

  balance_sheet.report_label
  ,company.company_bigint_key
  ,balance_sheet.report_label_bigint_key
  ,dates.reported_period as date_key

from 
  operations.finance_staging.dim_report_labels balance_sheet
cross join 
  operations.finance.dim_company company 
cross join 
(
  select distinct 
  reported_period
  from operations.finance_staging.fact_staging_financial_statement_tbl
  /*where reported_period in (20241231,20250331)
) dates
where 
  company.company_stock_symbol in ('AAPL','WMT','AMZN','ABBV','AMD','T','NVDA')*/
)

,dim_company_presented_labels as (select distinct
            dpl.report_label_bigint_key
            ,dpl.presented_label_bigint_key
            ,fsm.company_bigint_key
            /*,fsm.presented_label_bigint_key*/
            ,fsm.company_stock_symbol
            ,fsm.presented_label
          from 
            operations.finance_staging.dim_presented_labels dpl
          left join 
            (select 
              fsm.presented_label
              ,fsm.presented_label_bigint_key
              ,dc.company_stock_symbol
              ,dc.company_bigint_key
              from 
              operations.finance_staging.fact_staging_financial_statement_tbl fsm
              left join 
              operations.finance.dim_company dc on dc.company_bigint_key=fsm.company_bigint_key
              where 
              fsm.financial_statement = 'BS'  and fsm.value_segment is null
              and 
              fsm.reported_period = fsm.end_reported_period 
              /*and 
              dc.company_stock_symbol in ('AAPL','WMT','AMZN','ABBV','AMD','T','NVDA')*/
            ) fsm on fsm.presented_label_bigint_key = dpl.presented_label_bigint_key

          where 
            fsm.company_stock_symbol is not null
)

,final as (
select distinct
    dcpl.report_label_bigint_key as report_label_bigint_key
    ,dcpl.presented_label_bigint_key as presented_label_bigint_key
    ,bss.company_bigint_key as company_bigint_key
    ,bss.report_label as report_label
    ,bss.date_key as date_key
    ,dcpl.presented_label as presented_label
    ,dcpl.company_stock_symbol as company_stock_symbol
from 
    balance_sheet_schema bss
left join 
    dim_company_presented_labels dcpl on 
(
  dcpl.report_label_bigint_key=bss.report_label_bigint_key
  and 
  dcpl.company_bigint_key = bss.company_bigint_key
)
)

select * from final