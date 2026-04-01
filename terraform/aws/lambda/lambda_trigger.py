import json
import requests
import os

AIRFLOW_URL = os.environ["AIRFLOW_URL"]
USERNAME = os.environ["AIRFLOW_USERNAME"]
PASSWORD = os.environ["AIRFLOW_PASSWORD"]

def lambda_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])

        print("SQS Message:", body)

        # Trigger Airflow DAG
        response = requests.post(
            f"{AIRFLOW_URL}/api/v1/dags/airbnb_pipeline/dagRuns",
            auth=(USERNAME, PASSWORD),
            json={"conf": body}
        )

        print("Airflow Response:", response.status_code)

    return {"status": "success"}