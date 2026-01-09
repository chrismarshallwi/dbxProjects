import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.helpers import init_session_state

init_session_state()

year = 2025

st.write("## Income")

paycheck_frequency_options = ["Bi-Weekly", "Monthly"]

# Ensure session_state['income'] exists and has 2 slots
if "income" not in st.session_state:
    st.session_state.income = []
while len(st.session_state.income) < 2:
    st.session_state.income.append((0, "Bi-Weekly"))

col2, col3 = st.columns(2)

with col2:
    # first paycheck
    first_freq = st.session_state.income[0][1]
    first_index = paycheck_frequency_options.index(first_freq) if first_freq in paycheck_frequency_options else 0

    first_paycheck_frequency = st.selectbox(
        "Choose First Paycheck Frequency",
        paycheck_frequency_options,
        key="first_paycheck_freq",
        index=first_index
    )
    first_paycheck_amount = st.number_input(
        "First Paycheck Amount",
        min_value=0,
        key="first_paycheck_amt",
        value=st.session_state.income[0][0]
    )

with col3:
    # second paycheck
    second_freq = st.session_state.income[1][1]
    second_index = paycheck_frequency_options.index(second_freq) if second_freq in paycheck_frequency_options else 0

    second_paycheck_frequency = st.selectbox(
        "Choose Second Paycheck Frequency",
        paycheck_frequency_options,
        key="second_paycheck_freq",
        index=second_index
    )
    second_paycheck_amount = st.number_input(
        "Second Paycheck Amount",
        min_value=0,
        key="second_paycheck_amt",
        value=st.session_state.income[1][0]
    )

# store current input back in session_state
st.session_state.income[0] = (first_paycheck_amount, first_paycheck_frequency)
st.session_state.income[1] = (second_paycheck_amount, second_paycheck_frequency)

# calculate annualized income
frequency_map = {"Bi-Weekly": 26, "Monthly": 12}

first_annual_net_income = first_paycheck_amount * frequency_map[first_paycheck_frequency]
second_annual_net_income = second_paycheck_amount * frequency_map[second_paycheck_frequency]

total_annual_net_income = first_annual_net_income + second_annual_net_income

st.write("#### Total Annual Net Income", total_annual_net_income)
st.success(f"💰 Total Annual Income: ${total_annual_net_income:,.2f}")


st.markdown("<hr>", unsafe_allow_html=True)


st.write("### Expenses")

if st.button("+ Add Expense"):
    st.session_state.expense_count += 1

expense_type = ['Housing','Car Payment','Wifi','Phone Bills','Insurance']
expense_frequency_options = ['Bi-Weekly','Monthly','Annual']
frequency_map = {"Bi-Weekly": 26, "Monthly": 12, "Annual": 1}

# ensure expenses list has enough slots
if len(st.session_state.expenses) < st.session_state.expense_count:
    st.session_state.expenses.extend([("", 0, "Monthly", 0)] * 
                                     (st.session_state.expense_count - len(st.session_state.expenses)))

for i in range(st.session_state.expense_count):
    col1, col2, col3 = st.columns(3)

    with col1:
        exp = st.selectbox(f"Expense {i+1}", expense_type,
                           key=f"expense_type_{i}",
                           index=expense_type.index(st.session_state.expenses[i][0]) if st.session_state.expenses[i][0] in expense_type else 0)
    with col2:
        freq = st.selectbox("Frequency", expense_frequency_options,
                            key=f"expense_freq_{i}",
                            index=expense_frequency_options.index(st.session_state.expenses[i][2]) if st.session_state.expenses[i][2] in expense_frequency_options else 1)
    with col3:
        amt = st.number_input(f"Amount {i+1}", min_value=0,
                              key=f"expense_amount_{i}",
                              value=st.session_state.expenses[i][1])

    annual_amt = amt * frequency_map[freq]
    st.session_state.expenses[i] = (exp, amt, freq, annual_amt)

total = sum([e[3] for e in st.session_state.expenses])
st.success(f"💰 Total Annual Expenses: ${total:,.2f}")



# -------------------------------
# GET INCOME
# -------------------------------
income_list = st.session_state.get("income", [(0, "Bi-Weekly"), (0, "Bi-Weekly")])

monthly_incomes = []
for paycheck_amount, freq in income_list:
    try:
        amt = float(paycheck_amount)
    except:
        amt = 0

    if freq == "Monthly":
        monthly_incomes.append(amt)
    elif freq == "Bi-Weekly":
        total_year_income = amt * 26
        monthly_incomes.append(total_year_income / 12)
    elif freq == "Weekly":
        total_year_income = amt * 52
        monthly_incomes.append(total_year_income / 12)
    else:
        monthly_incomes.append(0)

total_monthly_income = sum(monthly_incomes)

# -------------------------------
# GET EXPENSES
# -------------------------------
expenses_list = st.session_state.get("expenses", [])

total_annual_expenses = sum(
    x[3] if isinstance(x, (list, tuple)) and len(x) > 3 else 0
    for x in expenses_list
)
monthly_expense = total_annual_expenses / 12

months = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq="MS")
df = pd.DataFrame({"Month": months.strftime("%Y-%m")})

df["Total Income"] = total_monthly_income
df["Total Expense"] = monthly_expense
df["Free Cash Flow"] = df["Total Income"] - df["Total Expense"]

st.session_state['monthly_free_cash_flow'] = np.mean(df['Free Cash Flow']) #convert to a single value
st.session_state['annual_free_cash_flow'] = np.mean(df['Free Cash Flow']*12) #convert to sum all values


st.markdown("<hr>", unsafe_allow_html=True)
st.write("### Summary Metrics")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric("💰 Annual Income", f"${sum(monthly_incomes)*12:,.2f}")
    st.metric("💸 Annual Expenses", f"${total_annual_expenses:,.2f}")
    st.metric("📊 Annual Free Cash Flow", f"${sum(monthly_incomes)*12 - total_annual_expenses:,.2f}")

with col2:
    st.metric("💰 Monthly Income", f"${sum(monthly_incomes):,.2f}")
    st.metric("💸 Monthly Expenses", f"${total_annual_expenses/12:,.2f}")
    st.metric("📊 Monthly Free Cash Flow", f"${sum(monthly_incomes) - total_annual_expenses/12:,.2f}")
    
with col3:

    data = {
        'Category': ['Total Expenses', 'Total Free Cash Flow'],
        'Allocation': [total_annual_expenses,sum(monthly_incomes)*12 - total_annual_expenses]
    }

    fig = px.pie(
        data, 
        names='Category', 
        values='Allocation', 
        title='Expense Analysis'
        )

    st.plotly_chart(fig,use_container_width=True)
