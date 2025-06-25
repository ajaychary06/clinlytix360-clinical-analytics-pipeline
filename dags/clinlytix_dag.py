from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ajayc',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='clinlytix360_pipeline',
    default_args=default_args,
    description='Automated Clinlytix360 pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags=['clinlytix'],
) as dag:

    # 1. Data Cleaning
    etl_cleaning = BashOperator(
        task_id='run_etl_cleaning',
        bash_command='python /opt/airflow/data/scripts/etl/etl_cleaning.py'
    )

    # 2. Survival Analysis
    survival = BashOperator(
        task_id='run_survival_analysis',
        bash_command='python /opt/airflow/data/scripts/modeling/survival_analysis.py'
    )

    # 3. Trial Feasibility
    feasibility = BashOperator(
        task_id='run_feasibility_model',
        bash_command='python /opt/airflow/data/scripts/modeling/feasibility_model.py'
    )

    # (Optional) Dashboard Trigger or Logging Task
    log_refresh = BashOperator(
        task_id='log_dashboard_refresh',
        bash_command='echo "Dashboard ready to serve latest data."'
    )

    # DAG dependencies
    etl_cleaning >> [survival, feasibility] >> log_refresh
