from airflow import models
from airflow.providers.google.cloud.operators.dataflow import DataflowCreatePythonJobOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'start_date': days_ago(1),
    'retry_delay': timedelta(minutes=5),
}

with models.DAG(
    'orchestrator_dataflow_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    kafka_to_gcs = DataflowCreatePythonJobOperator(
        task_id='kafka_to_gcs',
        py_file='gs://air-quality-analysis-data/dataflow/kafka_to_gcs.py',
        job_name='kafka-to-gcs-job',
        options={
            'bootstrap_servers': '34.155.116.106:9092',
            'topic': 'sensor_data',
            'output': 'gs://air-quality-analysis-data/raw/sensor_data',
            'max_records': 10
        },
        location='europe-west9',
        project_id='air-quality-analysis-451718',
        temp_location='gs://air-quality-analysis-data/temp/',
    )

    gcs_to_bigquery = DataflowCreatePythonJobOperator(
        task_id='gcs_to_bigquery',
        py_file='gs://air-quality-analysis-data/dataflow/gcs_to_bigquery.py',
        job_name='gcs-to-bigquery-job',
        options={
            'input': 'gs://air-quality-analysis-data/raw/sensor_data-*.json',
            'output_table': 'air-quality-analysis-451718:processed.sensor_data'
        },
        location='europe-west9',
        project_id='air-quality-analysis-451718',
        temp_location='gs://air-quality-analysis-data/temp/',
    )

    kafka_to_gcs >> gcs_to_bigquery
