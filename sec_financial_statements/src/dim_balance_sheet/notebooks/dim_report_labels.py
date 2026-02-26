# Databricks notebook source
catalog = 'operations'
schema = 'finance_staging'
table_name = 'dim_report_labels'

import json

with open(f"../json/dim_report_labels.json","r") as f:
    qry = json.load(f)

df = spark.createDataFrame(qry).createOrReplaceTempView('totals')

report_labels = spark.sql(f"""
                          select distinct 
totals.*
,cast(bigint(substr(xxhash64(concat_ws('|', totals.report_label)), 1, 18)) as bigint) AS report_label_bigint_key 
from totals""")

(
    report_labels
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{catalog}.{schema}.{table_name}")
)