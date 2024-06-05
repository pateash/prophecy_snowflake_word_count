from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def Python_1():

    def hello():
        return "Hello Ashish"

    import json
    from datetime import timedelta
    from airflow.operators.python import PythonOperator

    return PythonOperator(task_id = "Python_1", python_callable = hello, show_return_value_in_logs = True)
