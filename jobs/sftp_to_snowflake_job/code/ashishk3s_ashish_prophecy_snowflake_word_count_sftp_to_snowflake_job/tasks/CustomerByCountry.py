from ashishk3s_ashish_prophecy_snowflake_word_count_sftp_to_snowflake_job.utils import *

def CustomerByCountry():
    from typing import Optional, List, Dict
    from dataclasses import dataclass, field
    from abc import ABC


    @dataclass(frozen = True)
    class TableauExtractProperties():
        taskId: Optional[str] = None
        snowflake_conn_id: Optional[str] = "snowflake_default"
        snowflake_table: Optional[str] = None
        tableau_conn_id: Optional[str] = "tableau_default"
        tableau_project_name: Optional[str] = None
        hyper_name: Optional[str] = None

    props = TableauExtractProperties(  #skiptraversal
        taskId = "CustomerByCountry", 
        snowflake_conn_id = "snowflake_CICD_253", 
        snowflake_table = "CUSTOMERS_BY_COUNTRY", 
        tableau_conn_id = "tableau_ashish", 
        tableau_project_name = "Samples", 
        hyper_name = "CUSTOMERS_BY_COUNTRY"
    )
    settings = {}
    from airflow.operators.python import PythonOperator
    from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
    from airflow.hooks.base import BaseHook
    import pandas as pd
    import pantab
    import tableauserverclient as TSC
    tableau_conn_id = props.tableau_conn_id
    project_name = props.tableau_project_name
    hyper_path = f"{props.hyper_name}.hyper"
    table_name = 'Extract' # TODO: this can be handled internally
    # snowflake
    snowflake_conn_id = props.snowflake_conn_id
    # Snowflake connection using Airflow Snowflake Hook
    # sql_query = f"SELECT * FROM {self.props.snowflake_schema}.{self.props.snowflake_table}"
    sql_query = f"SELECT * FROM {props.snowflake_table}"

    def export_tableau_hyperfile():
        # tableau
        snowflake_hook = SnowflakeHook(snowflake_conn_id)
        connection = snowflake_hook.get_conn()
        cursor = connection.cursor()

        # Fetch data from Snowflake into a pandas DataFrame
        try:
            # Execute the query
            cursor.execute(sql_query)
            results = cursor.fetchall()

            if results:
                df = pd.DataFrame(results, columns = [col[0] for col in cursor.description])
                print("Data fetched successfully from Snowflake.")
                # Specify the path for the Hyper file
                pantab.frame_to_hyper(df, hyper_path, table = table_name)
                print(f"Data written to Hyper file successfully at {hyper_path}.")
            else:
                print("Query returned no data.")
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
            raise 

        # Get Tableau details from Airflow connection
        tableau_conn = BaseHook.get_connection(tableau_conn_id)
        # Tableau authentication ( using Username/Password )
        # tableau_auth = TSC.TableauAuth(tableau_conn.login, tableau_conn.password,
        #                                site_id=tableau_conn.extra_dejson.get('site_id'))
        # Using Personal Access Token
        tableau_auth = TSC.PersonalAccessTokenAuth(
            tableau_conn.extra_dejson.get('token_name'),
            tableau_conn.extra_dejson.get('personal_access_token'),
            site_id = tableau_conn.extra_dejson.get('site_id')
        )
        server = TSC.Server(tableau_conn.host, use_server_version = True)

        with server.auth.sign_in(tableau_auth):
            all_projects = TSC.Pager(server.projects.get)
            project = [project for project in all_projects if project.name == project_name][0]
            print("Writing into project: " + str(project.name))
            # Publish Hyper file to Tableau Server
            new_datasource_item = TSC.DatasourceItem(project.id)
            datasource = server.datasources.publish(new_datasource_item, hyper_path, 'Overwrite')
            print("Datasource published. ID: ", datasource.id)

    return PythonOperator(task_id = props.taskId, python_callable = export_tableau_hyperfile, **settings)
