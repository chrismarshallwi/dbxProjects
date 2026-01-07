import streamlit as st
from services.auth import UserInfo, get_current_user
from utils.helpers import get_state

from ui.navigation_config import NavigationPage

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
        st.pills("Region", key=GLOBAL_REGION, options=["NE", "SW", "NW", "SE"], default=user_default_region)
        st.toggle("Use header divider", key=GLOBAL_DIVIDER)
        st.divider()
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


def get_global_region() -> str | None:
    return get_state(GLOBAL_REGION, None)


def get_global_divider() -> bool:
    return get_state(GLOBAL_DIVIDER, False)
