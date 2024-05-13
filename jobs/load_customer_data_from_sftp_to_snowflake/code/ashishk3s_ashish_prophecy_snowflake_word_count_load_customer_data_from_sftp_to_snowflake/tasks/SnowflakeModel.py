from ashishk3s_ashish_prophecy_snowflake_word_count_load_customer_data_from_sftp_to_snowflake.utils import *

def SnowflakeModel():
    from datetime import timedelta
    from airflow.operators.bash import BashOperator
    envs = {}
    dbt_props_cmd = ""

    if "/home/airflow/gcs/data":
        envs = {"DBT_PROFILES_DIR" : "/home/airflow/gcs/data"}

    if "run_profile_snowflake":
        dbt_props_cmd = " --profile run_profile_snowflake"

    if "word_count":
        dbt_props_cmd = dbt_props_cmd + " -m " + "word_count"

    return BashOperator(
        task_id = "SnowflakeModel",
        bash_command = " && ".join(
          ["{} && cd $tmpDir/{}".format(
             (
               "set -euxo pipefail && tmpDir=`mktemp -d` && git clone "
               + "{} --branch {} --single-branch $tmpDir".format(
                 "https://github.com/pateash/prophecy_snowflake_word_count",
                 "dev"
               )
             ),
             ""
           ),            "dbt run" + dbt_props_cmd,  "dbt test" + dbt_props_cmd]
        ),
        env = envs,
        append_env = True,
    )