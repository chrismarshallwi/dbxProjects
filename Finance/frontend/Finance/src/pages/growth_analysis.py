import streamlit as st
import pandas as pd
import datetime as dt
from utils import init_session_state

st.set_page_config(layout="wide") 

year = [2026, 2027]
init_session_state()

class Plan:
    def __init__(self):
        self.start_year = st.selectbox("Select Start Year", year)
        self.end_year = st.selectbox("Select End Year", year)
        self.title = st.title("Growth Analysis")
        self.monthly_free_cash_flow = st.write(f"Monthly Free Cash Flow: ${round(st.session_state['monthly_free_cash_flow'],0)}")
        self.line = st.markdown("<hr>", unsafe_allow_html=True)
    
    def create_and_save_inputs(self, session_name, comment, min_value, max_value, step, format):
        '''
        Create and save inputs used in the create_growth_analysis function
        '''
        value = st.number_input(
            comment,
            min_value=min_value,
            max_value=max_value,
            step=step,
            format=format,
            key=session_name)

    def create_growth_analysis(self, start_year:str, end_year:str, starting_balance:str, annual_return:str,percent_saved:str) -> pd.DataFrame:
        '''
        Create the Output Dataframe
        '''
        months = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-12-31", freq="MS")
        df = pd.DataFrame({"Month": months.strftime("%Y-%m")})
        
        #define some variables to start, parameterize the fields here accessed in session_state

        #start = st.session_state["starting_bal_retirement"]

        start = st.session_state[f"{starting_balance}"]
        annual_rate = st.session_state[f"{annual_return}"]
        monthly_rate = (1 + annual_rate) ** (1 / 12) - 1
        monthly_contrib = (
            st.session_state[f"{percent_saved}"] * st.session_state["monthly_free_cash_flow"]
        )

        #Projected ending balance
        df["Starting Balance"] = 0.0
        df["Monthly Contribution"] = monthly_contrib
        df["Projected Ending Balance"] = 0.0
        df.loc[0, "Starting Balance"] = start
        df.loc[0, "Projected Ending Balance"] = (start + monthly_contrib) * (1 + monthly_rate)
        
        df["Projected Return"] = df["Projected Ending Balance"] - (
            df["Starting Balance"] + df["Monthly Contribution"]
        )

        for i in range(1, len(df)):
            df.loc[i, "Starting Balance"] = df.loc[i - 1, "Projected Ending Balance"]
            df.loc[i, "Projected Ending Balance"] = (
                (df.loc[i, "Starting Balance"] + monthly_contrib) * (1 + monthly_rate)
            )

        df["Projected Return"] = df["Projected Ending Balance"] - (
            df["Starting Balance"] + df["Monthly Contribution"]
        )

        st.write(df[['Month','Projected Ending Balance']])


growth_analysis = Plan()

cols = st.columns(3)
comments = ['% Free Cash Flow', '% Annual Return']
fund_titles = ['Retirement Fund', 'Cash Fund','Investment Fund']
fund_session_names = [
    ['percent_saved_retirement','annual_return_retirement'],
    ['percent_saved_cash','annual_return_cash'],
    ['percent_saved_investment','annual_return_investment']
]

for col, title, session_names in zip(cols, fund_titles, fund_session_names):
    with col:
        st.subheader(title)
        for name, comment in zip(session_names, comments):
            growth_analysis.create_and_save_inputs(
                session_name=name,
                comment=comment,
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.2f"
            )

comments_start_bal = ['$ Starting Balance']

fund_session_names_start_bal = [
    ['starting_bal_retirement'],
    ['starting_bal_cash'],
    ['starting_bal_investment']
]

for col, session_names in zip(cols, fund_session_names_start_bal):
    with col:
        for name, comment in zip(session_names, comments_start_bal):
            growth_analysis.create_and_save_inputs(
                session_name=name,
                comment=comment,
                min_value=0.0,
                max_value=1000000.0,
                step=1.0,
                format="%.2f"
            )

starting_balances = ['starting_bal_retirement','starting_bal_cash']
returns = ['annual_return_retirement','annual_return_cash']
percent_saved = ['percent_saved_retirement','percent_saved_cash']

for starting_balance,ret,saved in zip(starting_balances,returns,percent_saved):
    growth_analysis.create_growth_analysis(
        start_year=growth_analysis.start_year, 
        end_year=growth_analysis.end_year, 
        starting_balance=starting_balance,
        annual_return =ret,
        percent_saved=saved
        )

