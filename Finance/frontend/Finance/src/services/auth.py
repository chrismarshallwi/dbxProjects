import streamlit as st

from data import lakehouse
from services import databricks
from utils.helpers import init_state_fn, get_state


class UserInfo:
    """
    Represents information about a user.
    Attributes:
        id (str): The unique identifier of the user.
        display_name (str): The display name of the user.
        roles (list[str]): A list of roles assigned to the user.
        metadata (dict): Additional metadata associated with the user.
    """

    def __init__(self, id: str, display_name: str, roles: list[str] = [], metadata: dict = {}):
        self.id = id
        self.display_name = display_name
        self.roles = roles
        self.metadata = metadata

    def get_metadata(self, key: str, default=None):
        return self.metadata.get(key, default)


def _get_current_user() -> UserInfo:
    user_id = st.context.headers.get("X-Forwarded-Email", None)
    if user_id:
        user_entitlements = lakehouse.get_user_entitlements(user_id)
        return UserInfo(user_id, user_id, user_entitlements.get("roles", []), user_entitlements.get("metadata", {}))

    workspace_user = databricks.get_workspace_user()
    user_entitlements = lakehouse.get_user_entitlements(workspace_user.user_name)
    return UserInfo(
        workspace_user.user_name,
        workspace_user.display_name,
        user_entitlements.get("roles", []),
        user_entitlements.get("metadata", {}),
    )


def get_current_user() -> UserInfo:
    """
    Retrieves the current user's information, including their roles and metadata.
    Returns:
        UserInfo: An object containing the current user's information.
    """
    init_state_fn("user_info", _get_current_user)
    return get_state("user_info")
