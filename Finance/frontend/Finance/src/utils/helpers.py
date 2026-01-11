from typing import Any, Callable
import pandas as pd
import streamlit as st

def init_session_state():
    """Initialize session state variables if not set yet."""
    defaults = {
        "expense_count": 1,
        "expenses": [],
        "income": [],
        "user_input": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def init_state_fn(key: str, value_fn: Callable[[], Any]) -> None:
    """Initialize session state key if not exists"""
    if key not in st.session_state:
        v = value_fn()
        st.session_state[key] = v

def init_state(key: str, value: Any) -> None:
    """Initialize session state key if not exists"""
    if key not in st.session_state:
        st.session_state[key] = value

def get_state(key: str, default: Any = None) -> Any:
    """Get value from session state with default"""
    return st.session_state.get(key, default)


def has_state(key: str) -> bool:
    """Check if key exists in session state"""
    return key in st.session_state


def set_state(key: str, value: Any) -> None:
    """Set value in session state"""
    st.session_state[key] = value


def clear_state_fn(key_fn: Callable[[str], bool]) -> None:
    """Remove keys from session state based on a function"""
    keys_to_remove = [key for key in st.session_state.keys() if key_fn(key)]
    for key in keys_to_remove:
        del st.session_state[key]


def clear_state(key: str) -> None:
    """Remove key from session state"""
    if key in st.session_state:
        del st.session_state[key]


def reset_session() -> None:
    """Clear all session state"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
