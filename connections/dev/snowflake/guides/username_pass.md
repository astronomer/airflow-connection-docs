## Before you Start

- Have a Snowflake Account

## Gather Credentials

- Create Snowflake Database User (note the `Username` & `Password`) - [CREATE USER - Snowflake Documentation](https://docs.snowflake.com/en/sql-reference/sql/create-user.html)
- Obtain the `Host Endpoint`, `Account`, & `Region`

<aside class="alert alert-info">
💡 If you login to snowflake via a web browser, these parameters are in the URL. So if your URL was: `https://gp12345.us-east-1.snowflakecomputing.com/` then these would be your parameters:
  - host endpoint: `gp12345.us-east-1.snowflakecomputing.com/`
  - account: `gp12345`
  - region: `us-east-1`
</aside>

- Obtain the `Database Name` that your user is going to be using
- Obtain the `warehouse` that your user is going to be using

<aside class="alert alert-info">
💡 If you login to snowflake via a web browser (with the account Airflow will be using), you can find the warehouses that your user has access to by clicking the `Warehouses` button on the header of the page
</aside>

## Add Snowflake to your Airflow environment

- Add the following line to your `requirements.txt` file

```
apache-airflow-providers-snowflake
```

<aside class="alert alert-info">
💡 If you are running Airflow locally, you’ll need to restart the project so that the Snowflake provider is installed. You can restart your project using `astro dev restart`
</aside>

## Create Connection

- Create a connection in one of the following ways:
  - Add a Snowflake Connection in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)
    ```bash
    export AIRFLOW_CONN_SNOWFLAKE_DEFAULT='snowflake://<USERNAME>:<PASSWORD>@<HOST-ENDPOINT>?extra__snowflake__account=<SNOWFLAKE-ACCOUNT>&extra__snowflake__database=<DATABASE>&extra__snowflake__region=<REGION>&extra__snowflake__warehouse=<WAREHOUSE>'
    ```
  - **OR** go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`snowflake_default`), select `Snowflake` as a connection type, and fill in the following fields (leave all other fields as their default value or blank):
    ```yaml
    Connection Id: snowflake_default
    Connection Type: Snowflake
    Host: <HOST-ENDPOINT>
    Login: <USERNAME>
    Password: <PASSWORD>
    Account: <ACCOUNT>
    Database: <DATABASE NAME>
    Region: <REGION>
    Warehouse: <WAREHOUSE>
    ```
  - For more information on Snowflake connection in Airflow, be sure to review the Airflow OSS documentation [Snowflake Connection - apache-airflow-providers-snowflake Documentation](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html)

## Test the Connection

- Run this Test DAG

## Checkpoint

You now have

- tested the Snowflake connection in Airflow
- and have utilized the `SnowflakeOperator`

## Next Steps

- Integrate the new Airflow Connection with your Use Case Workload
- [Review other Snowflake Operators](https://registry.astronomer.io/modules/?query=Snowflake&page=1) in the Astronomer Registry

## Reference

- [Orchestrate Snowflake Queries with Airflow | Astronomer Tutorial](https://docs.astronomer.io/learn/airflow-snowflake)
- [Intro to Airflow for ETL with Snowflake | Astronomer Webinar](https://www.youtube.com/watch?v=3-XGY0bGJ6g)
- [Snowflake Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html)
- [SnowflakeOperator | Astronomer Registry](https://registry.astronomer.io/providers/snowflake/modules/snowflakeoperator)
