# 🏡 Airbnb Data Engineering Pipeline

## 🚀 Project Overview

This project demonstrates an end-to-end data engineering pipeline using modern tools and best practices.

The pipeline ingests Airbnb data, processes it using dbt, and prepares it for analytics. It also incorporates **event-driven orchestration using Airflow and AWS SQS**, making the pipeline scalable, automated, and production-ready.

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

## 📊 Data Model

### Layered Architecture

**RAW Layer (Snowflake)**

* Direct ingestion from S3 using `COPY INTO`
* Minimal transformation

**STAGING Layer (dbt)**

* Basic cleaning and standardization
* Column formatting 

**INTERMEDIATE Layer (dbt)**

* Business logic transformations
* Joins and derived fields

**MART Layer (dbt)**

* Analytics-ready tables
* Optimized for reporting (Power BI)

---

## ⚡ Key Features

* Event-driven pipeline (S3 → SQS → Airflow)
* Incremental data processing
* Slowly Changing Dimensions (SCD Type 2)
* Modular dbt models (layered architecture)
* Data quality testing with dbt
* Auto-generated documentation (dbt docs)
* Infrastructure as Code (Terraform)
* Dynamic ingestion using Airflow task mapping

---

## 📁 Project Structure

## 📁 Project Structure

```
AIRBNB_DATA_ENGINEERING_PROJECT/
│
├── airflow/
│   ├── dags/
│   │   ├── airbnb_pipeline.py
│   │   └── upload_to_s3.py
│   ├── docker-compose.yml
│   ├── plugins/
│   └── logs/
│
├── dbt_project/
│   └── airbnb_dbt/
│       ├── models/
│       ├── snapshots/
│       ├── tests/
│       └── dbt_project.yml
│
├── terraform/
│   ├── aws/
│   │   ├── s3.tf
│   │   ├── sqs.tf
│   │   ├── iam.tf
│   │
│   └── snowflake/
│
├── ingestion/
│   └── upload_to_s3.py
│
├── data/
│   ├── bookings.csv
│   ├── hosts.csv
│   └── listings.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Execution Steps

### 1. Provision Infrastructure

```bash
terraform init
terraform apply
```

### 2. Start Airflow

```bash
docker compose up
```

### 3. Trigger Pipeline

* Upload file to S3 OR
* Trigger DAG manually

---

## 📊 Observability

Pipeline execution can be monitored through:

* Airflow UI → DAG and task status
* Snowflake → Query history and load status
* dbt → Test results and documentation

---

## 🔍 Data Validation Strategy

| Layer     | Validation         |
| --------- | ------------------ |
| S3        | File presence      |
| Snowflake | Load success       |
| dbt       | Data quality tests |

---

## 🧠 Design Decisions

* **SQS used for decoupling** → avoids tight coupling between S3 and Airflow
* **External stage in Snowflake** → efficient bulk ingestion
* **Dynamic task mapping in Airflow** → scalable file processing
* **dbt for transformation** → modular, testable, and documented models

---

## ⚠️ Challenges Faced

* Docker path resolution issues
* AWS credential handling inside containers
* S3 → SQS permission validation
* dbt profile configuration inside Airflow

---

## 🐛 Troubleshooting

**No SQS Messages**

* Check S3 notification configuration
* Verify IAM policy

**Airflow Sensor Not Triggering**

* Validate SQS queue URL
* Check AWS connection in Airflow

**dbt Failures**

* Ensure correct profiles.yml path
* Run `dbt debug`

---

## 📊 Future Enhancements

* CI/CD pipeline using GitHub Actions
* Hosting dbt docs on S3
* Incremental ingestion with partitioning
* Alerting and monitoring system
* Power BI dashboard integration

---

## 👩‍💻 Author

Devanshi

---

## 💡 Final Thought

This project demonstrates how to design and implement a **modern, event-driven data pipeline**, combining infrastructure automation, orchestration, and transformation into a scalable data platform.
