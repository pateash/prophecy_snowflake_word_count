from ashishk3s_ashish_prophecy_snowflake_word_count_load_customer_data_from_sftp_to_snowflake.utils import *

def TransferSFTPFileToS3():
    from airflow.providers.amazon.aws.transfers.sftp_to_s3 import SFTPToS3Operator

    return SFTPToS3Operator(
        task_id = "TransferSFTPFileToS3",
        sftp_conn_id = "sftp_ashish",
        sftp_path = "/sftp_user/ashish/customer/customer_data.csv",
        s3_key = "airflow/customer_data.csv",
        s3_bucket = "ashishpatel-prophecy-test",
        s3_conn_id = "aws_default",
        use_temp_file = True,
        do_xcom_push = True
    )
