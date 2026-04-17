# 🏡 Airbnb Data Engineering Pipeline

## 🚀 Project Overview

This project demonstrates a **fully automated, event-driven data engineering pipeline** built using modern cloud-native tools.

The pipeline ingests Airbnb datasets, processes them using dbt, and prepares analytics-ready models. Once data is uploaded to S3, the entire pipeline runs automatically — from ingestion to transformation, validation, and documentation.

---

## 🧱 Architecture

S3 → SQS → Lambda → Airflow → Snowflake (RAW) → dbt (STAGING → INTERMEDIATE → MART) → Power BI

---

## 🛠️ Tech Stack

| Layer            | Technology |
|-----------------|-----------|
| Data Lake        | AWS S3 |
| Event Handling   | AWS SQS |
| Trigger Logic    | AWS Lambda |
| Orchestration    | Apache Airflow (Docker) |
| Data Warehouse   | Snowflake |
| Transformation   | dbt |
| Infrastructure   | Terraform |
| Visualization    | Power BI |

---

## 📂 Project Structure

```
AIRBNB_DATA_ENGINEERING_PROJECT/
│
├── airflow/
│ ├── dags/
│ │ ├── airbnb_pipeline.py
│ │ └── upload_to_s3.py
│ ├── docker-compose.yml
│
├── dbt_project/
│ └── airbnb_dbt/
│ ├── models/
│ ├── snapshots/
│ ├── tests/
│
├── terraform/
│ ├── aws/
│ │ ├── s3.tf
│ │ ├── sqs.tf
│ │ ├── iam.tf
│ │ ├── lambda.tf
│ │
│ └── snowflake/
│ ├── warehouse.tf
│ ├── stage.tf
│ ├── integration.tf
│ ├── file_format.tf
│
├── ingestion/
│ └── upload_to_s3.py
│
├── data/
│ ├── bookings.csv
│ ├── hosts.csv
│ └── listings.csv
│
├── requirements.txt
├── README.md
└── .gitignore
```
---

## 🔄 Data Pipeline Flow

### 1. File Upload
CSV files are uploaded to S3 (`raw/` folder) manually or via Airflow DAG.

### 2. Event Trigger
S3 generates an `ObjectCreated` event and sends it to SQS.

### 3. Lambda Processing
- Consumes SQS messages  
- Validates required files:
  - `listings.csv`
  - `hosts.csv`
  - `bookings.csv`
- Writes a `_triggered` marker file to prevent duplicate runs  
- Calls Airflow REST API to trigger pipeline  

### 4. Airflow Execution
- DAG starts automatically  
- Uses dynamic task mapping to process files  

### 5. Snowflake Ingestion
- External stage reads data directly from S3  
- `COPY INTO` loads data into RAW tables  

### 6. dbt Transformation
- STAGING → cleaning & standardization  
- INTERMEDIATE → joins & business logic  
- MART → analytics-ready models  

### 7. Data Validation
dbt tests validate:
- Not null constraints  
- Uniqueness  

### 8. Historical Tracking
dbt snapshots implement **SCD Type 2**

### 9. Documentation
dbt docs generate lineage and metadata

---

## ⚡ Key Features

- Event-driven pipeline (S3 → SQS → Lambda → Airflow)  
- Fully automated execution  
- Incremental data processing  
- SCD Type 2 implementation  
- Dynamic task mapping in Airflow  
- Infrastructure as Code (Terraform)  
- External stage in Snowflake  
- Data quality testing with dbt  
- Auto-generated documentation  
- Fault-tolerant architecture using SQS  

---

## 🧠 Design Decisions

| Decision | Why |
|--------|-----|
| SQS between S3 & Lambda | Ensures retry and decoupling |
| Lambda trigger layer | Adds validation and control |
| `_triggered` marker | Prevents duplicate DAG execution |
| External stage | Direct S3 read (efficient & cost-effective) |
| dbt layered architecture | Separation of concerns |
| Incremental models | Cost optimization |
| Snapshots (SCD2) | Historical tracking |
| Terraform | Reproducible infrastructure |

---

## 📊 Data Model

### RAW Layer
- Direct ingestion using `COPY INTO`
- No transformations  

### STAGING Layer
- Cleaning and standardization  
- Materialized as views  

### INTERMEDIATE Layer
- Business logic and joins  
- Materialized as tables  

### MART Layer
- Analytics-ready models:
  - `dim_hosts`
  - `dim_listings`
  - `fct_bookings` (incremental)

---

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

## 🧠 Design Decisions

* **SQS used for decoupling** → avoids tight coupling between S3 and Airflow
* **External stage in Snowflake** → efficient bulk ingestion
* **Dynamic task mapping in Airflow** → scalable file processing
* **dbt for transformation** → modular, testable, and documented models

---

## ⚠️ Challenges Faced

* Docker path resolution issues
* AWS credential handling inside Docker
* S3 → SQS permission configuration
* Preventing duplicate triggers
* dbt profile configuration in Airflow
* Lambda retry handling

---

## 📊 Future Enhancements

* CI/CD using GitHub Actions
* Hosting dbt docs on S3
* Dead-letter queue (DLQ) for SQS
* Alerting and monitoring system
* Production-grade Airflow deployment
* Power BI dashboard integration

---

## 👩‍💻 Author

Devanshi

---

## 💡 Final Thought

This project demonstrates how to design and implement a **modern, event-driven data pipeline**, combining infrastructure automation, orchestration, and transformation into a scalable data platform.
