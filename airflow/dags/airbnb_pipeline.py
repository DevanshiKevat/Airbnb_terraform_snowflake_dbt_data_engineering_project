from airflow import DAG
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# 🔹 Import custom ingestion logic (S3 upload script)
# This file is placed inside the dags folder so Airflow can import it
from upload_to_s3 import upload_files_to_s3


# =========================================================
# 🔹 Central Configuration (IMPORTANT DESIGN PATTERN)
# =========================================================

# 👉 Absolute path inside container where dbt project is mounted
# This comes from docker-compose:
#   ../dbt_project:/opt/airflow/dbt
# So actual project becomes:
#   /opt/airflow/dbt/airbnb_dbt
DBT_PROJECT_DIR = "/opt/airflow/dbt/airbnb_dbt"

# 👉 dbt executable path inside container
# dbt gets installed in airflow user local bin directory
# Without this full path, Airflow may say "dbt not found"
DBT_CMD = "/home/airflow/.local/bin/dbt"


# =========================================================
# 🔹 Default DAG Arguments (applies to all tasks)
# =========================================================
default_args = {
    "owner": "Devanshi",                  # owner of DAG (for tracking/debugging)
    "retries": 2,                         # retry failed tasks
    "retry_delay": timedelta(minutes=5),  # wait time between retries
}


# =========================================================
# 🔹 DAG Definition
# =========================================================
with DAG(
    dag_id="airbnb_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,   # manual trigger (can be changed later)
    catchup=False,            # don't backfill old runs
    default_args=default_args,
    tags=["airbnb", "snowflake", "dbt"],
) as dag:


    # =========================================================
    # 1. Upload Local Files → S3
    # =========================================================
    # 👉 This simulates ingestion layer
    # 👉 Reads from /opt/airflow/data (mounted from local machine)
    upload_to_s3 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_files_to_s3
    )


    # =========================================================
    # 2. Wait for S3 Event (via SQS)
    # =========================================================
    # 👉 Event-driven pipeline
    # 👉 When file lands in S3 → SQS message is generated
    # 👉 Sensor waits until message is received
    wait_for_s3_event = SqsSensor(
        task_id="wait_for_s3_event",
        sqs_queue="https://sqs.us-east-1.amazonaws.com/507325772253/airbnb-s3-events-queue",
        aws_conn_id="aws_default",
        max_messages=1,
        wait_time_seconds=20,
        delete_message_on_reception=True
    )


    # =========================================================
    # 3. Refresh Snowflake Stage
    # =========================================================
    # 👉 Snowflake external stage needs refresh to detect new files
    refresh_stage = SQLExecuteQueryOperator(
        task_id="refresh_stage",
        conn_id="snowflake_connection",
        sql="ALTER STAGE AIRBNB_STAGE REFRESH;"
    )


    # =========================================================
    # 4. Get List of Files from Stage
    # =========================================================
    @task
    def get_files():
        """
        Fetch list of files available in Snowflake stage directory.
        """
        hook = SnowflakeHook(snowflake_conn_id="snowflake_connection")

        records = hook.get_records(
            "SELECT RELATIVE_PATH FROM DIRECTORY(@AIRBNB_DB.RAW.AIRBNB_STAGE)"
        )

        # Convert list of tuples → list of strings
        return [r[0] for r in records]


    # =========================================================
    # 5. Build COPY INTO Queries Dynamically
    # =========================================================
    @task
    def build_queries(files):
        """
        Generate COPY INTO queries dynamically for each file.
        Each file maps to a RAW table.
        """
        queries = []

        for file in files:
            # Example: bookings.csv → BOOKINGS_RAW
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


    # =========================================================
    # 6. Load Data into Snowflake (Dynamic Task Mapping)
    # =========================================================
    # 👉 Runs COPY INTO for each file dynamically
    copy_into = SQLExecuteQueryOperator.partial(
        task_id="copy_into",
        conn_id="snowflake_connection",
    ).expand(sql=queries)


    # =========================================================
    # 7. dbt Run (Transform Data)
    # =========================================================
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"{DBT_CMD} run --project-dir {DBT_PROJECT_DIR}",
    )


    # =========================================================
    # 8. dbt Test (Data Quality Checks)
    # =========================================================
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"{DBT_CMD} test --project-dir {DBT_PROJECT_DIR}",
    )


    # =========================================================
    # 9. dbt Snapshot (Slowly Changing Dimensions)
    # =========================================================
    # 👉 Tracks historical changes in data
    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=f"{DBT_CMD} snapshot --project-dir {DBT_PROJECT_DIR}",
    )
    
    # =========================================================
    # 10. dbt Docs (Generate Documentation)
    # =========================================================
    # 👉 Generates static documentation (lineage + metadata)
    # 👉 Can be hosted later or viewed locally
    dbt_docs = BashOperator(
        task_id="dbt_docs",
        bash_command=f"{DBT_CMD} docs generate --project-dir {DBT_PROJECT_DIR}",
    )

    # =========================================================
    # 🔗 DAG Flow (End-to-End Pipeline)
    # =========================================================
    upload_to_s3 >> wait_for_s3_event >> refresh_stage >> files >> queries >> copy_into >> dbt_run >> dbt_test >> dbt_snapshot >> dbt_docs

    # /home/airflow/.local/bin/dbt docs serve   --project-dir /opt/airflow/dbt/airbnb_dbt   --port 8081
    # Command to see docs generated by dbt (run this in terminal after DAG runs successfully)