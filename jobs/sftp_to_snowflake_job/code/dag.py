import os
import sys
import pendulum
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.models.param import Param
from airflow.decorators import task
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from ashishk3s_ashish_prophecy_snowflake_word_count_sftp_to_snowflake_job.tasks import (
    CheckCustomerData,
    CreateCustomerTable,
    CustomerByCountryExtract,
    CustomerDataExtract,
    RunModel
)
PROPHECY_RELEASE_TAG = "__PROJECT_ID_PLACEHOLDER__/__PROJECT_RELEASE_VERSION_PLACEHOLDER__"

with DAG(
    dag_id = "ashishk3s_ashish_prophecy_snowflake_word_count_sftp_to_snowflake_job", 
    schedule_interval = "0 0 * * *", 
    default_args = {"owner" : "Prophecy", "ignore_first_depends_on_past" : True, "do_xcom_push" : True}, 
    start_date = pendulum.today('UTC'), 
    catchup = False, 
    max_active_runs = 1
) as dag:
    CheckCustomerData_op = CheckCustomerData()
    CreateCustomerTable_op = CreateCustomerTable()
    CustomerDataExtract_op = CustomerDataExtract()
    RunModel_op = RunModel()
    CustomerByCountryExtract_op = CustomerByCountryExtract()
    CheckCustomerData_op >> CreateCustomerTable_op
    CreateCustomerTable_op >> [CustomerDataExtract_op, RunModel_op]
    CustomerDataExtract_op >> RunModel_op
    RunModel_op >> CustomerByCountryExtract_op
