# Clinlytix360: End-to-End Clinical & Real-World Outcomes Analytics Platform

Clinlytix360 is a full-stack, containerized data analytics pipeline that simulates real-world clinical data, performs survival and feasibility analysis, and visualizes insights through an interactive Streamlit dashboard. The project is designed to mirror analytical workflows used in clinical trial design, PRO/COA psychometrics, and real-world evidence (RWE) analysis 

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

## Step 2: Launch Streamlit Dashboard
``` bash
cd clinlytix360_airflow/scripts/dashboards
streamlit run app.py
```

Then go to: http://localhost:8501


## 📊 Key Visual Outputs

| Visualization                 | Description                                             |
| ----------------------------- | ------------------------------------------------------- |
| `km_plot.png`                 | Kaplan-Meier survival curves by cancer stage            |
| `cox_summary.txt`             | Text summary of Cox regression model                    |
| `cox_plot.png`                | Hazard ratios from Cox model as a bar chart             |
| `site_feasibility_report.csv` | Site-level patient eligibility and projected enrollment |


## 🧪 Use Cases Simulated

- Real-world evidence (RWE) modeling

- Clinical trial feasibility planning

- PRO/COA psychometric data capture

- Risk factor identification with Cox regression

- Automated clinical data pipelines (Airflow)


## 📜 License

This project is licensed under the MIT License — see the ```LICENSE``` file for details.


Built by Ajaychary as a showcase of healthcare analytics, MLOps, and end-to-end data pipeline orchestration.




## 📬 Questions or Feedback?
Open an issue or contact me directly on GitHub. Contributions welcome!

🔗 [Portfolio](https://ajaychary06.github.io/Portfolio/) 

🐍 [GitHub](https://github.com/ajaychary06) 

💼 [LinkedIn](https://www.linkedin.com/in/ajaychary-kandukuri-053a5a25a/)”




