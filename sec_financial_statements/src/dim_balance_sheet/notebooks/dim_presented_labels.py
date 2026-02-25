# Databricks notebook source
catalog = 'operations'
schema = 'finance_staging'
table_name = 'dim_presented_labels'

import json
import pandas as pd

json_files = ['dim_presented_labels']

df_x = [] 

for file in json_files:
    with open(f"../json/{file}.json", "r") as f:
        qry = json.load(f)

    rows = []

    for main_category, level1 in qry.items():
        for sub_category, level2 in level1.items():
            for item_category, inner in level2.items():
                labels = inner.get("presented_labels", [])
                for label in labels:
                    rows.append({
                        "report": main_category,
                        "report_class": sub_category,
                        "report_label": item_category,
                        "presented_label": label
                    })

    df_x.append(pd.DataFrame(rows))

df = spark.createDataFrame(pd.concat(df_x, ignore_index=True))
df.createOrReplaceTempView("presented_labels")

presented_labels = spark.sql(f"""
select distinct 
    presented_labels.*
    ,cast(bigint(substr(xxhash64(concat_ws('|', presented_labels.presented_label)), 1, 18)) as bigint) AS presented_label_bigint_key 
    ,bigint(substr(xxhash64(concat_ws('|', presented_labels.report_label)), 1, 18)) AS report_label_bigint_key 
from 
    presented_labels""")

(
presented_labels
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{catalog}.{schema}.{table_name}")
)