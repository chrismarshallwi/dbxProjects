import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styling to the app"""
    st.markdown(
        """
    <style>
    .stAppHeader {
        background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
        visibility: visible;  /* Ensure the header is visible */
    }

    /* Main container styling */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )


# Other (unused) CSS styles can be added
# /* Hide Streamlit branding */
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}

st.markdown(
    """
    <style>
    </style>
    """,
    unsafe_allow_html=True,
)
