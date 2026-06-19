FROM apache/airflow:2.10.4

RUN pip install --no-cache-dir boto3==1.43.34