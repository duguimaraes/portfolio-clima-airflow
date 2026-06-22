from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="capital_weather_pipeline",
    description="Pipeline de previsoes para as capitais brasileiras",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "weather", "capitals"],
) as dag:
    extract_capitals_weather = BashOperator(
        task_id="extract_capitals_weather",
        bash_command="cd /opt/airflow && python src/extract_capitals_weather.py",
    )

    transform_capitals_weather = BashOperator(
        task_id="transform_capitals_weather",
        bash_command="cd /opt/airflow && python src/transform_capitals_weather.py",
    )

    create_capitals_gold = BashOperator(
        task_id="create_capitals_gold",
        bash_command="cd /opt/airflow && python src/create_capitals_gold.py",
    )

    load_capitals_to_s3 = BashOperator(
        task_id="load_capitals_to_s3",
        bash_command="cd /opt/airflow && python src/load_capitals_to_s3.py",
    )

    (
        extract_capitals_weather
        >> transform_capitals_weather
        >> create_capitals_gold
        >> load_capitals_to_s3
    )