import streamlit as st
from datetime import datetime
import pandas as pd


def _normalize_mean_reversion_settings(allocation_df: pd.DataFrame | None, moving_average=None, threshold=None):
    """Return scalar or per-stock mean reversion settings based on the allocation table."""

    if allocation_df is None or allocation_df.empty:
        return moving_average, threshold

    if "Moving Average" in allocation_df.columns and "Threshold %" in allocation_df.columns:
        ma_values = pd.to_numeric(allocation_df["Moving Average"], errors="coerce")
        threshold_values = allocation_df["Threshold %"]

        if ma_values.nunique() == 1 and threshold_values.nunique() == 1:
            return int(ma_values.iloc[0]), threshold_values.iloc[0]

        return (
            {row.Stock: int(row["Moving Average"]) for _, row in allocation_df.iterrows()},
            {row.Stock: row["Threshold %"] for _, row in allocation_df.iterrows()},
        )

    return moving_average, threshold


def initialize_sessions():
    """Initialize trading session storage."""

    if "trading_sessions" not in st.session_state:
        st.session_state.trading_sessions = {}

    if "active_session_id" not in st.session_state:
        st.session_state.active_session_id = None


def create_session(
    session_name: str,
    asset_type: str,
    strategy: str,
    investment_amount: int,
    frequency: str = None,
    day_of_week: str = None,
    moving_average: int = None,
    threshold: int = None,
    allocation_df: pd.DataFrame = None
):
    """Create a new trading session."""

    if strategy == 'Dollar Cost Average':

        session_id = f"session_{len(st.session_state.trading_sessions) + 1}"

        session = {
            "session_id": session_id,
            "session_name": session_name,
            "asset_type": asset_type,
            "strategy": strategy,
            "investment_amount": investment_amount,
            "allocations": allocation_df,
            "frequency": frequency,
            "day_of_week": day_of_week,
            "created_at": datetime.now(),
        }

        st.session_state.trading_sessions[session_id] = session
        st.session_state.active_session_id = session_id

        return session

    elif strategy == 'Mean Reversion':
        session_id = f"session_{len(st.session_state.trading_sessions) + 1}"
        normalized_moving_average, normalized_threshold = _normalize_mean_reversion_settings(
            allocation_df,
            moving_average,
            threshold
        )

        session = {
            "session_id": session_id,
            "session_name": session_name,
            "asset_type": asset_type,
            "strategy": strategy,
            "investment_amount": investment_amount,
            "allocations": allocation_df,
            "moving_average": normalized_moving_average,
            "threshold": normalized_threshold,
            "created_at": datetime.now(),
        }

        st.session_state.trading_sessions[session_id] = session
        st.session_state.active_session_id = session_id

        return session


def get_sessions():
    """Return all trading sessions."""
    return st.session_state.trading_sessions


def get_session(session_id: str):
    """Return a single trading session by id."""
    if session_id is None:
        return None
    return st.session_state.trading_sessions.get(session_id)


def get_active_session():
    """Return the currently active trading session."""

    session_id = st.session_state.get("active_session_id")

    if session_id is None:
        return None

    return st.session_state.trading_sessions.get(session_id)


def update_session(
    session_id: str,
    session_name: str,
    asset_type: str,
    strategy: str,
    investment_amount: int,
    frequency: str = None,
    day_of_week: str = None,
    moving_average=None,
    threshold=None,
    allocation_df: pd.DataFrame = None,
):
    """Update an existing trading session."""

    if session_id not in st.session_state.trading_sessions:
        return None

    session = st.session_state.trading_sessions[session_id]

    session["session_name"] = session_name
    session["asset_type"] = asset_type
    session["strategy"] = strategy
    session["investment_amount"] = investment_amount
    session["frequency"] = frequency
    session["day_of_week"] = day_of_week
    session["moving_average"] = moving_average
    session["threshold"] = threshold
    session["allocations"] = allocation_df
    session["updated_at"] = datetime.now()

    return session


def delete_session(session_id: str):
    """Delete a trading session."""

    if session_id not in st.session_state.trading_sessions:
        return

    del st.session_state.trading_sessions[session_id]

    # If the deleted session was active, clear the active session
    if st.session_state.get("active_session_id") == session_id:
        st.session_state.active_session_id = None