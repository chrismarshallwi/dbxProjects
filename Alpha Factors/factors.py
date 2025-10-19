
import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(layout="wide")

factors = ['Relative Strength Index (RSI)','Price Momentum']

ticker = ['AAPL','MSFT']

class Factor():
    def __init__(self,factor,ticker,start_date,end_date):
        self.factor = factor
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
    
    def calc_rsi(self):
        df = yf.download(self.ticker,start=self.start_date,end=self.end_date)

    def calc_price_momentum(self):
        pass
        
col1, col2, col3, col4 = st.columns(4)   

with col1:
    ticker = st.selectbox('Ticker',ticker)
    if "ticker" not in st.session_state:
        st.session_state.ticker = ticker

with col2:
    alpha_factor = st.selectbox('Alpha Factor',factors)
    if "alpha_factor" not in st.session_state:
        st.session_state.alpha_factor = alpha_factor

with col3: 
    start_date = st.date_input('Start Date')
    if "start_date" not in st.session_state:
        st.session_state.start_date = start_date

with col4:
    end_date = st.date_input('End Date')
    if "end_date" not in st.session_state:
        st.session_state.end_date = end_date

observation = Factor(factor = st.session_state.alpha_factor,ticker = st.session_state.ticker,start_date = st.session_state.start_date,end_date = st.session_state.end_date)

observation.calc_rsi()


