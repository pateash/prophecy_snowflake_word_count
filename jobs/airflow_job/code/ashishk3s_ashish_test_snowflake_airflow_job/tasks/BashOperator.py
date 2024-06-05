from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def BashOperator():
    from airflow.operators.bash import BashOperator

    return BashOperator(task_id = "BashOperator", bash_command = "echo \"hello world\"", )
