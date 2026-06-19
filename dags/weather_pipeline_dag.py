from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="weather_pipeline",
    description="Pipeline de clima com camadas bronze, silver e gold",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "weather"],
) as dag:

    extract_weather = BashOperator(
        task_id="extract_weather",
        bash_command="cd /opt/airflow && python src/extract_weather.py",
    )

    transform_weather = BashOperator(
        task_id="transform_weather",
        bash_command="cd /opt/airflow && python src/transform_weather.py",
    )

    create_gold_weather = BashOperator(
        task_id="create_gold_weather",
        bash_command="cd /opt/airflow && python src/create_gold_weather.py",
    )

    load_to_s3 = BashOperator(
        task_id="load_to_s3",
        bash_command="cd /opt/airflow && python src/load_to_s3.py",
    )

    extract_weather >> transform_weather >> create_gold_weather >> load_to_s3