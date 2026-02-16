import json
import re
from pathlib import Path
from databricks import sql
from dataclasses import dataclass
from typing import List, Dict

from dbruntime.databricks_repl_context import get_context


@dataclass
class FileExecutionOrder:
    rejected: List[str]
    once: List[str]
    replay: List[str]


class FileSorter:
    """Abstract base class for file sorters."""

    rejected_hint: str = "Check the file naming conventions."

    def sort_files(self, file_path: Path, params: Dict) -> FileExecutionOrder:
        raise NotImplementedError("Subclasses must implement this method")


class AlphaPatternFileSorter(FileSorter):
    """File sorter that uses a regex pattern to categorize files."""

    def __init__(self):
        """Initialize the AlphaPatternFileSorter with a regex pattern."""
        self.pattern = r"^(?P<type>once|replay)_(?P<order>\d{2,4})_(?P<description>.+)\.sql$"
        self.rejected_hint = "[once|replay]_[00|000|0000]_file_name.sql"

    def sort_files(self, file_path: Path, params: Dict) -> FileExecutionOrder:
        """Sort files into rejected, once, and replay categories based on the regex pattern."""
        file_names: List[str] = [f.name for f in file_path.iterdir() if f.is_file()]
        rejected_files: List[str] = []
        once_files: List[str] = []
        replay_files: List[str] = []
        for filename in file_names:
            match = re.match(self.pattern, filename)
            if match:
                if match.group("type") == "once":
                    once_files.append(filename)
                if match.group("type") == "replay":
                    replay_files.append(filename)
            else:
                rejected_files.append(filename)
        rejected_files = sorted(rejected_files)
        once_files = sorted(once_files)
        replay_files = sorted(replay_files)
        return FileExecutionOrder(rejected=rejected_files, once=once_files, replay=replay_files)


class BetaFileSorter(FileSorter):
    def __init__(self):
        self.rejected_hint = "TBD"

    def sort_files(self, file_path: Path, params: Dict) -> FileExecutionOrder:
        # Placeholder for a different sorting logic
        return FileExecutionOrder(rejected=[], once=[], replay=[])


sorters = {
    "alpha": AlphaPatternFileSorter(),
    "beta": BetaFileSorter(),
}


