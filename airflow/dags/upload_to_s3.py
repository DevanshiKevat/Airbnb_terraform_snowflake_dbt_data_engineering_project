import boto3
import os
from airflow.hooks.base import BaseHook

def upload_files_to_s3():
    # 🔥 Get credentials from Airflow connection
    aws_conn = BaseHook.get_connection("aws_default")

    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_conn.login,
        aws_secret_access_key=aws_conn.password,
        region_name="us-east-1"
    )

    BUCKET_NAME = "airbnb-raw-data-26"
    LOCAL_FOLDER = "/opt/airflow/data"

    for file in os.listdir(LOCAL_FOLDER):
        if file.endswith(".csv"):
            file_path = os.path.join(LOCAL_FOLDER, file)
            s3_key = f"raw/{file}"

            print(f"Uploading {file}...")
            s3.upload_file(file_path, BUCKET_NAME, s3_key)

    print("All files uploaded successfully!")