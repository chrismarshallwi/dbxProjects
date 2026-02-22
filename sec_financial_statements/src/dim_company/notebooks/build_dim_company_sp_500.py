# Databricks notebook source
import requests
import pandas as pd
from pyspark.sql import SparkSession

##need to install lxml in job.yml file

catalog = 'operations'
schema = 'finance_staging'
table_name = 'raw_dim_sp_500'

spark = SparkSession.builder.getOrCreate()

wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
wiki_headers = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) '
        'Version/17.4 Safari/605.1.15'
    )
}

session = requests.Session()
session.headers.update(wiki_headers)

html = session.get(wiki_url).text
tables = pd.read_html(html, header=0)
df_sp500 = tables[0]

df_sp500.rename(columns={'Symbol': 'ticker'}, inplace=True)
df_sp500['ticker'] = df_sp500['ticker'].str.upper()

df = df_sp500.rename(columns ={'GICS Sector':'gics_sector','GICS Sub-Industry':'gics_sub_industry','Headquarters Location':'headquarters_location','Date added':'date_added'},inplace=True)

df = spark.createDataFrame(df_sp500)

df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{table_name}")