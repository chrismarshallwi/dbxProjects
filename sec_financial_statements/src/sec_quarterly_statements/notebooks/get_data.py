# Databricks notebook source
import requests
import zipfile
from io import BytesIO

years = ['2025']
quarters = ['q1','q2']

edgar_base_url = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/"
volume_base_path = "/Volumes/operations/finance_staging/edgar_data"

def download_and_unzip(url, extract_to):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 (Contact: your-email@example.com)'
    }
    
    print(f"Downloading ZIP file from {url} ...")
    response = requests.get(url, headers=headers)
    
    response.raise_for_status()
    
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    
    print(f"Extracting the contents to {extract_to}...")
    zip_file.extractall(path=extract_to)
    zip_file.close()

for year in years:
    for quarter in quarters:
        edgar_url = f"{edgar_base_url}{year}{quarter}.zip" 
        volume_path = f"{volume_base_path}/{year}/{quarter}/"
        download_and_unzip(url = edgar_url, extract_to= volume_path)