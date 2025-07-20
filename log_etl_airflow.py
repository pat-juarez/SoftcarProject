# Import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow.models import DAG
# Operators; you need this to write tasks!
from airflow.operators.bash_operator import BashOperator

# This makes scheduling easy
from airflow.utils.dates import days_ago

# Define the path for the input and output files
mydir = '/home/project/airflow/dags/'
input_file = mydir+'capstone.txt'
extracted_file = mydir+'extract_data.txt'
transformed_file = mydir+'transformed_data.txt'
output_file = mydir+'weblog.tar'

# Default arguments

default_args = {
    'owner': 'Omar Juarez',
    'start_date': days_ago(0),
    'email': ['pat_jualv@ciencias.unam.mx'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
process_web_log = DAG(
    'process_web_log_dag',
    default_args=default_args,
    description='Web logging',
    schedule_interval=timedelta(days=1),
)

# Define the task named execute_extract to call the `extract` function
extract_data = BashOperator(
    task_id='extract',
    bash_command=f'cut -d "-" -f 1 {input_file} > {extracted_file}',
    dag=process_web_log,
)

# Define the task named execute_transform to call the `transform` function
transform_data = BashOperator(
    task_id='transform',
    bash_command=f"grep -v '198.46.149.143' {extracted_file} > {transformed_file}",
    dag=process_web_log,
)

# Define the task named execute_load to call the `load` function
load_data = BashOperator(
    task_id='load',
    bash_command=f"tar -czvf {output_file} {transformed_file}",
    dag=process_web_log,
)

# Task pipeline
extract_data >> transform_data >> load_data