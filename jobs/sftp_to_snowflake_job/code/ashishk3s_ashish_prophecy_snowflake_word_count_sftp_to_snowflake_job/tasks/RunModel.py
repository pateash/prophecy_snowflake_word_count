from ashishk3s_ashish_prophecy_snowflake_word_count_sftp_to_snowflake_job.utils import *

def RunModel():
    from airflow.operators.bash import BashOperator
    import os
    import zipfile
    import tempfile

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
           ),            "dbt run --profile run_profile_snowflake -m customers_by_country",            "dbt test --profile run_profile_snowflake -m customers_by_country"]
        ),
        env = {"DBT_DATABRICKS_INVOCATION_ENV" : "prophecy", "DBT_PROFILES_DIR" : "/home/airflow/gcs/data"},
        append_env = True,
    )
