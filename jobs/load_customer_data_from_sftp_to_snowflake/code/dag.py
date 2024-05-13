import os
import sys
import pendulum
from datetime import timedelta
import airflow
from airflow import DAG
from airflow.models.param import Param
from airflow.decorators import task
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from ashishk3s_ashish_prophecy_snowflake_word_count_load_customer_data_from_sftp_to_snowflake.tasks import (
    LoadFileToSnowflake,
    ReadCustomerData,
    SnowflakeModel,
    TableauExtractOperator_1,
    TransferSFTPFileToS3
)
PROPHECY_RELEASE_TAG = "__PROJECT_ID_PLACEHOLDER__/__PROJECT_RELEASE_VERSION_PLACEHOLDER__"

with DAG(
    dag_id = "ashishk3s_ashish_prophecy_snowflake_word_count_load_customer_data_from_sftp_to_snowflake", 
    schedule_interval = "0/5 * * * *", 
    default_args = {"owner" : "Prophecy", "ignore_first_depends_on_past" : True, "do_xcom_push" : True}, 
    start_date = pendulum.today('UTC'), 
    catchup = False, 
    max_active_runs = 1
) as dag:
    ReadCustomerData_op = ReadCustomerData()
    TransferSFTPFileToS3_op = TransferSFTPFileToS3()
    LoadFileToSnowflake_op = LoadFileToSnowflake()
    SnowflakeModel_op = SnowflakeModel()
    TableauExtractOperator_1_op = TableauExtractOperator_1()
    TransferSFTPFileToS3_op >> LoadFileToSnowflake_op
    ReadCustomerData_op >> TransferSFTPFileToS3_op
    LoadFileToSnowflake_op >> SnowflakeModel_op
    SnowflakeModel_op >> TableauExtractOperator_1_op
