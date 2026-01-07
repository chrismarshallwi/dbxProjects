import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.service import jobs
from databricks.sdk.service.iam import User


@st.cache_resource(ttl=600)
def workspace() -> WorkspaceClient:
    """
    Get a cached Databricks WorkspaceClient instance.
    Returns:
        WorkspaceClient: The Databricks workspace client.
    """
    return WorkspaceClient()


def get_workspace_user() -> User:
    """
    Get the current user from the Databricks workspace.
    Returns:
        User: The current Databricks user.
    """
    return workspace().current_user.me()


class DatabricksJob:
    def __init__(self, job_id: int) -> None:
        self.ws = WorkspaceClient()
        self.job_id = job_id
        self.run_id: int = self._start_job()
        self.job_run: jobs.Run = self.ws.jobs.get_run(run_id=self.run_id)
        self.run_page_url = self.job_run.run_page_url

    def _start_job(self) -> int:
        return self.ws.jobs.run_now(self.job_id).response.run_id

    def check_status(self):
        return self.ws.jobs.get_run(run_id=self.run_id).state.life_cycle_state

    def has_finished(self, status=None) -> bool:
        if not status:
            status = self.check_status()
        return status in [
            jobs.RunLifeCycleState.TERMINATED,
            jobs.RunLifeCycleState.SKIPPED,
            jobs.RunLifeCycleState.INTERNAL_ERROR,
        ]

    def format_status_message(self, status=None) -> str:
        if not status:
            status = self.check_status()

        match status:
            case jobs.RunLifeCycleState.QUEUED:
                return f"Job :gray-badge[{status.name}]"
            case jobs.RunLifeCycleState.PENDING:
                return f"Job :blue-badge[{status.name}]"
            case jobs.RunLifeCycleState.RUNNING:
                return f"Job :green-badge[{status.name}]"
            case jobs.RunLifeCycleState.TERMINATED:
                return f"Job :green-badge[{status.name}]"
            case jobs.RunLifeCycleState.SKIPPED:
                return f"Job :gray-badge[{status.name}]"
            case jobs.RunLifeCycleState.INTERNAL_ERROR:
                return f"Job :red-badge[{status.name}]"
            case _:
                return f"Job :blue-badge[{status.name if status else 'UNKOWN'}]"

    def __repr__(self) -> str:
        return f"Job(id={self.job_id}, run_id={self.run_id})"