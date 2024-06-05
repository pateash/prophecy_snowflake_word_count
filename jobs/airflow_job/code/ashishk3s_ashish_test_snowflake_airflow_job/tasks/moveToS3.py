from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def moveToS3():
    from airflow.providers.amazon.aws.transfers.sftp_to_s3 import SFTPToS3Operator

    return SFTPToS3Operator(
        task_id = "moveToS3",
        sftp_conn_id = "sftp_ashish",
        sftp_path = "/sftp_user/ashish/customer/customer_data.csv",
        s3_key = "airflow/customer_data.csv",
        s3_bucket = "ashishpatel-prophecy-test",
        s3_conn_id = "aws_default",
        use_temp_file = True,
        email_on_retry = False, 
        trigger_rule = "all_success"
    )
