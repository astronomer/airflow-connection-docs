
### Module - dbt Cloud

> [DBT (data build tool)](https://docs.getdbt.com/docs/introduction) enables analytics engineers to transform data in their warehouses by simply writing select statements. dbt handles turning these select statements into [tables](https://docs.getdbt.com/terms/table) and [views](https://docs.getdbt.com/terms/view).
dbt does the `T` in [ELT](https://docs.getdbt.com/terms/elt) (Extract, Load, Transform) processes – it doesn’t extract or load data, but it’s extremely good at transforming data that’s already loaded into your warehouse.
>

**Before you start**

- [ ]  Have existing knowledge of how to create/debug your DBT project *without Airflow*
- [ ]  Ensure that you know what can be run with dbt, in what environments, and what will happen if you turn an existing DBT pipeline off or migrate it to Airflow
- [ ]  Have a test schema or test database available **OR**
- [ ]  Have access to any existing dbt projects that will be ported to Airflow
- [ ]  Have access to any existing connections required by dbt - they will be turned into [Airflow Connections](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html) and imported into the project

**Add dbt Cloud to your Airflow environment**

- [ ]  Add the following line to your `requirements.txt` file:

```
apache-airflow-providers-dbt-cloud
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the Databricks provider is installed. You can restart your project using `astro dev restart`

</aside>

**Create Airflow connection**

- [ ]  Create a connection in one of the following ways:
    - Go to Admin > Connections in the Airflow UI, fill in:
        - `Connection ID` : `dbt_cloud_default`
        - `Connection Type`: `dbt Cloud`
        - `Tenant`: Optional. The Tenant name for your dbt Cloud environment (i.e. [https://my-tenant.getdbt.com](https://my-tenant.getdbt.com/)). This is particularly useful when using a single-tenant dbt Cloud instance
        - `Account ID`: Optional. If an Account ID is provided in the connection, you are not required to pass **`account_id`**to operators or hook methods
        - `API token`: The API token to use when authenticating to the dbt Cloud API
    - **OR** add a dbt Cloud connection in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)
        - When not specifying an `account_id`, make sure to remove it:

            ```bash
            export AIRFLOW_CONN_DBT_CLOUD_DEFAULT='dbt-cloud://account_id:api_token@'
            ```

        - When specifying `tenant name`:

            ```bash
            export AIRFLOW_CONN_DBT_CLOUD_DEFAULT='dbt-cloud://:api_token@:/my-tenant'
            ```

    - For more information on the dbt Cloud connection in Airflow, be sure to review the Airflow OSS documentation

        [Connecting to dbt Cloud - apache-airflow-providers-dbt-cloud Documentation](https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/connections.html)



**Test the connection**

- [ ]  Test out dbt Cloud hook
- Create the following DAG (add `dbt_cloud_example.py` file to your `dags/` directory)

```python
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook

# To be changed accordingly
DBT_CLOUD_CONN = "dbt_cloud_default"

default_args = {
    'owner': 'cs',
    'retries': 1,
    'retry_delay': timedelta(seconds=15),
    }

with DAG(
    dag_id="dbt_cloud_example",
    default_args=default_args,
    start_date=pendulum.datetime(2022, 11, 1, tz="UTC"),
    schedule=None,
    tags=["dbt Cloud", "TaskFlow API"],
):

    @task
    def list_all_projects(conn_id):
        hook = DbtCloudHook(dbt_cloud_conn_id=conn_id)
        print(hook.list_projects())

    list_all_projects(conn_id=DBT_CLOUD_CONN)
```

<aside>
💡 If you did not specify `account ID` in the connection, make sure to pass it to `list_projects()` method.

</aside>

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Go to logs of `list_all_projects` tasks, you should see the following:

```python
{http.py:148} INFO - Sending 'GET' to url: https://cloud.getdbt.com/api/v2/accounts/<your_account_id>/projects/
{logging_mixin.py:120} INFO - [<Response [200]>]
```

**Checkpoint**

At this point you should:

- Have a working dbt Cloud connection
- Run the example DAG and see expected output

**Extras / Reference**

- References


    ### DBT

    - [GitHub](https://github.com/astronomer/airflow-dbt-demo): *Proof-of-concept that shows users how to run DBT commands using a BashOperator. This repository was created as a support to the Blog posts below.*
    - [Orchestrate dbt with Airflow | Astronomer Tutorials](https://docs.astronomer.io/learn/airflow-dbt#dbt-cloud)
    - Astronomer Blog:
        - [Blog Post 1: Building a Scalable Analytics Architecture with Airflow and dbt](https://www.astronomer.io/blog/airflow-dbt-1)

            *Describes the* **dbt_basic.py** *and* **dbt_advanced_dag.py** *DAGs in the above repository. For dbt_basic, there are a couple of simple BashOperators running simple DBT commands (i.e. seed, run, test). For dbt_advanced_dag, there are several dynamically generated tasks based on the* **dbt/target/manifest.json** *file in the repository*

        - [Blog Post 2: Building a Scalable Analytics Architecture with Airflow and dbt: Part 2](https://www.astronomer.io/blog/airflow-dbt-2)

            *Describes the elt.py DAG in the above repository. Shows how to build a script that would be used in a CI/CD process to automatically update the* **dbt/target/manifest.json** *file as well as use singer.io to run a singer tap command against GitHub as an ELT workflow*

        - [Blog Post 3: Building a Scalable Analytics Architecture with Airflow and dbt: Part 3](https://www.astronomer.io/blog/airflow-dbt-3)

            *Describes the* **dbt_advanced_utility.py** *DAG in the above repository. This DAG creates a parser utility that puts the same DBT DAGs together from part 2 in a more convenient fashion.*

        - [Integrating Airflow and dbt (Astronomer Guide)](https://www.astronomer.io/guides/airflow-dbt): *Contains a nice summary of the 3 blog posts so that you don’t need to jump around links*
    - [dbt Cloud Provider](https://registry.astronomer.io/providers/dbt-cloud) | Astronomer Regsitry
