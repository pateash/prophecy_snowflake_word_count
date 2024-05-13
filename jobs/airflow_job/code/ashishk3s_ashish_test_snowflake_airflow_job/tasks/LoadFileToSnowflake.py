from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def LoadFileToSnowflake():
    # S3ToSnowflakeOperator is deprecated in provider 5.0.0
    from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator

    return CopyFromExternalStageToSnowflakeOperator(
        task_id = "LoadFileToSnowflake",
        files = ["airflow/customer"],  # TODO: make the key a list as well
        file_format = "(type = 'CSV')",
        snowflake_conn_id = "snowflake_ashish",
        table = "customer",
        stage = "ASHISH_S3_STAGE",
        copy_options = "ON_ERROR = 'CONTINUE'"
    )
