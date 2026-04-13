import logging
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)   # ✅ fix 1

DBT_PROJECT_DIR = "/opt/airflow/dbt/airbnb_dbt"
DBT_CMD         = "/home/airflow/.local/bin/dbt"

default_args = {
    "owner": "Devanshi",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="airbnb_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["airbnb", "snowflake", "dbt"],
) as dag:

    refresh_stage = SQLExecuteQueryOperator(
        task_id="refresh_stage",
        conn_id="snowflake_connection",
        sql="ALTER STAGE AIRBNB_STAGE REFRESH;"
    )

    @task
    def get_files():
        hook = SnowflakeHook(snowflake_conn_id="snowflake_connection")
        records = hook.get_records(
            "SELECT RELATIVE_PATH FROM DIRECTORY(@AIRBNB_DB.RAW.AIRBNB_STAGE)"
        )
        files = [r[0] for r in records]
        logger.info("Files found in stage: %s", files)
        return files

    @task
    def build_queries(files):
        queries = []
        for file in files:
            filename = file.split("/")[-1]             # ✅ fix 3 — strip folder prefix
            table    = filename.split(".")[0].upper() + "_RAW"
            queries.append(f"""
                COPY INTO AIRBNB_DB.RAW.{table}
                FROM '@AIRBNB_DB.RAW.AIRBNB_STAGE/{file}'
                FILE_FORMAT = (FORMAT_NAME = AIRBNB_CSV_FORMAT)
                MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
                ON_ERROR = 'CONTINUE';
            """)
            logger.info("Built query for table: %s from file: %s", table, file)
        return queries

    files   = get_files()
    queries = build_queries(files)

    copy_into = SQLExecuteQueryOperator.partial(
        task_id="copy_into",
        conn_id="snowflake_connection",
    ).expand(sql=queries)

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{DBT_CMD} run --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{DBT_CMD} test --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=f"{DBT_CMD} snapshot --project-dir {DBT_PROJECT_DIR}",
        trigger_rule="all_done",   # ✅ fix 4 — runs even if dbt_test has failures
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs",
        bash_command=f"{DBT_CMD} docs generate --project-dir {DBT_PROJECT_DIR}",
        trigger_rule="all_done",
    )

    refresh_stage >> files >> queries >> copy_into >> dbt_run >> dbt_test >> dbt_snapshot >> dbt_docs