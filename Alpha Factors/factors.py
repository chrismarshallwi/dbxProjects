

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

factors = ['Relative Strength Index (RSI)']

st.selectbox('Alpha Factor',factors)

