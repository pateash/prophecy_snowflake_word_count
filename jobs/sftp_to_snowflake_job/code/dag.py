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
    CustomerByCountry,
    CustomerData,
    RunModel,
    SFTPToSnowflakeOperator_1
)
PROPHECY_RELEASE_TAG = "__PROJECT_ID_PLACEHOLDER__/__PROJECT_RELEASE_VERSION_PLACEHOLDER__"

with DAG(
    dag_id = "ashishk3s_ashish_prophecy_snowflake_word_count_sftp_to_snowflake_job", 
    schedule_interval = "0 0 * * *", 
    default_args = {"owner" : "Prophecy", "ignore_first_depends_on_past" : True, "do_xcom_push" : True}, 
    params = {
      'SFTP_FILE_PATH': Param(
        """/sftp_user/ashish/customer/customer_data.csv""", 
        type = "string", 
        title = """SFTP_FILE_PATH"""
      ), 
      'CUSTOMER_TABLE': Param("""CUSTOMER_DATA""", type = "string", title = """CUSTOMER_TABLE"""), 
      'CUSTOMER_BY_COUNTRY_TABLE': Param(
        """CUSTOMER_BY_COUNTRY""", 
        type = "string", 
        title = """CUSTOMER_BY_COUNTRY_TABLE"""
      ), 
      'TABLEAU_PROJECT_NAME': Param("""Customers""", type = "string", title = """TABLEAU_PROJECT_NAME""")
    }, 
    start_date = pendulum.today('UTC'), 
    catchup = False, 
    max_active_runs = 1
) as dag:
    CheckCustomerData_op = CheckCustomerData()
    SFTPToSnowflakeOperator_1_op = SFTPToSnowflakeOperator_1()
    RunModel_op = RunModel()
    CustomerByCountry_op = CustomerByCountry()
    CustomerData_op = CustomerData()
    RunModel_op >> CustomerByCountry_op
    SFTPToSnowflakeOperator_1_op >> [CustomerData_op, RunModel_op]
    CheckCustomerData_op >> SFTPToSnowflakeOperator_1_op
