import pandas as pd 
import yfinance as yf

class Market():
    def __init__(self, ticker, start, end):
        self.tickers = tickers #what market are we creating?
        self.start = start #Start date 
        self.end = end #end date

    # def get_price(self):
    #     data = yf.download(tickers=self.ticker, start=self.start, end=self.end)
    #     return data
    
    def get_price(self):
        data = yf.download(self.tickers, start=self.start, end=self.end, group_by='ticker')

        all_data = []
        for ticker in self.tickers:
            df = data[ticker].copy()
            df.insert(0, 'Symbol', ticker)
            all_data.append(df)

        return pd.concat(all_data)
