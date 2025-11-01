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
        self.tickers = tickers #what market are we creating? (Investment Universe)
        self.start = start #Start date 
        self.end = end #end date
    
    def get_price(self):
        data = yf.download(self.tickers, start=self.start, end=self.end, group_by='ticker')

        all_data = []
        for ticker in self.tickers:
            df = data[ticker].copy()
            df = df.reset_index()
            df.insert(0, 'Symbol', ticker)
            all_data.append(df)

        final_df = pd.concat(all_data, ignore_index=True)
        return final_df

class Tickers():
    def __init__(self):
        pass

    def get_tickers_sp():
    
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        } #assign a fake user agent because Wikipedia blocks requests without one

        response = requests.get(url_sp, headers=headers)
        response.raise_for_status()

        tables = pd.read_html(StringIO(response.text))
        df = tables[0]
        return df['Symbol'].tolist()
    
class Factor:
    def __init__(self, data: pd.DataFrame):
        
        columns = ['symbol','date_value','close']
        if list(self.data.columns) != columns:
            raise ValueError(f"Columns must be {columns}")

        self.data = data.copy()

    def data(self):
        return self.data

    def moving_average(self,window:int=200):
        '''
        Moving Average
        Default: 200 Days
        ''' 
        pass
    def bbands(self,std_dev:float):
        '''
        Bollinger Bands
        '''
        pass
    def rsi(self):
        pass
    def returns(self,days:int=1):
        '''
        Return Calculator
        '''
        pass

# class Strategy:
#     def __init__(self)




