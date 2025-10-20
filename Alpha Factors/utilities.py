import pandas as pd 
import yfinance as yf

class Market():
    def __init__(self, tickers, start, end):
        self.tickers = tickers #what market are we creating?
        self.start = start #Start date 
        self.end = end #end date

    def get_price(self):
        stock_data_df = []
        for i in self.tickers:
            data = yf.download(i, start=self.start, end=self.end)
            data['Symbol'] = i
            data['first_column'] = data.pop('Symbol')
            data.insert(0, 'Symbol', data['first_column'])
            stock_data_df.append(data)
        stock_data_df = pd.concat(stock_data_df)
        return stock_data_df.iloc[:,:7] 