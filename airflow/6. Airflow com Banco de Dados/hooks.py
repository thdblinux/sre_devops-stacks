# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook


dag =  DAG('hook', description="hook",
        schedule_interval=None,start_date=datetime(2023,3,5),
        catchup=False)

def create_table():
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    pg_hook.run('create table if not exists teste2(id int);', autocommit=True)

def insert_data():
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    pg_hook.run('insert into teste2 values(1);', autocommit=True)

def select_data(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    records = pg_hook.get_records('select * from teste2;')
    kwargs['ti'].xcom_push(key='query_result', value = records)

def print_data(ti):
    task_instance = ti.xcom_pull(key='query_result', task_ids='select_data_task')
    print("Dados da tabela:")
    for row in task_instance:
        print(row)


create_table_task = PythonOperator(task_id='create_table_task',
                                    python_callable=create_table, dag=dag)

insert_data_task = PythonOperator(task_id='insert_data_task',
                                    python_callable=insert_data, dag=dag)

select_data_task = PythonOperator(task_id='select_data_task',
                                    python_callable=select_data,
                                    provide_context=True,
                                    dag=dag)

print_data_task = PythonOperator(task_id='print_data_task',
                                    python_callable=print_data, 
                                    provide_context=True,
                                    dag=dag)

create_table_task >> insert_data_task >> select_data_task >> print_data_task