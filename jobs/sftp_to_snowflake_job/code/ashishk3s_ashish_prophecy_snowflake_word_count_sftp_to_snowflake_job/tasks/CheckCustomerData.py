from ashishk3s_ashish_prophecy_snowflake_word_count_sftp_to_snowflake_job.utils import *

def CheckCustomerData():
    from airflow.providers.sftp.sensors.sftp import SFTPSensor

    return SFTPSensor(
        task_id = "CheckCustomerData",
        path = "/sftp_user/ashish/customer/customer_data.csv",
        sftp_conn_id = "sftp_ashish",
        poke_interval = 60,
        timeout = 600,
    )
