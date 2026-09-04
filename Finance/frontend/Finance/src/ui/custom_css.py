import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styling to the app"""

    st.markdown(
        """
        
        <style>


        /* =========================================================
           Global Font
           ========================================================= */

        .stApp {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Main Text
           ========================================================= */

        .stApp p,
        .stApp label,
        .stApp input,
        .stApp textarea {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Headers
           ========================================================= */

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp h5,
        .stApp h6 {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Buttons
           ========================================================= */

        .stApp button {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Select Boxes / Multi-selects
           ========================================================= */

        [data-baseweb="select"] {
            font-family: "Consolas", monospace;
        }

        [data-baseweb="select"] input {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Tabs
           ========================================================= */

        button[data-baseweb="tab"] {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Sidebar
           ========================================================= */

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] button {
            font-family: "Consolas", monospace;
        }


        /* =========================================================
           Main Container
           ========================================================= */

        .block-container {
            padding-top: 0rem;
            padding-bottom: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }


        /* =========================================================
           Streamlit Header
           ========================================================= */

        .stAppHeader {
            background-color: rgba(255, 255, 255, 0.0);
            visibility: visible;
        }


        </style>
        """,
        unsafe_allow_html=True,
    )


