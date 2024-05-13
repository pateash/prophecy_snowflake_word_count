from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def ReadCustomerData():
    from airflow.providers.sftp.sensors.sftp import SFTPSensor

    return SFTPSensor(
        task_id = "ReadCustomerData",
        path = "/sftp_user/ashish/customer",
        file_pattern = "customer_data_*.csv",
        sftp_conn_id = "sftp_ashish",
        poke_interval = 60,
        timeout = 600,
    )
