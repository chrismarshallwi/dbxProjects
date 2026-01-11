from typing import Any
import streamlit as st
from services.auth import UserInfo, get_current_user
from ui.navigation_config import NavigationPage, navigation_config

user: UserInfo = get_current_user()

from pathlib import Path 

APP_ROOT = Path(__file__).resolve().parents[1]

def init_navigation():
    nav_sections = {}
    for section in navigation_config.sections:
        pages = []
        for page in section.pages:

            page_path = APP_ROOT / page.page

            #check if user has one of the required roles for this section
            if page.roles and not set(page.roles).intersection(user.roles):
                continue

            st_page = st.Page(
                str(page_path),
                title=page.title,
                icon=page.icon
            )
            st_page.page_config = page
            pages.append(st_page)
        nav_sections[section.name] = pages
    return st.navigation(nav_sections)


def get_page_info(page: Any) -> NavigationPage | None:
    return page.page_config if page else None
