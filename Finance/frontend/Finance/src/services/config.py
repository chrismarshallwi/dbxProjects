import os

from databricks.sdk.core import Config

cfg = Config()


class Settings:
    """
    Application settings.
    """

    APP_NAME: str = os.getenv("APP_NAME") or "app_streamlit"
    OPS_CATALOG: str = os.getenv("OPS_CATALOG") or "NOCATALOG"
    SERVER_HOSTNAME: str = cfg.host


settings = Settings()