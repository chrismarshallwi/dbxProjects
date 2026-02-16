# Databricks notebook source
# MAGIC %md
# MAGIC # Data Quality Check
# MAGIC
# MAGIC This notebook runs a set of data quality checks usign DQX.
# MAGIC
# MAGIC ## Required Parameters
# MAGIC
# MAGIC - `config_path` (String): Path to the configuration file or directory.
# MAGIC - `fail_on_error` (String): Set to control error handling behavior (e.g., "true" or "false").
# MAGIC
# MAGIC ## Required Libraries
# MAGIC
# MAGIC Ensure the following libraries are installed in your Databricks environment:
# MAGIC
# MAGIC - DQX: `databricks-labs-dqx`
# MAGIC - Yaml: `pyyaml`
# MAGIC
# MAGIC ## Usage
# MAGIC
# MAGIC 1. Create the configuration files (`.yml`) inside a folder:
# MAGIC    ```yaml
# MAGIC    # file: dev_operations.demand.dim_demand_date.yml
# MAGIC    # pattern: catalog.schema.table.yml
# MAGIC     - criticality: error
# MAGIC       check:
# MAGIC         function: is_unique
# MAGIC         arguments:
# MAGIC           columns:
# MAGIC             - date_key
# MAGIC    ```
# MAGIC 1. Set the required parameters before running the notebook:
# MAGIC    ```yaml
# MAGIC         - task_key: refresh_procurement_audits_pbi
# MAGIC           depends_on:
# MAGIC             - task_key: fact_procurement_audits_tracking
# MAGIC           notebook_task:
# MAGIC             notebook_path: ../../../shared/notebooks/pbi_refresh.py
# MAGIC             base_parameters:
# MAGIC               config_path: ${workspace.file_path}/${bundle.name}/src/data_product_xyz/dq/
# MAGIC               fail_on_error: true
# MAGIC           environment_key: odpenv
# MAGIC    ```
# MAGIC 1. Verify that all necessary libraries are available in the serverless environment:
# MAGIC    ```yaml
# MAGIC       environments:
# MAGIC         - environment_key: odpenv
# MAGIC           spec:
# MAGIC             environment_version: "4"
# MAGIC             dependencies:
# MAGIC               - databricks-labs-dqx
# MAGIC               - pyyaml
# MAGIC    ```
# MAGIC

# COMMAND ----------

import os
import yaml
from pathlib import Path
from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from databricks.sdk import WorkspaceClient
from databricks.labs.dqx.engine import DQEngine
from databricks.labs.dqx.metrics_observer import DQMetricsObserver

# COMMAND ----------

dbutils.widgets.text("config_path", "", "Config path")
config_path = dbutils.widgets.get("config_path")

dbutils.widgets.text("dq_catalog", "", "Data Quality Catalog Name")
dq_catalog_name = dbutils.widgets.get("dq_catalog")

config_path = Path(config_path).resolve()
if not config_path.exists():
    raise RuntimeError(f"Configuration directory [{config_path}] not found.")
print(f"Configuration directory: {config_path}")

dbutils.widgets.text("fail_on_error", "", "Fail the notebook execution on check error")
fail_on_error: bool = dbutils.widgets.get("fail_on_error") == "true"
print(f"Fail on error: {fail_on_error}")

# COMMAND ----------

ws = WorkspaceClient()
dqe = DQEngine(ws, observer=DQMetricsObserver(name="sca"))


def apply_checks(file: Path, catalog:str) -> DQMetricsObserver:
    full_table_name = catalog+'.'+file.stem
    input_df = spark.read.table(full_table_name)
    with file.open("r", encoding="utf-8") as f:
        checks = yaml.safe_load(f)
    result_df, result_obs = dqe.apply_checks_by_metadata(input_df, checks)
    result_df = (
        result_df.select(F.explode(F.col("_errors")).alias("json_data"))
        .select("json_data.*")
        .groupBy("name", "columns", "filter", "function", "run_time", "user_metadata")
        .count()
        .withColumnRenamed("count", "failed_check_count")
        .withColumns(
            {
                "full_table_name": F.lit(full_table_name),
            }
        )
    )
    result_df.count()  # required to get the observation
    result = result_obs.get
    return {
        "table": full_table_name,
        "has_error": result.get("error_row_count", 0) > 0,
        "result_df": result_df,
        **result,
    }


dq_results = [apply_checks(file,catalog=dq_catalog_name) for file in config_path.glob("*.yml")]
for result in [r for r in dq_results if r["has_error"]]:
    displayHTML(f'<h4>Errors in table <span style="color:blue">{result["table"]}</span></h4>')
    display(result["result_df"])

# COMMAND ----------

if any(r["has_error"] for r in dq_results):
    # add the list of files to the task values
    dbutils.jobs.taskValues.set(key="dq_result", value="failed")

    if fail_on_error:
        raise RuntimeError("One or more data quality checks failed.")
else:
    dbutils.jobs.taskValues.set(key="dq_result", value="passed")
