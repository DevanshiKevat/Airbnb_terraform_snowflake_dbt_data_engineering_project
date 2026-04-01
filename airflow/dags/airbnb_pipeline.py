from airflow import DAG
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# =========================================================
# CONFIG
# =========================================================
DBT_PROJECT_DIR = "/opt/airflow/dbt/airbnb_dbt"
DBT_CMD = "/home/airflow/.local/bin/dbt"

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
        return [r[0] for r in records]

    @task
    def build_queries(files):
        queries = []
        for file in files:
            table = file.split(".")[0].upper() + "_RAW"
            queries.append(f"""
            COPY INTO AIRBNB_DB.RAW.{table}
            FROM '@AIRBNB_DB.RAW.AIRBNB_STAGE/{file}'
            FILE_FORMAT = (FORMAT_NAME = AIRBNB_CSV_FORMAT)
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
            ON_ERROR = 'CONTINUE';
            """)
        return queries

    files = get_files()
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
    )

    dbt_docs = BashOperator(
        task_id="dbt_docs",
        bash_command=f"{DBT_CMD} docs generate --project-dir {DBT_PROJECT_DIR}",
    )

    # 🔗 Updated flow (starts from SQS now)
    refresh_stage >> files >> queries >> copy_into >> dbt_run >> dbt_test >> dbt_snapshot >> dbt_docs