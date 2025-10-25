import pandas as pd 
import yfinance as yf

class Market():
    def __init__(self, ticker, start, end):
        self.ticker = ticker #what market are we creating?
        self.start = start #Start date 
        self.end = end #end date

    def get_price(self):
        data = yf.download(tickers=self.ticker, start=self.start, end=self.end)
        return data