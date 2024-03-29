import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


def greet():
    print('Writing in file')
    with open('/home/abhishek/airflow_test.txt', 'a+', encoding='utf8') as f:
        now = dt.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        f.write(str(t) + '\n')
    return 'Greeted'

def respond():
    return 'Greet Responded Again'


default_args = {
    'owner': 'airflow',
    'start_date': dt.datetime(2018, 10, 22, 16, 00, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('write_to_file_dag',
         default_args=default_args,
         schedule_interval='*/3 * * * *',
         ) as dag:
    opr_hello = BashOperator(task_id='say_Hi',
                             bash_command='echo "Hi!!"')

    opr_greet = PythonOperator(task_id='greet',
                               python_callable=greet)
    # opr_sleep = BashOperator(task_id='sleep_me',
    #                          bash_command='sleep 1')

    opr_respond = PythonOperator(task_id='respond',
                                 python_callable=respond)
                                 
opr_hello >> opr_greet >> opr_respond