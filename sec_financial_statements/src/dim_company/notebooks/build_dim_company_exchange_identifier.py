# Databricks notebook source
import requests
import pandas as pd
from pyspark.sql import SparkSession

catalog = 'operations'
schema = 'finance_staging'
table_name = 'raw_dim_exchange'

spark = SparkSession.builder.getOrCreate()

url = "https://www.sec.gov/files/company_tickers_exchange.json"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 (Contact: your-email@example.com)'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

columns = data["fields"]
rows = data["data"]

df = pd.DataFrame(rows, columns=columns)

df.columns = df.columns.str.lower()
spark_df = spark.createDataFrame(df)

spark_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{table_name}")