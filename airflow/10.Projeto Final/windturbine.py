# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import json
import os

default_args = {
        'depends_on_past' : False,
        'email' : ['aws@evoluth.com.br'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries' : 1,
        'retry_delay' : timedelta(seconds=10)
        }

#schedule_interval="*/3 * * * * "
dag = DAG('windturbine', description='Dados da Turbina',
          schedule_interval=None, start_date=datetime(2023,3,5),
          catchup=False, default_args=default_args, default_view='graph',
          doc_md="## Dag para registrar dados de turbina eólica")

group_check_temp = TaskGroup("group_check_temp", dag=dag)
group_database = TaskGroup('group_database', dag=dag)

file_sensor_task = FileSensor(
        task_id = 'file_sensor_task',
        filepath = Variable.get('path_file'),
        fs_conn_id = 'fs_default',
        poke_interval = 10,
        dag = dag)

def process_file(**kwarg):
    with open(Variable.get('path_file')) as f:
        data = json.load(f)
        kwarg['ti'].xcom_push(key='idtemp',value=data['idtemp'])
        kwarg['ti'].xcom_push(key='powerfactor',value=data['powerfactor'])
        kwarg['ti'].xcom_push(key='hydraulicpressure',value=data['hydraulicpressure'])
        kwarg['ti'].xcom_push(key='temperature',value=data['temperature'])
        kwarg['ti'].xcom_push(key='timestamp',value=data['timestamp'])
    os.remove(Variable.get('path_file'))

get_data = PythonOperator(
            task_id = 'get_data',
            python_callable= process_file, 
            provide_context = True,
            dag=dag)

create_table = PostgresOperator(task_id="create_table",
                                postgres_conn_id='postgres',
                                sql='''create table if not exists
                                sensors (idtemp varchar, powerfactor varchar,
                                hydraulicpressure varchar, temperature varchar,
                                timestamp varchar);
                                ''',
                                task_group=group_database,
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data',
                               postgres_conn_id='postgres',
                               parameters=(
                               '{{ ti.xcom_pull(task_ids="get_data",key="idtemp") }}',     
                               '{{ ti.xcom_pull(task_ids="get_data",key="powerfactor") }}',     
                               '{{ ti.xcom_pull(task_ids="get_data",key="hydraulicpressure") }}',     
                               '{{ ti.xcom_pull(task_ids="get_data",key="temperature") }}',     
                               '{{ ti.xcom_pull(task_ids="get_data",key="timestamp") }}'                                                                               
                               ),
                               sql = '''INSERT INTO sensors (idtemp, powerfactor,
                               hydraulicpressure, temperature, timestamp)
                               VALUES (%s, %s, %s, %s, %s);''',
                               task_group = group_database,
                               dag=dag
                               )

send_email_alert = EmailOperator(
                                task_id='send_email_alert',
                                to='aws@evoluth.com.br',
                                subject='Airlfow alert',
                                html_content = '''<h3>Alerta de Temperatrura. </h3>
                                <p> Dag: windturbine </p>
                                ''',
                                task_group = group_check_temp,
                                dag=dag)

send_email_normal = EmailOperator(
                                task_id='send_email_normal',
                                to='aws@evoluth.com.br',
                                subject='Airlfow advise',
                                html_content = '''<h3>Temperaturas normais. </h3>
                                <p> Dag: windturbine </p>
                                ''',
                                task_group = group_check_temp,
                                dag=dag)

def avalia_temp(**context):
    number = float( context['ti'].xcom_pull(task_ids='get_data', key="temperature"))
    if number >= 24 :
        return 'group_check_temp.send_email_alert'
    else:
        return 'group_check_temp.send_email_normal'
        
                        

check_temp_branc = BranchPythonOperator(
                                task_id = 'check_temp_branc',
                                python_callable=avalia_temp,
                                provide_context = True,
                                dag = dag,
                                task_group = group_check_temp)

with group_check_temp:
    check_temp_branc >> [send_email_alert, send_email_normal]

with group_database:
    create_table >> insert_data


file_sensor_task >> get_data
get_data >> group_check_temp
get_data >> group_database

