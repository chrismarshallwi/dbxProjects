import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(layout="wide")

factors = ['Relative Strength Index (RSI)','Price Momentum']

ticker = ['AAPL','MSFT']

col1, col2, col3, col4 = st.columns(4)   

with col1:
    st.session_state.ticker = st.selectbox('Ticker',ticker)

with col2:
    st.session_state.alpha_factor = st.selectbox('Alpha Factor',factors)

with col3: 
    st.session_state.start_date = st.date_input('Start Date')

with col4:
    st.session_state.end_date = st.date_input('End Date')

st.write(st.session_state.ticker, 
         st.session_state.alpha_factor, 
         st.session_state.start_date,
            st.session_state.end_date)

###NEXT STEPS: Print some stock market data for which ever stock is selected in the st.session_state.ticker variable

def get_price(ticker,start_date,end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    st.dataframe(data)

def calculate_rsi():
    pass

def calculate_price_momentum():
    pass

if st.session_state.alpha_factor == 'Relative Strength Index (RSI)':
    calculate_rsi()
elif st.session_state.alpha_factor == 'Price Momentum':
    calculate_price_momentum()
else:
    pass

get_price(ticker=st.session_state.ticker,start= st.session_state.start_date, end=st.session_state.end_date)
