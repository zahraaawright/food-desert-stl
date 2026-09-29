"""Weekly DAG: pull source data, land it in BigQuery, then run dbt.

Assumes places_api.py and census_api.py are adapted to load their output
straight into BigQuery rather than local CSVs, and that dbt is available
in the Airflow environment (a BashOperator shelling into a venv/Docker
image with dbt-bigquery installed works fine for a portfolio project).
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-eng",
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="food_desert_pipeline",
    default_args=default_args,
    schedule="@weekly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["food-desert", "portfolio"],
) as dag:

    extract_places = BashOperator(
        task_id="extract_places",
        bash_command="python /opt/airflow/ingestion/places_api.py",
    )

    extract_census = BashOperator(
        task_id="extract_census",
        bash_command="python /opt/airflow/ingestion/census_api.py",
    )

    run_dbt = BashOperator(
        task_id="run_dbt",
        bash_command="cd /opt/airflow/dbt && dbt run",
    )

    [extract_places, extract_census] >> run_dbt
