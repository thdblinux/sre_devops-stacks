# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past' : False,
    'start_date': datetime(2023,3,5),
    'email' : ['aws@evoluth.com.br'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

dag =  DAG('email_test', description="Email",
        default_args = default_args, 
        schedule_interval=None,
        catchup=False, default_view='graph', tags=['processo','tag','pipeline'])

task1 = BashOperator(task_id="tsk1",bash_command="sleep 1",dag=dag )
task2 = BashOperator(task_id="tsk2",bash_command="sleep 1",dag=dag )
task3 = BashOperator(task_id="tsk3",bash_command="sleep 1",dag=dag )
task4 = BashOperator(task_id="tsk4",bash_command="exit 1",dag=dag )
task5 = BashOperator(task_id="tsk5",bash_command="sleep 1",dag=dag, trigger_rule='none_failed' )
task6 = BashOperator(task_id="tsk6",bash_command="sleep 1",dag=dag, trigger_rule='none_failed' )

send_email = EmailOperator(task_id="send_email",
                to="aws@evoluth.com.br",
                subject="Airflow Error",
                html_content="""<h3>Ocorreu um erro na Dag. </h3>
                                <p>Dag: send_email </p>  
                                """,
                dag=dag, trigger_rule="one_failed")

[task1,task2] >> task3 >> task4
task4 >> [task5,task6, send_email]