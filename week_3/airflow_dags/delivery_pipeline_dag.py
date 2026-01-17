import os
import sys
import logging
import pandas as pd
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Senior Dev Note: This mount ensures we reuse the Week 1 scraper logic
# without maintaining two copies of the same extraction code.
REPO_ROOT = "/opt/airflow/repo"
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)

try:
    from week_1.etl_pipeline import execute_extraction
except ImportError as e:
    logging.error("Sourcing Error: Verify /opt/airflow/repo mount and __init__.py.")
    raise e

DEFAULT_ARGS = {
    'owner': 'Grace Irungu',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False
}

@dag(
    dag_id='icp_gold_delivery_pipeline_v3',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['production', 'medallion', 'silver_layer']
)
def delivery_pipeline():

    @task
    def run_ingestion():
        logging.info("Triggering Bronze Layer extraction engine...")
        return execute_extraction()

    @task
    def load_to_silver_layer(csv_path: str):
        """
        Moves data to Silver Layer with Idempotency.
        Ensures 95% Quality SLA by preventing duplicate record accumulation.
        """
        if not csv_path or not os.path.exists(csv_path):
            raise FileNotFoundError(f"Data not found at: {csv_path}")

        # PostgresHook avoids the 'invalid dsn' SQLAlchemy error.
        hook = PostgresHook(postgres_conn_id='postgres_default')
        df = pd.read_csv(csv_path)

        # ARCHITECT'S LOGIC: Idempotency check.
        # We truncate the table before loading to ensure a fresh state.
        # This prevents the '130 rows' duplicate issue by resetting the table.
        logging.info("Cleansing Silver Layer table for idempotent load...")
        hook.run("TRUNCATE TABLE silver_quotes;")

        # Mapping Bronze headers (raw_text, author_name) to Silver schema (quote, author)
        # This handles the KeyError by explicitly selecting available columns.
        try:
            data_to_insert = df[['raw_text', 'author_name']].values.tolist()
            
            hook.insert_rows(
                table='silver_quotes',
                rows=data_to_insert,
                target_fields=['quote', 'author'],
                commit_every=1000 
            )
            logging.info(f"Successfully delivered {len(df)} clean records to the Silver Layer.")
        except KeyError as e:
            logging.error(f"Mapping Failure: Check CSV headers. Found: {df.columns.tolist()}")
            raise e
            
        return "Silver Migration Complete"

    # Orchestration: Task Dependencies
    path_to_data = run_ingestion()
    load_to_silver_layer(path_to_data)

# Deployment Instance
delivery_pipeline_instance = delivery_pipeline()