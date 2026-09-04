import streamlit as st
import pandas as pd

from pages.create_session import CreateSession
from ui.session_manager import (
    get_active_session,
    get_sessions,
    update_session,
    delete_session,
)


# =========================================================
# Active Session
# =========================================================

active_session = get_active_session()

if active_session:

    st.info(
        active_session['session_name']
    )

else:

    st.warning("No trading session selected")


# =========================================================
# Tabs
# =========================================================

tabs = st.tabs([
    "📈 Create New Session",
    "🛠️ Session Manager",
])


# =========================================================
# Create New Session
# =========================================================

with tabs[0]:

    CreateSession()


# =========================================================
# Session Manager
# =========================================================

with tabs[1]:

    st.subheader("Open Sessions")
    sessions = get_sessions()

    if not sessions:
        st.info("No sessions have been created yet.")

    else:

        # -------------------------------------------------
        # Convert sessions to DataFrame
        # -------------------------------------------------

        for session_id, session in sessions.items():

            if session['strategy'] == 'Dollar Cost Average':

                with st.expander(
                    f"{session['session_name']}-{session['strategy']}"
                ):

                    allocation_df = pd.DataFrame(session['allocations'])

                    # Add session-level information
                    allocation_df["Session Name"] = session["session_name"]
                    allocation_df["Asset Type"] = session["asset_type"]
                    allocation_df["Strategy"] = session["strategy"]
                    allocation_df["Total Investment"] = session["investment_amount"]
                    allocation_df["Created"] = session["created_at"]
                    allocation_df['Frequency'] = session["frequency"]
                    allocation_df['Day of Week'] = session["day_of_week"]

                    allocation_df = allocation_df[
                        [
                            "Session Name",
                            "Asset Type",
                            "Strategy",
                            "Total Investment",
                            "Stock",
                            "Allocation %",
                            "Investment Amount",
                            "Frequency",
                            "Day of Week",
                            "Created"
                        ]
                    ]

                    st.dataframe(
                        allocation_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Total Investment": st.column_config.NumberColumn(
                                format="$%d"
                            ),
                            "Allocation %": st.column_config.NumberColumn(
                                format="%d%%"
                            ),
                            "Investment Amount": st.column_config.NumberColumn(
                                format="$%d"
                            ),
                            "Created": st.column_config.DatetimeColumn(
                                format="YYYY-MM-DD HH:mm"
                            )
                        }
                    )

                    update_col, delete_col = st.columns(2)

                    with update_col:
                        if st.button("Update Details", key=f"update_{session_id}"):
                            st.session_state["editing_session_id"] = session_id
                            from pages.create_session import create_session_dialog
                            create_session_dialog(edit_session_id=session_id)

                    with delete_col:
                        if st.button("Delete Session", key=f"delete_{session_id}", type="secondary"):
                            delete_session(session_id)
                            st.rerun()

            elif session['strategy'] == 'Mean Reversion':

                with st.expander(
                    f"{session['session_name']}-{session['strategy']}"
                ):

                    allocation_df = pd.DataFrame(session['allocations'])

                    allocation_df["Session Name"] = session["session_name"]
                    allocation_df["Asset Type"] = session["asset_type"]
                    allocation_df["Strategy"] = session["strategy"]
                    allocation_df["Total Investment"] = session["investment_amount"]
                    allocation_df["Created"] = session["created_at"]

                    if isinstance(session.get("moving_average"), dict):
                        allocation_df["Moving Average"] = allocation_df["Stock"].map(session["moving_average"])
                        allocation_df["Threshold %"] = allocation_df["Stock"].map(session["threshold"])
                    else:
                        allocation_df["Moving Average"] = session.get("moving_average")
                        allocation_df["Threshold %"] = session.get("threshold")

                    allocation_df = allocation_df[
                        [
                            "Session Name",
                            "Asset Type",
                            "Strategy",
                            "Total Investment",
                            "Stock",
                            "Allocation %",
                            "Investment Amount",
                            "Moving Average",
                            "Threshold %",
                            "Created"
                        ]
                    ]

                    st.dataframe(
                        allocation_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Total Investment": st.column_config.NumberColumn(
                                format="$%d"
                            ),
                            "Allocation %": st.column_config.NumberColumn(
                                format="%d%%"
                            ),
                            "Investment Amount": st.column_config.NumberColumn(
                                format="$%d"
                            ),
                            "Created": st.column_config.DatetimeColumn(
                                format="YYYY-MM-DD HH:mm"
                            )
                        }
                    )

                    update_col, delete_col = st.columns(2)

                    with update_col:
                        if st.button("Update Details", key=f"update_{session_id}"):
                            st.session_state["editing_session_id"] = session_id
                            from pages.create_session import create_session_dialog
                            create_session_dialog(edit_session_id=session_id)

                    with delete_col:
                        if st.button("Delete Session", key=f"delete_{session_id}", type="secondary"):
                            delete_session(session_id)
                            st.rerun()
