# Clinlytix360: End-to-End Clinical & Real-World Outcomes Analytics Platform

Clinlytix360 is a full-stack, containerized data analytics pipeline that simulates real-world clinical data, performs survival and feasibility analysis, and visualizes insights through an interactive Streamlit dashboard. The project is designed to mirror analytical workflows used in clinical trial design, PRO/COA psychometrics, and real-world evidence (RWE) analysis — making it ideal for demonstrating skills relevant to roles at IQVIA, Flatiron Health, and other healthcare data science teams.

---

## 🚀 Features

- ✅ **Synthetic EHR + Clinical Trial Data Simulation**
- ✅ **Apache Airflow DAG** orchestrating ETL, modeling, and report generation
- ✅ **Kaplan-Meier survival curves** grouped by cancer stage
- ✅ **Cox Proportional Hazards model** with summary & hazard ratio plot
- ✅ **Feasibility modeling** based on inclusion/exclusion criteria
- ✅ **Interactive Streamlit dashboard** with filtering and visual insights
- ✅ **Dockerized setup** with CeleryExecutor, Postgres, Redis

---

## 🧠 Architecture Overview

**Clinlytix360** is composed of three key layers:

1. **Data Layer**
   - Simulated datasets: `ehr_oncology.csv`, `trial_protocol.csv`, `pro_scores.csv`
   - Cleaned and transformed to create survival data, eligibility tables, and PRO metrics

2. **Pipeline Layer (Apache Airflow)**
   - DAG: `clinlytix360_pipeline`
   - Tasks: `run_etl_cleaning`, `run_survival_analysis`, `run_feasibility_model`, `log_dashboard_refresh`
   - Orchestrates analytics tasks with BashOperators

3. **Presentation Layer (Streamlit)**
   - Dashboard that shows:
     - Kaplan-Meier plots
     - Cox model summaries and hazard ratios
     - Filtered patient data tables

---

## 📁 Folder Structure

clinlytix360_airflow/

├── dags/

│ └── clinlytix_dag.py

├── data/

│ ├── ehr_oncology.csv

│ ├── trial_protocol.csv

│ ├── pro_scores.csv

│ ├── outputs/

│ │ ├── km_plot.png

│ │ ├── cox_plot.png

│ │ ├── cox_summary.txt

│ │ └── site_feasibility_report.csv

├── scripts/

│ ├── etl/

│ │ └── etl_cleaning.py

│ ├── modeling/

│ │ └── survival_analysis.py

│ └── dashboards/

│ └── app.py

├── docker-compose.yaml

├── requirements.txt

├── LICENSE

├── .gitignore

└── README.md



---

## 🔧 How to Run

### Prerequisites
- Docker Desktop (with WSL2 backend)
- Python 3.10+ for local testing (optional)

### Step 1: Start Airflow & DAG
```bash
cd clinlytix360_airflow
docker compose up --build
```

Then go to: http://localhost:8080 and log in with:
```
Username: airflow

Password: airflow
```

Trigger the DAG named ```clinlytix360_pipeline```



