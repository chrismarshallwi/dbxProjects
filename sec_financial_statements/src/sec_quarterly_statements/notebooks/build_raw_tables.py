# Databricks notebook source
import pandas as pd
from pyspark.sql.functions import lit

catalog = 'operations'
schema = 'finance_staging'

volume_base = "/Volumes/operations/finance_staging/edgar_data"

years = ['2025']
quarters = ['q1','q2']

files = ['pre','num','sub','tag']

for year in years:
    for quarter in quarters:
        for file in files:
            filing_path = f"{volume_base}/{year}/{quarter}/{file}.txt"
            filing = pd.read_csv(f"{filing_path}", sep="\t", low_memory=False, keep_default_na=False)
            filing = (
                spark.read
                .option("sep", "\t")
                .option("header", "true")
                .option("inferSchema", "true")
                .option("nullValue", "")
                .csv(filing_path)
            )

            filing = (
                filing
                .withColumn("source_file", lit(filing_path))
                .withColumn("source_file_description", lit(f"{year}_{quarter}_{file}"))
            )
            (
                filing.write
                .mode("overwrite")
                .option("overwriteSchema", "true")
                .saveAsTable(f'{catalog}.{schema}.raw_{year}_{quarter}_{file}_tbl')
            )
