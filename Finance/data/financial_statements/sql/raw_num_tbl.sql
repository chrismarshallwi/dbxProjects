select 
*
from (
    select * from operations.finance_staging.raw_2025_q1_num_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q2_num_tbl
  )