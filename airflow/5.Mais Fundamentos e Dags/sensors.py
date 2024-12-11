# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.http.sensors.http import HttpSensor
import requests

dag =  DAG('httpsensor', description="httpsensor",
        schedule_interval=None,start_date=datetime(2023,3,5),
        catchup=False)

def query_api():
    response = requests.get("https://api.publicapis.org/entries")
    print(response.text)

check_api = HttpSensor(task_id="check_api",
            http_conn_id='connection',
            endpoint='entries',
            poke_interval=5,
            timeout=20,
            dag=dag)
process_data = PythonOperator(task_id="process_data", python_callable=query_api, dag=dag)

check_api >> process_data