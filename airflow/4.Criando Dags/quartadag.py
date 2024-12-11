# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

with  DAG('quarta_dag', description="Quarta DAG",
        schedule_interval=None,start_date=datetime(2023,3,5),
        catchup=False) as dag:

    task1 = BashOperator(task_id="tsk1",bash_command="sleep 5")
    task2 = BashOperator(task_id="tsk2",bash_command="sleep 5")
    task3 = BashOperator(task_id="tsk3",bash_command="sleep 5")

    task1.set_upstream(task2)
    task2.set_upstream(task3)