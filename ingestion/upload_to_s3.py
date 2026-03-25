import boto3
import os

# Initialize S3 client
s3 = boto3.client('s3')

BUCKET_NAME = "airbnb-raw-data-26"

# Local folder where your CSV files are stored
LOCAL_FOLDER = "data"

# Upload all files
for file in os.listdir(LOCAL_FOLDER):
    if file.endswith(".csv"):
        file_path = os.path.join(LOCAL_FOLDER, file)

        s3_key = f"raw/{file}"   # S3 folder structure

        print(f"Uploading {file}...")

        s3.upload_file(file_path, BUCKET_NAME, s3_key)

print("All files uploaded successfully!")