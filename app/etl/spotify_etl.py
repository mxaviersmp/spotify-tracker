import os
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from app.etl.tasks import (
    run_get_artist_info,
    run_get_played_tracks,
    run_get_track_info,
    run_update_access_tokens,
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': [os.getenv('EMAIL')],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'spotify_etl',
    default_args=default_args,
    description='DAG to update db',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['spotify'],
)

t1 = PythonOperator(
    task_id='update_access_tokens',
    python_callable=run_update_access_tokens,
    dag=dag
)

t2 = PythonOperator(
    task_id='get_played_tracks',
    python_callable=run_get_played_tracks,
    dag=dag
)
t3 = PythonOperator(
    task_id='get_track_info',
    python_callable=run_get_track_info,
    dag=dag
)
t4 = PythonOperator(
    task_id='get_artist_info',
    python_callable=run_get_artist_info,
    dag=dag
)

t1 >> t2 >> [t3, t4]
