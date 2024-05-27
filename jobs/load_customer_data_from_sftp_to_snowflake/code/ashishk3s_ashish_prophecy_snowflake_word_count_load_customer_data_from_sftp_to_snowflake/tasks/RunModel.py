from ashishk3s_ashish_prophecy_snowflake_word_count_load_customer_data_from_sftp_to_snowflake.utils import *

def RunModel():
    from airflow.operators.bash import BashOperator
    import os
    import zipfile
    import tempfile
    envs = {"DBT_DATABRICKS_INVOCATION_ENV" : "prophecy"}
    dbt_props_cmd = ""

    if "/home/airflow/gcs/data":
        envs = {"DBT_DATABRICKS_INVOCATION_ENV" : "prophecy", "DBT_PROFILES_DIR" : "/home/airflow/gcs/data"}

    if "run_profile_snowflake":
        dbt_props_cmd = " --profile run_profile_snowflake"

    if "customers_by_country":
        dbt_props_cmd = dbt_props_cmd + " -m " + "customers_by_country"

    return BashOperator(
        task_id = "RunModel",
        bash_command = " && ".join(
          ["{} && cd $tmpDir/{}".format(
             (
               "set -euxo pipefail && tmpDir=`mktemp -d` && git clone "
               + "--depth 1 {} --branch {} $tmpDir".format(
                 "https://github.com/pateash/prophecy_snowflake_word_count",
                 "__PROJECT_FULL_RELEASE_TAG_PLACEHOLDER__"
               )
             ),
             ""
           ),            "dbt run" + dbt_props_cmd,  "dbt test" + dbt_props_cmd]
        ),
        env = envs,
        append_env = True,
    )
