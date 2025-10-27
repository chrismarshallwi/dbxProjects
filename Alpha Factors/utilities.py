import pandas as pd 
import yfinance as yf
import yaml
import requests
from io import StringIO

def read_yaml_file(file_path):
    '''
    Access keys in yaml file
    '''
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

yaml_path = '/Workspace/Users/chrismarshall.wi@icloud.com/dbxProjects/Alpha Factors/.gitignore/connections.yaml'
config_data = read_yaml_file(yaml_path)
url_sp = config_data.get('spurl')

class Market():
    def __init__(self, tickers, start, end):
        self.tickers = tickers #what market are we creating?
        self.start = start #Start date 
        self.end = end #end date
    
    def get_price(self):
        data = yf.download(self.tickers, start=self.start, end=self.end, group_by='ticker')

        all_data = []
        for ticker in self.tickers:
            df = data[ticker].copy()
            df.insert(0, 'Symbol', ticker)
            all_data.append(df)

        return pd.concat(all_data)

class Tickers():
    def __init__(self):
        pass

    # def get_tickers_sp():
    #     '''
    #     SP 500 Tickers
    #     '''
    #     ticker_list = []
    #     tickers = pd.read_html(url_sp)[0].Symbol.to_list()
    #     return tickers

    def get_tickers_sp():
    
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        } #assign a fake user agent because Wikipedia blocks requests without one

        response = requests.get(url_sp, headers=headers)
        response.raise_for_status()

        tables = pd.read_html(StringIO(response.text))
        df = tables[0]
        return df['Symbol'].tolist()

