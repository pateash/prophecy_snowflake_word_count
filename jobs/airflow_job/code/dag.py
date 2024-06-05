import os
import sys
import pendulum
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.models.param import Param
from airflow.decorators import task
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from ashishk3s_ashish_test_snowflake_airflow_job.tasks import BashOperator, CheckCustomerData, Python_1, moveToS3
PROPHECY_RELEASE_TAG = "__PROJECT_ID_PLACEHOLDER__/__PROJECT_RELEASE_VERSION_PLACEHOLDER__"

with DAG(
    dag_id = "ashishk3s_ashish_test_snowflake_airflow_job", 
    schedule_interval = "0 0 * * *", 
    default_args = {"owner" : "Prophecy", "ignore_first_depends_on_past" : True, "do_xcom_push" : True}, 
    params = {'SFTP_PATH' : Param("""/sftp_user/ashish/customer/customer_data.csv""", type = "string", title = """SFTP_PATH""")}, 
    start_date = pendulum.today('UTC'), 
    catchup = False, 
    max_active_runs = 1
) as dag:
    CheckCustomerData_op = CheckCustomerData()
    moveToS3_op = moveToS3()
    BashOperator_op = BashOperator()
    Python_1_op = Python_1()
    CheckCustomerData_op >> moveToS3_op
    moveToS3_op >> [BashOperator_op, Python_1_op]
