select 
*
from (
    select * from operations.finance_staging.raw_2025_q1_sub_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q2_sub_tbl
  )