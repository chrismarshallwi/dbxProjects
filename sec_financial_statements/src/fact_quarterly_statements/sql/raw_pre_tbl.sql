INSERT OVERWRITE TABLE IDENTIFIER(:target_catalog || ".finance_staging.raw_pre_tbl") 
select 
*
from (
    select * from operations.finance_staging.raw_2025_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q2_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q3_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2025_q4_pre_tbl
/*2024*/
union all 
        select * from operations.finance_staging.raw_2024_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2024_q2_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2024_q3_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2024_q4_pre_tbl
/*2023*/
union
        select * from operations.finance_staging.raw_2023_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2023_q2_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2023_q3_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2023_q4_pre_tbl
/*2022*/
union all
        select * from operations.finance_staging.raw_2022_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2022_q2_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2022_q3_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2022_q4_pre_tbl
/*2021*/
union all
        select * from operations.finance_staging.raw_2021_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2021_q2_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2021_q3_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2021_q4_pre_tbl
/*2020*/
union all
        select * from operations.finance_staging.raw_2020_q1_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2020_q2_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2020_q3_pre_tbl
    union all 
    select * from operations.finance_staging.raw_2020_q4_pre_tbl
  )