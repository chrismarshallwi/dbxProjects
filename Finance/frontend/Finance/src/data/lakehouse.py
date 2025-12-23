import pandas as pd
import streamlit as st
from databricks.connect import DatabricksSession
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from services.config import settings

def validate_spark_session(spark) -> bool:
    """
    Validate that the Spark session is still active by performing a simple operation.
        Returns True if the session is valid, False otherwise.
    """
    try:
        spark.range(1).count()
        return True
    except Exception:
        return False


@st.cache_resource(show_spinner=True, show_time=True, validate=validate_spark_session)
def spark():
    """
    Create and return a Databricks Serverless Spark session.
    Returns:
        DatabricksSession: A Databricks Serverless Spark session.
    """
    return DatabricksSession.builder.serverless(True).getOrCreate()


def read_table(catalog_name: str, schema_name: str, table_name: str) -> DataFrame:
    """
    Read a table from the specified catalog, schema, and table name.
    Args:
        catalog_name (str): The name of the catalog.
        schema_name (str): The name of the schema.
        table_name (str): The name of the table.
    Returns:
        DataFrame: A Spark DataFrame containing the table data.
    """
    return spark().table(f"{catalog_name}.{schema_name}.{table_name}")



