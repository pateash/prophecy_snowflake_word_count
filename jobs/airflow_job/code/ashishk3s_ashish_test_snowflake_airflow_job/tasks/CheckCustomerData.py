from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def CheckCustomerData():
    from airflow.providers.sftp.sensors.sftp import SFTPSensor

    return SFTPSensor(
        task_id = "CheckCustomerData",
        path = "/sftp_user/ashish/customer/customer_data.csv",
        sftp_conn_id = "sftp_ashish",
        poke_interval = 60,
        timeout = 600,
    )
