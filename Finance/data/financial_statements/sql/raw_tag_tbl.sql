select 
*
from (
    select * from operations.finance_staging.raw_2025_q1_tag_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q2_tag_tbl
  )