from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DUCKDB_PATH = PROJECT_ROOT / "nyc_taxi.duckdb"


def database_exists(database_path: Path = DEFAULT_DUCKDB_PATH) -> bool:
    return database_path.exists()


def read_table(table_name: str, database_path: Path = DEFAULT_DUCKDB_PATH) -> pd.DataFrame:
    if not database_path.exists():
        raise FileNotFoundError(
            f"DuckDB database not found at {database_path}. Run `dbt build --profiles-dir .` first."
        )

    with duckdb.connect(str(database_path), read_only=True) as connection:
        return connection.execute(f"select * from {table_name}").fetchdf()


def load_dashboard_tables(database_path: Path = DEFAULT_DUCKDB_PATH) -> dict[str, pd.DataFrame]:
    return {
        "trips": read_table("fct_taxi_trips", database_path),
        "daily_metrics": read_table("mart_daily_taxi_metrics", database_path),
        "route_revenue": read_table("mart_route_revenue", database_path),
    }
