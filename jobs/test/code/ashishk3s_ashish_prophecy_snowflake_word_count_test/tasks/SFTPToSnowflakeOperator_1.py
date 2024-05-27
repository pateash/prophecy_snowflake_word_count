from ashishk3s_ashish_prophecy_snowflake_word_count_test.utils import *

def SFTPToSnowflakeOperator_1():
    from typing import Optional, List, Dict
    from dataclasses import dataclass, field
    from abc import ABC


    @dataclass(frozen = True)
    class SFTPToSnowflakeProperties():
        taskId: Optional[str] = None
        snowflake_conn_id: Optional[str] = None
        snowflake_table: Optional[str] = None
        write_mode: str = "OVERWRITE"
        sftp_conn_id: Optional[str] = None
        sftp_file_path: Optional[str] = None
        sftp_operation: str = "put"
        file_format: str = "CSV"
        # format specific
        csv_field_delimiter: str = ","
        csv_header_settings: str = "DEFAULT"

    props = SFTPToSnowflakeProperties(  #skiptraversal
        taskId = "SFTPToSnowflakeOperator_1", 
        snowflake_conn_id = "snowflake_CICD_253", 
        snowflake_table = "CUSTOMER_DATA", 
        write_mode = "APPEND", 
        sftp_conn_id = "sftp_ashish", 
        sftp_file_path = "{{ params.SFTP_FILE_PATH }}", 
        sftp_operation = "put", 
        file_format = "CSV", 
        csv_field_delimiter = ",", 
        csv_header_settings = "PARSE_HEADER"
    )
    settings = {}
    from airflow.operators.python import PythonOperator
    from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
    from airflow.providers.sftp.hooks.sftp import SFTPHook
    from pathlib import Path
    import datetime
    import os
    # sftp
    sftp_conn_id = props.sftp_conn_id
    sftp_file_path = props.sftp_file_path
    file_name = f"{os.path.basename(sftp_file_path)}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    local_file_path = f"/tmp/{file_name}" # download file to this path locally
    file_format = props.file_format
    # snowflake
    stage_name = "PROPHECY_AIRFLOW_SNOWFLAKE_TEMP_STAGE"
    format_name = "PROPHECY_AIRFLOW_SNOWFLAKE_TEMP_FORMAT"
    snowflake_file_path = f"@{stage_name}/{file_name}"
    table_name = props.snowflake_table
    snowflake_conn_id = props.snowflake_conn_id
    write_mode = props.write_mode
    # file props
    csv_field_delimiter = props.csv_field_delimiter

    if props.csv_header_settings == 'PARSE_HEADER':
        csv_header_settings = 'PARSE_HEADER = TRUE'
    elif props.csv_header_settings == 'SKIP_HEADER':
        csv_header_settings = 'SKIP_HEADER = 1'
    else:
        csv_header_settings = ''

    def run_query(cursor, query):
        print("Running: ", query)
        cursor.execute(query)
        output = cursor.fetchall()

        for row in output:
            print(row)

        print("=" * 20)

    def download_data():
        sftp_hook = SFTPHook(ssh_conn_id = sftp_conn_id)
        local_folder = os.path.dirname(local_file_path)
        Path(local_folder).mkdir(parents = True, exist_ok = True)
        file_msg = f"downloading file from {sftp_file_path} to {local_file_path}"
        print("Starting to transfer %s", file_msg)
        sftp_hook.retrieve_file(sftp_file_path, local_file_path)
        print("Transfer complete")

    def upload_data():
        # csv properties
        queries = {
            "create_stage": f"CREATE  TEMPORARY  STAGE IF NOT EXISTS {stage_name} ",
            "copy_file": f"PUT file://{local_file_path} {snowflake_file_path}",
            "create_file_format": f"CREATE TEMPORARY FILE FORMAT {format_name} TYPE = {file_format} FIELD_DELIMITER = '{csv_field_delimiter}' {csv_header_settings}",
            "delete_table": f"""DROP TABLE IF EXISTS {table_name}""",
            "truncate_table": f"""TRUNCATE TABLE IF EXISTS {table_name}""",
            "create_table": f"""CREATE TABLE IF NOT EXISTS {table_name}
                                  USING TEMPLATE (
                                    SELECT ARRAY_AGG(OBJECT_CONSTRUCT('COLUMN_NAME',COLUMN_NAME, 'TYPE',TYPE, 'NULLABLE', NULLABLE, 'EXPRESSION',EXPRESSION))
                                    FROM TABLE(
                                      INFER_SCHEMA(
                                        LOCATION=>'{snowflake_file_path}',
                                        FILE_FORMAT=>'{format_name}'
                                      )
                                    )
                                  )""",
            "copy_data_to_table": f"""COPY INTO {table_name}
                        FROM {snowflake_file_path}
                        FILE_FORMAT = (FORMAT_NAME = '{format_name}')
                        {'MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE' if csv_header_settings == 'PARSE_HEADER = TRUE' else ''}""",
            "get_data": f"""SELECT * from {table_name}"""
        }
        snowflake_hook = SnowflakeHook(snowflake_conn_id)
        conn = snowflake_hook.get_conn()
        cur = conn.cursor()

        try:
            # creating a temporary stage
            run_query(cur, queries["create_stage"])
            # creating a temporary file format
            run_query(cur, queries["create_file_format"])
            # copy file from local to snowflake
            run_query(cur, queries["copy_file"])
            # create table if not exists
            run_query(cur, queries["create_table"])

            if write_mode == "OVERWRITE":  # truncate table
                run_query(cur, queries["truncate_table"])

            # copy data from stage to table
            run_query(cur, queries["copy_data_to_table"])
            # show data
            run_query(cur, queries["get_data"])
        except Exception as e:
            print("Exception occurred: ", e)
            raise e
        finally:
            # Close the cursor and connection
            cur.close()
            conn.close()

    def execute():
        download_data()
        upload_data()

    return PythonOperator(task_id = props.taskId, python_callable = execute, **settings)
