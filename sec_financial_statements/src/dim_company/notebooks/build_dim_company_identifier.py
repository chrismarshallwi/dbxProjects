# Databricks notebook source
import requests
import pandas as pd

catalog = 'operations'
schema = 'finance_staging'
table_name = 'raw_dim_cik'

url = "https://www.sec.gov/files/company_tickers.json"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 (Contact: your-email@example.com)'
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()
df = pd.DataFrame.from_dict(data, orient='index').rename(columns = {'cik_str':'cik'})
df = spark.createDataFrame(df)

df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{table_name}")