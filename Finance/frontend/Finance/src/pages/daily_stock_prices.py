import streamlit as st
from data.lakehouse import sql_query, get_tickers
from pages.search_daily_stock_prices import SearchDailyStockPrice

SearchDailyStockPrice()