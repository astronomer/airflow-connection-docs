
### Module - MySQL Connection + Operators

**Before you Start**

- Have an existing MySQL Database with data
- Ensure that your Astronomer Cloud cluster has network access to the existing Database
- Have access to existing MySQL User Credentials

**Add MySQL Provider and Packages**

- [ ]  Add `build-essential` and `libmariadb-dev-compat` to your project’s `packages.txt` file

```bash
$ cat packages.txt
build-essential
libmariadb-dev-compat
```

- [ ]  Add `apache-airflow-providers-mysql` to your project’s `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-mysql
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that MySQL provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create Connection and Test with DAG**

- [ ]  Create a connection in one of the following ways:
    - Add a MySQL Connection in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

        ```bash
        export AIRFLOW_CONN_MYSQL_DEFAULT='mysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<SCHEMA>
        ```

    - **OR** go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`mysql_default`), select `MySQL` as a connection type, and fill in the following fields (leave all other fields as their default value or blank):

        ```yaml
        Connection Id: mysql_default
        Connection Type: Mysql
        Host: <HOST>
        Schema: <Schema>
        Login: <USERNAME>
        Password: <PASSWORD>
        Port: <PORT>
        ```

    - For more information on MySQL connection in Airflow, be sure to review the Airflow OSS documentation

        [MySQL Connection - apache-airflow-providers-mysql Documentation](https://airflow.apache.org/docs/apache-airflow-providers-mysql/stable/connections/mysql.html)

- [ ]  Create a file called `dags/example_mysql.py` or something similar, with the contents:

    ```python
    from datetime import datetime
    from os import getenv
    from airflow import DAG
    from airflow.providers.mysql.operators.mysql import MySqlOperator

    with DAG(
        dag_id="example_mysql",
        start_date=datetime(2021, 1, 1),
        schedule=None
    ) as dag:
        MySqlOperator(
    				mysql_conn_id="mysql_default",
            sql="SELECT 1;",
            task_id="example_mysql",
        )
    		# Note - the MySql Operator does not send query results back
        # If you need the output of the SQL Query, use a PythonOperator
        # and the MysqlHook
    ```


**Checkpoint**

You now have tested a functioning MySql connection in Airflow, and have utilized the `MySqlOperator`

**Next Steps**

- Integrate the new Airflow Connection with your Use Case Workload
- [Review other MySql Operators](https://registry.astronomer.io/modules/?query=mysql&page=1) in the Astronomer Registry

**Extras / Reference**

- Reference


    ### MySQL

    - [MySQL Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-mysql/stable/connections/mysql.html)
    - [MySQLHook | Astronomer Registry](https://registry.astronomer.io/providers/mysql/modules/mysqlhook)
    - [MySQLOperator | Astronomer Registry](https://registry.astronomer.io/providers/mysql/modules/mysqloperator)
    - [S3ToMySqlOperator | Astronomer Registry](https://registry.astronomer.io/providers/mysql/modules/s3tomysqloperator)
