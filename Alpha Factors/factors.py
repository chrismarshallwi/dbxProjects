import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(layout="wide")

factors = ['Relative Strength Index (RSI)','Price Momentum']

ticker = ['AAPL','MSFT']


        
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

st.write(st.session_state.ticker, st.session_state.alpha_factor, st.session_state.start_date, st.session_state.end_date)


