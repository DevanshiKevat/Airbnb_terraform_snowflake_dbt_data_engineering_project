from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from upload_to_s3 import upload_files_to_s3

default_args = {
    "owner": "Devanshi",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="upload_data_to_s3",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
    default_args=default_args,
    tags=["airbnb", "upload"],
) as dag:

    upload_to_s3 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_files_to_s3
    )