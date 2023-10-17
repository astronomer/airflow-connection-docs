
### Module - MSSQL (SQLServer or AzureDB) Connection + Operators

**Before you Start**

- Have an existing MSSQL Database with data
- Ensure that your Astronomer Cloud cluster has network access to the existing Database
- Have access to existing MSSQL User Credentials

**Add MSSQL Provider and Packages**

- [ ]  Add `apache-airflow-providers-microsoft-mssql` to your project’s `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-microsoft-mssql
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that MSSQL provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create Connection and Test with DAG**

- [ ]  Create a connection in one of the following ways:
    - Add a MSSQL Connection in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

        ```bash
        export AIRFLOW_CONN_MSSQL_DEFAULT=mssql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<SCHEMA>
        ```

    - **OR** go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`mssql_default`), select `MySQL` as a connection type, and fill in the following fields (leave all other fields as their default value or blank):

        ```yaml
        Connection Id: mssql_default
        Connection Type: mssql
        Host: <HOST>
        Schema: <Schema>
        Login: <USERNAME>
        Password: <PASSWORD>
        Port: <PORT>
        ```

    - For more information on MSSQL connection in Airflow, be sure to review the Airflow OSS documentation

        [MSSQL Connection - apache-airflow-providers-microsoft-mssql Documentation](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/connections/mssql.html)

- [ ]  Create a file called `dags/example_mssql.py` or something similar, with the contents:

    ```python
    from datetime import datetime
    from airflow import DAG
    from airflow.providers.microsoft.mssql.operators.mssql import MsSqlOperator

    with DAG(
        dag_id="example_mssql",
        start_date=datetime(2021, 1, 1),
        schedule=None
    ) as dag:
        MsSqlOperator(
    				mssql_conn_id="mssql_default",
            sql="SELECT 1;",
            task_id="example_mssql",
        )
    ```


**Checkpoint**

You now have tested a functioning MsSql connection in Airflow, and have utilized the `MsSqlOperator`

**Next Steps**

- Integrate the new Airflow Connection with your Use Case Workload
- [Review other MsSql Operators](https://registry.astronomer.io/providers/mssql) in the Astronomer Registry

**Extras / Reference**

- [MSSQL Connection](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-mssql/stable/connections/mssql.html)
