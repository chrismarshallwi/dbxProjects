import streamlit as st
from services.auth import UserInfo, get_current_user
from utils.helpers import get_state
from data.lakehouse import sql_query, get_tickers
from ui.navigation_config import NavigationPage
# from ui.custom_css import apply_custom_styles
from ui.session_manager import get_sessions

# apply_custom_styles()

GLOBAL_REGION = "global_region"
GLOBAL_DIVIDER = "global_divider"
user: UserInfo = get_current_user()
user_default_region = user.get_metadata("default_region")


@st.dialog("Help", on_dismiss="ignore")
def help(page):
    if page:
        st.markdown(open(page).read())


def init_sidebar(page_info: NavigationPage):
    # Global parameters in sidebar
    with st.sidebar:
        # asset_type = st.pills("Asset Type", options=["Stocks", "Index", "ETF"])

        # if asset_type == "Stocks":
        #     stocks = """select distinct dc.company_stock_symbol from operations.finance.fact_price_daily fa
        #                 left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
        #                 where fa.asset_type = 'Stock'
        #                 order by company_stock_symbol asc"""

        #     stocks_list = sql_query(stocks).iloc[:,0].tolist()
        #     st.multiselect(label='Stock List', options = stocks_list, placeholder = 'Select a stock...') 
        
        # if asset_type == "Index":
        #     index =  """select distinct dc.company_stock_symbol from operations.finance.fact_price_daily fa
        #                 left join operations.finance.dim_company dc on dc.company_bigint_key = fa.company_bigint_key
        #                 where fa.asset_type = 'Index'
        #                 order by company_stock_symbol asc"""
            
        #     index_list = sql_query(index).iloc[:,0].tolist()
        #     st.multiselect(label='Index List', options = index_list, placeholder = 'Select a index...')

        if page_info and page_info.help_page:
            st.button(
                "Help",
                key="help",
                icon=":material/help:",
                type="tertiary",
                help="Instructions",
                on_click=help,
                args=[page_info.help_page],
            )
        
        #st.divider()
        st.subheader("Sessions")
        
        sessions = get_sessions()

        if not sessions:
            st.caption("No sessions created")
        else:
            for session_id, session in sessions.items():
                if st.button(session['session_name'], key=f"session_{session_id}",icon=":material/finance_mode:",use_container_width=True):
                    st.session_state.active_session_id = session_id 
                    st.rerun()
        
        


def get_global_region() -> str | None:
    return get_state(GLOBAL_REGION, None)


def get_global_divider() -> bool:
    return get_state(GLOBAL_DIVIDER, False)
