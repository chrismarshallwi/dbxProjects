INSERT OVERWRITE TABLE IDENTIFIER(:target_catalog || ".finance_staging.raw_pre_tbl") 
select 
*
from (
    select * from operations.finance_staging.raw_2025_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q2_pre_tbl
  )