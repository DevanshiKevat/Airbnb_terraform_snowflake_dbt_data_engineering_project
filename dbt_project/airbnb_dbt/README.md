# 🏡 Airbnb Data Engineering Pipeline

## 🚀 Project Overview

This project demonstrates an end-to-end data engineering pipeline using modern tools and best practices.

The pipeline ingests Airbnb data, processes it using dbt, and prepares it for analytics. It also incorporates **event-driven orchestration using Airflow and AWS SQS**, making the pipeline more scalable and production-ready.

---

## 🧱 Architecture

S3 → SQS → Airflow → Snowflake (RAW) → dbt (STAGING → INTERMEDIATE → MART) → Power BI

---

## 🛠️ Tech Stack

* Snowflake (Data Warehouse)
* AWS S3 (Data Lake)
* AWS SQS (Event-driven trigger)
* Terraform (Infrastructure as Code)
* Python (Data Ingestion)
* dbt (Transformation, Testing, Documentation)
* Airflow (Orchestration)
* Power BI (Visualization)

---

## 📂 Project Structure

* `terraform/` → Infrastructure setup (S3, SQS, IAM)
* `ingestion/` → Python scripts for S3 upload
* `dbt_project/` → Transformation logic, tests, snapshots, docs
* `airflow/` → DAGs for orchestration and automation

---

## 🔄 Data Pipeline Flow

1. Upload data to S3
2. S3 triggers an event → sent to SQS
3. Airflow SQS sensor detects event and starts pipeline
4. Snowflake loads data using external stage (RAW layer)
5. dbt transforms data into staging, intermediate, and mart layers
6. dbt tests validate data quality
7. dbt snapshots track historical changes (SCD Type 2)
8. dbt docs generate lineage and metadata

---

## ⚡ Key Features

* Event-driven pipeline (S3 → SQS → Airflow)
* Incremental data processing
* Slowly Changing Dimensions (SCD Type 2)
* Modular dbt models (layered architecture)
* Data quality testing with dbt
* Auto-generated documentation (dbt docs)
* Infrastructure as Code (Terraform)
* Scalable and decoupled architecture

---

## 📊 Future Enhancements

* Airflow DAG for orchestration
* CI/CD pipeline using GitHub Actions
* Power BI dashboard integration

---

## 👩‍💻 Author

Devanshi
