
### Module - Postgres Connection + Operators

**Before you start:**

- Have an existing Postgres Database with data
- Ensure that your Astronomer Cloud cluster has network access to the existing Database
- Have a Postgres User with existing Credentials

**Create Connection and Test with DAG**

- [ ]  Create a connection in one of the following ways:
    - Add a Postgres Connection in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

        ```bash
        export AIRFLOW_CONN_POSTGRES_DEFAULT=postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<SCHEMA>
        ```

    - **OR** go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`postgres_default`), select `Postgres` as a connection type, and fill in the following fields (leave all other fields as their default value or blank):

        ```yaml
        Connection Id: postgres_default
        Connection Type: Postgres
        Host: <HOST>
        Schema: <Schema>
        Login: <USERNAME>
        Password: <PASSWORD>
        Port: <PORT>
        ```

    - For more information on Postgres connection in Airflow, be sure to review the Airflow OSS documentation

        [PostgreSQL Connection - apache-airflow-providers-postgres Documentation](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/connections/postgres.html)


**Add the example DAG to your project:**

- [ ]  Create the following as `dags/example_postgres.py` and run the DAG in the Airflow UI locally and in Astronomer Cloud

    ```python
    from datetime import datetime
    from airflow import DAG
    from airflow.providers.postgres.operators.postgres import PostgresOperator

    with DAG(
        dag_id="example_postgres",
        schedule=None,
        start_date=datetime(2022, 1, 1)
    ) as dag:
        PostgresOperator(
            task_id="test_postgres",
            postgres_conn_id="postgres_default",
            sql="SELECT 1;"
        )
    ```


**Checkpoint:**

You have now tested a functioning `Postgres` connection in Airflow and have utilized the `PostgresOperator`.

**Next Steps:**

- [ ]  Implement `PostgresOperator` or `PostgresHook` into your workflows.

**Extras / Reference**

- In addition to the `PostgresOperator`, take a look at the `PostgresHook` linked below for additional options for interacting with your newly created Postgres connection.
- Learn how [Templating](https://www.astronomer.io/guides/templating/) and [XComs](https://airflow.apache.org/docs/apache-airflow/stable/concepts/xcoms.html) can be added to your tasks and queries to provide additional flexibility and make your queries more dynamic.
- Learn how to separate your `.sql` files in order to keep your DAGs short and concise. (For example, using template_searchpath in your DAG definition

    ```python
    with DAG(..., template_searchpath="/include/folder/with/sql/files/") as dag:
    ```

- Reference


    - [PostgresOperator | Astronomer Registry](https://registry.astronomer.io/providers/postgres/modules/postgresoperator)
    - [PostgresHook | Astronomer Registry](https://registry.astronomer.io/providers/postgres/modules/postgreshook)
    - [Templating | Astronomer Guide](https://www.astronomer.io/guides/templating/)
