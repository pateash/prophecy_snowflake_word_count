from ashishk3s_ashish_prophecy_snowflake_word_count_load_customer_data_from_sftp_to_snowflake.utils import *

def LoadFileToSnowflake():
    # S3ToSnowflakeOperator is deprecated in provider 5.0.0
    from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator

    return CopyFromExternalStageToSnowflakeOperator(
        task_id = "LoadFileToSnowflake",
        files = ["airflow/customer_data.csv"],  # TODO: make the key a list as well
        file_format = "(type = 'CSV')",
        snowflake_conn_id = "snowflake_ashish",
        table = "CUSTOMER_DATA",
        stage = "ASHISH_S3_STAGE",
        copy_options = "ON_ERROR = 'CONTINUE'"
    )
