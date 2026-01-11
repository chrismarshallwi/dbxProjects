import streamlit as st
from ui.custom_css import apply_custom_styles
from ui.navigation import  init_navigation ,get_page_info
from ui.navigation_config import NavigationPage
from ui.sidebar import  init_sidebar,get_global_divider, get_global_region

apply_custom_styles()
st.logo("static/img/Screenshot 2025-12-29 155010.jpg", size="large")
st.set_page_config(
    page_title="Finance",
    # page_icon=":material/electric_bolt:",
    #page_icon="static/img/milwaukeetool.svg",
    layout="wide",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. \n\nThis is an *extremely* cool app!",
    },
)

page = init_navigation()

# Page shell elements
# Page shell elements
page_info: NavigationPage | None = get_page_info(page)
if page_info:
    init_sidebar(page_info)
    st.header(page_info.header, divider=get_global_divider())
    st.caption(page_info.caption)
    global_region = get_global_region()
    if global_region:
        with st.container(horizontal=True):
            st.text("Global filters:")
            st.badge(f"region [{global_region}]", icon=":material/filter_alt:")


# Run page
page.run()

