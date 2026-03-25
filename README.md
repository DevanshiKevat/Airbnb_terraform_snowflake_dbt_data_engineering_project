# 🏡 Airbnb Data Engineering Pipeline

## 🚀 Project Overview

This project demonstrates an end-to-end data engineering pipeline using modern tools and best practices.

The pipeline ingests Airbnb data, processes it using dbt, and prepares it for analytics.

---

## 🧱 Architecture

S3 → Snowflake (RAW) → dbt (STAGING → INTERMEDIATE → MART) → Power BI

---

## 🛠️ Tech Stack

* Snowflake (Data Warehouse)
* AWS S3 (Data Lake)
* Terraform (Infrastructure as Code)
* Python (Data Ingestion)
* dbt (Transformation)
* Airflow (Orchestration - upcoming)
* Power BI (Visualization)

---

## 📂 Project Structure

* `terraform/` → Infrastructure setup
* `ingestion/` → Python scripts for S3 upload
* `dbt_project/` → Transformation logic
* `airflow/` → Orchestration (planned)

---

## 🔄 Data Pipeline Flow

1. Upload data to S3
2. Snowflake loads data using external stage
3. dbt transforms data into staging, intermediate, and mart layers
4. Incremental models optimize performance
5. Snapshots track historical changes (SCD Type 2)

---

## ⚡ Key Features

* Incremental data processing
* Slowly Changing Dimensions (SCD Type 2)
* Modular dbt models
* Infrastructure as Code (Terraform)
* Scalable architecture

---

## 📊 Future Enhancements

* Airflow DAG for orchestration
* CI/CD pipeline using GitHub Actions
* Power BI dashboard integration

---

## 👩‍💻 Author

Devanshi