class SchemaManager:
    """Manages the execution of SQL schema files based on provided parameters."""

    def __init__(self, params: dict, sql_path: str = None):
        EXCLUDE_KEYS = {"dry_run", "sql_path", "warehouse_id", "environment_code"}
        self.params: dict = {k: v for k, v in params.items() if k not in EXCLUDE_KEYS}
        self.dry_run: bool = params.get("dry_run", "false").lower() == "true"
        base_path = sql_path or params.get("sql_path", "")
        self.sql_path: Path = Path(base_path).resolve()
        self.warehouse_id: str = params.get("warehouse_id", "")
        self.target_catalog: str = params.get("target_catalog", "")
        sorter_name: str = params.get("sorter", "alpha").lower()
        self.sorter: FileSorter = sorters.get(sorter_name, AlphaPatternFileSorter())

    def _get_connection(self):
        return sql.connect(
            server_hostname=get_context().apiUrl,
            http_path=f"/sql/1.0/warehouses/{self.warehouse_id}",
            access_token=get_context().apiToken,
            user_agent_entry="Schema Management",
            catalog=self.target_catalog,
        )

    def get_executed_files(self) -> List[str]:
        try:
            with self._get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT file_name
                        FROM data_platform.schema_execution_log
                        WHERE file_path = :file_path""",
                        {"file_path": str(self.sql_path)},
                    )
                    results = cursor.fetchall()
                    return [row[0] for row in results]
        except Exception as e:
            print(f"Error getting executed files: {e}")
            return []

    def update_executed_file(self, file_name: str) -> None:
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO data_platform.schema_execution_log
                    VALUES (:file_path, :file_name, current_timestamp(), current_user())""",
                    {"file_path": str(self.sql_path), "file_name": file_name},
                )
        return

    def run_queries(self, queries: List[str]) -> None:
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                for index, query in enumerate(queries):
                    print("-" * 80)
                    print(f"Executing query [{index + 1}/{len(queries)}]")
                    print(f"> Query parameters: {json.dumps(self.params, indent=2)}")
                    try:
                        query = query.format(**self.params)
                    except Exception as e:
                        print(f"> Error when trying to str.format() query: {e}")
                    print(f"\033[94m{query}\033[0m")

                    if self.dry_run:
                        print("\033[91m[ DRY-RUN-MODE ]\033[0m query not executed")
                        continue
                    cursor.execute(query, self.params)
                    print("\033[32m> SUCCESS\033[0m")

    def _extract_queries(self, sql_content: str) -> List[str]:
        # Split the SQL content by semicolon to separate queries
        return [query.strip() for query in sql_content.split(";") if query.strip()]

    def run(self):
        # Check if sql_path exists and finish execution gracefully
        if not self.sql_path.exists():
            print(f"\033[91m[ SKIP ]\033[0m SQL path does not exist: {self.sql_path}")
            return

        # List and sort all files in the sql_path directory
        file_order: FileExecutionOrder = self.sorter.sort_files(self.sql_path, self.params)

        if self.dry_run:
            print("\033[91m[ DRY-RUN-MODE ]\033[0m Notice: no changes will be applied while in dry-run mode\n\n")

        # Print initial information
        print("JOB INFORMATION")
        print(f"SQL root folder: {self.sql_path}")
        if file_order.rejected:
            print(f"Files rejected (did not match pattern): {len(file_order.rejected)}")
            for file in file_order.rejected:
                print(f"> \033[91m[ REJECTED ]\033[0m {file}")
            print(f"> Make sure they follow the pattern: \033[94m{self.sorter.rejected_hint}\033[0m")

        # Iterate over replayable operations first
        print("\n\nRECURRING OPERATIONS")
        print(f"Found {len(file_order.replay)} SQL files to replay")
        for replay in file_order.replay:
            with (self.sql_path / replay).open("r") as file:
                sql_content = file.read()

            # Split the SQL content by semicolon to separate queries
            queries = self._extract_queries(sql_content)
            print("=" * 80)
            # Execute the SQL query with the provided arguments
            print(f"> Applying replayable operation using [\033[94m{replay}\033[0m]")
            self.run_queries(queries)
            print("> Replayable operation applied successfully")

        # Iterate over schema versions greater than the current version
        print("\n\nONLY-ONCE OPERATIONS")
        print(f"Found {len(file_order.once)} only-once operations to apply")
        executed_files = self.get_executed_files()
        executed_count = 0
        for once in file_order.once:
            # If the file has already been executed, skip it
            if once in executed_files:
                print(f"> \033[94m[ SKIPPED ]\033[0m File [\033[94m{once}\033[0m] has already been executed")
                continue

            with (self.sql_path / once).open("r") as file:
                sql_content = file.read()

            # Split the SQL content by semicolon to separate queries
            queries = self._extract_queries(sql_content)
            print("=" * 80)

            # Execute the SQL query with the provided arguments
            print(f"> Applying only-once operation using [\033[94m{once}\033[0m]")
            self.run_queries(queries)

            # If successfull, update executed files
            if self.dry_run:
                print("\033[91m[ DRY-RUN-MODE ]\033[0m operation will not be marked as executed")
            else:
                self.update_executed_file(once)
                print("> Only-once operation applied and marked as executed successfully")
            executed_count += 1

        print("\n\n")
        print("=" * 80)
        print(
            f"{'\033[91m[ DRY-RUN-MODE ]\033[0m ' if self.dry_run else ''}COMPLETED: Applied \033[94m{len(file_order.replay)}\033[0m replayable operations and \033[94m{executed_count}\033[0m only-once operations"
        )
