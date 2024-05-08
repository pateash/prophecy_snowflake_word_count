from ashishk3s_ashish_test_snowflake_airflow_job.utils import *

def Python_1():

    def test_tableau():
        from pathlib import Path
        import tableauserverclient as TSC
        from tableauhyperapi import (
            HyperProcess,
            Telemetry,  \
            Connection,
            CreateMode,  \
            NOT_NULLABLE,
            NULLABLE,
            SqlType,
            TableDefinition,  \
            Inserter,  \
            escape_name,
            escape_string_literal,  \
            TableName,  \
            HyperException
        )
        from airflow.providers.tableau.hooks.tableau import TableauHook
        # Configure for TSC to publish
        # Note: Do not store creds/tokens in plaintext, please use env vars :)
        # from properties
        hyper_name = 'customer.hyper'
        site_name = 'ashish0b1f0348d6'
        # from connection
        server_address = 'https://prod-apnortheast-a.online.tableau.com/'
        project_name = 'Samples'
        # For more on tokens, head here:
        # https://help.tableau.com/current/server/en-us/security_personal_access_tokens.htm
        path_to_database = Path('customer.hyper')
        # The table is called "Extract" and will be created in the "Extract" schema
        # and contains four columns.
        extract_table = TableDefinition(
            table_name = TableName("Extract", "Extract"),
            columns = [TableDefinition.Column(name = 'Customer ID', type = SqlType.text(), nullability = NOT_NULLABLE),
             TableDefinition.Column(name = 'Customer Name', type = SqlType.text(), nullability = NOT_NULLABLE),
             TableDefinition.Column(
               name = 'Loyalty Reward Points',
               type = SqlType.big_int(),
               nullability = NOT_NULLABLE
             ),
             TableDefinition.Column(name = 'Segment', type = SqlType.text(), nullability = NOT_NULLABLE)]
        )

        def insert_data():
            """
        An example demonstrating a simple single-table Hyper file including table creation and data insertion with different types
        This code is lifted from the below example:
        https://github.com/tableau/hyper-api-samples/blob/main/Tableau-Supported/Python/insert_data_into_single_table.py
        """
            print("Creating single table for publishing.")

            # Starts the Hyper Process with telemetry enabled to send data to Tableau.
            # To opt out, simply set telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU.
            with HyperProcess(telemetry = Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:

                # Creates new Hyper file "customer.hyper".
                # Replaces file with CreateMode.CREATE_AND_REPLACE if it already exists.
                with Connection(
                    endpoint = hyper.endpoint,
                    database = path_to_database,
                    create_mode = CreateMode.CREATE_AND_REPLACE
                ) as connection:
                    connection.catalog.create_schema(schema = extract_table.table_name.schema_name)
                    connection.catalog.create_table(table_definition = extract_table)
                    # The rows to insert into the "Extract"."Extract" table.
                    data_to_insert = [["DK-13375", "Dennis Kane", 685, "Consumer"],
                                      ["EB-13705", "Ed Braxton", 815, "Corporate"]]

                    with Inserter(connection, extract_table) as inserter:
                        inserter.add_rows(
                            rows = [["DK-13375", "Dennis Kane", 685, "Consumer"], ["EB-13705", "Ed Braxton", 815, "Corporate"]]
                        )
                        inserter.execute()

                    # The table names in the "Extract" schema (the default schema).
                    table_names = connection.catalog.get_table_names("Extract")
                    print(
                        "Tables available in {} are: {}".format(
                          path_to_database, 
                          connection.catalog.get_table_names("Extract")
                        )
                    )
                    # Number of rows in the "Extract"."Extract" table.
                    # `execute_scalar_query` is for executing a query that returns exactly one row with one column.
                    row_count = connection.execute_scalar_query(
                        query = f"SELECT COUNT(*) FROM {extract_table.table_name}"
                    )
                    print(
                        "The number of rows in table {} is {}.".format(
                          extract_table.table_name, 
                          connection.execute_scalar_query(query = f"SELECT COUNT(*) FROM {extract_table.table_name}")
                        )
                    )

                print("The connection to the Hyper file has been closed.")

            print("The Hyper process has been shut down.")

        def publish_hyper():
            """
        Shows how to leverage the Tableau Server Client (TSC) to sign in and publish an extract directly to Tableau Online/Server
        """

            # Sign in to server
            # tableau_auth = TSC.PersonalAccessTokenAuth('token', '3pHW1FGfREqgrkktd6y0MA==:Aqnk7VGoWtWSOXQIOrrrDx8iSFu4ihEP', site_id=site_name)
            # server = TSC.Server(server_address, use_server_version=False)
            with TableauHook(site_id = site_name, tableau_conn_id = 'tableau') as hook:
                print(f"Signing into {site_name} at {server_address}")
                # Define publish mode - Overwrite, Append, or CreateNew
                publish_mode = TSC.Server.PublishMode.Overwrite
                p = hook.get_all('projects')
                print(hook.get_all('projects'))

                # Get project_id from project_name
                for project in hook.get_all('projects'):
                    if project.name == project_name:
                        project_id = project.id

                # Create the datasource object with the project_id
                datasource = TSC.DatasourceItem(project_id = project_id, name = 'customer2')
                print(f"Publishing {hyper_name} to {project_name}...")
                # Publish datasource
                datasource = hook.server.datasources.publish(
                    TSC.DatasourceItem(project_id = project_id, name = 'customer2'),
                    path_to_database,
                    TSC.Server.PublishMode.Overwrite
                )
                print(
                    "Datasource published. Datasource ID: {0}".format(
                      hook.server.datasources.publish(
                        TSC.DatasourceItem(project_id = project_id, name = 'customer2'),
                        path_to_database,
                        TSC.Server.PublishMode.Overwrite
                      )\
                        .id
                    )
                )

        insert_data()
        publish_hyper()

    import json
    from datetime import timedelta
    from airflow.operators.python import PythonOperator

    return PythonOperator(task_id = "Python_1", python_callable = test_tableau, show_return_value_in_logs = True)
