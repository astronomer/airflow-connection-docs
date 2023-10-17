
### Module - DBT Core

> [DBT (data build tool)](https://docs.getdbt.com/docs/introduction) enables analytics engineers to transform data in their warehouses by simply writing select statements. dbt handles turning these select statements into [tables](https://docs.getdbt.com/terms/table) and [views](https://docs.getdbt.com/terms/view).
dbt does the `T` in [ELT](https://docs.getdbt.com/terms/elt) (Extract, Load, Transform) processes – it doesn’t extract or load data, but it’s extremely good at transforming data that’s already loaded into your warehouse.
>

This module is a combination of

- [this blog series](https://www.astronomer.io/blog/airflow-dbt-1),
- the [companion](https://github.com/astronomer/airflow-dbt-demo) project
- and the [jaffle_shop](https://github.com/dbt-labs/jaffle_shop) repo
- We will also pass most of our [important information to DBT via env_var](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var)

**Before You Start**

- Have a Test Schema or Test Database available **OR**
- Have access to any existing DBT projects that will be ported to Airflow
- Have existing knowledge of how to create/debug your DBT project *without Airflow*
- Ensure that you know what can be run with dbt, in what environments, and what will happen if you turn an existing DBT pipeline off or migrate it to Airflow
- Have access to any existing connections required by DBT - they will be turned into [Airflow Connections](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html) and imported into the project

**Install DBT Into Your Airflow Deployment Image**

- [ ]  [Utilize `requirements.txt` (and pip) to install DBT](https://docs.getdbt.com/dbt-cli/install/pip)
    - Additionally, you may want to `pip install dbt-*****` (for example, `pip install dbt-postgres`) on your workstation (or `pip install -r requirements.txt`) to assist your development efforts

<aside>
⚠️ Note: You will need to [specify your database adapter](https://docs.getdbt.com/docs/available-adapters) (`dbt-*****`), and version your new dependency

</aside>

```
$ cat requirements.txt
dbt-*******
```

- If you were running Airflow locally, run `astro dev restart` to install the new dependencies

**Create an Airflow Connection**

- [ ]  [Follow this guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) to create an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html)
    - the specifics will vary greatly based on what system you are integrating with
    - Additionally - the [DBT Documentation](https://docs.getdbt.com/reference/profiles.yml), goes into more detail about what is required to make this connection

<aside>
🛠 Specifics for creating your connection should be inserted here

</aside>

**Setup the DBT definitions and configuration**

Create these files, naming your DAG and the folder containing the DAG and it’s supporting files something that makes sense for workload. We will use `example_dbt` for now. There are a number of places this will need to change if you pick a different name, so be aware and change it as you see it.

- [ ]  Create and fill in `dags/example_dbt/dbt_project.yml`

    ```yaml
    name: 'example_dbt'

    config-version: 2
    version: '0.1'

    profile: 'example_dbt'

    model-paths: [ "models" ]
    seed-paths: [ "seeds" ]
    test-paths: [ "tests" ]
    analysis-paths: [ "analysis" ]
    macro-paths: [ "macros" ]

    log-path: "/tmp/dbt/logs"  # the DAGs folder is read-only locally
    target-path: "/tmp/dbt/target"
    packages-install-path: "/tmp/dbt/dbt_modules"

    clean-targets:
      - "/tmp/dbt/target"
      - "/tmp/dbt/dbt_modules"
      - "/tmp/dbt/logs"

    require-dbt-version: [ ">=1.0.0", "<2.0.0" ]

    models:
      example_dbt:
        materialized: table
        staging:
          materialized: view
    ```

- [ ]  Create and fill in `dags/example_dbt/profiles.yml`

    **note:** that this may change significantly [depending on the type of connection](https://docs.getdbt.com/reference/profiles.yml) ([more reference](https://docs.getdbt.com/dbt-cli/configure-your-profile)), but [the `"{{ env_var( ... ) }}"` pattern will remain](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var)

    ```yaml
    example_dbt:
      target: dev
      outputs:
        dev:
          type: postgres
          host: "{{ env_var('DBT_HOST') }}"
          user: "{{ env_var('DBT_USER') }}"
          password: "{{ env_var('DBT_PASSWORD') }}"
          port: "{{ env_var('DBT_PORT') }}"
          dbname: "{{ env_var('DBT_DBNAME') }}"
          schema: "{{ env_var('DBT_SCHEMA') }}"
    ```

- [ ]  (optional: if you don’t have an existing DBT project) Get the `models` and `seeds` directories from the [Jaffle Shop](https://github.com/dbt-labs/jaffle_shop) project

    ```bash
    wget https://github.com/dbt-labs/jaffle_shop/archive/refs/heads/main.zip
    unzip main.zip
    mv jaffle_shop-main/models dags/example_dbt/
    mv jaffle_shop-main/seeds dags/example_dbt/
    rm -rf jaffle_shop-main
    ```


At this point you should have:

```bash
$ tree dags/example_dbt/
dags/example_dbt/
├── dbt_project.yml
├── models
│   ├── customers.sql
│   ├── docs.md
│   ├── orders.sql
│   ├── overview.md
│   ├── schema.yml
│   └── staging
│       ├── schema.yml
│       ├── stg_customers.sql
│       ├── stg_orders.sql
│       └── stg_payments.sql
├── profiles.yml
└── seeds
    ├── raw_customers.csv
    ├── raw_orders.csv
    └── raw_payments.csv
```

**Create a DBT DAG using the Bash Operator**

- [ ]  Create `dags/example_dbt/example_dbt.py` - see [the Airflow Tutorial](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html) and Education Modules if this is your first time seeing a DAG before continuing

    ⚠️ **DO NOT RUN** `dbt seed` **UNLESS YOU ARE CONNECTED TO A NEW SANDBOX OR DEV DATABASE ⚠️**   Note: this DAG *can* run `dbt seed` to add test data to your database


```python
import os.path
from datetime import datetime

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

# Note - you will need to change this to fit your connection and profiles.yaml
default_args = {
    "env": {
        "DBT_USER": "{{ conn.postgres.login }}",
        "DBT_ENV_SECRET_PASSWORD": "{{ conn.postgres.password }}",
        "DBT_HOST": "{{ conn.postgres.host }}",
        "DBT_SCHEMA": "{{ conn.postgres.schema }}",
        "DBT_PORT": "{{ conn.postgres.port }}",
    }
}
DBT_PROJECT_DIR = os.path.dirname(__file__)

@dag(schedule=None, default_args=default_args, start_date=datetime(1970, 1, 1))
def example_dbt():
    # !!!EXTREMELY IMPORTANT!!! #
    # DO NOT RUN `dbt seed` UNLESS THIS IS A DEV OR SANDBOX DATABASE
    # !!!EXTREMELY IMPORTANT!!! #
    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command=f"dbt seed --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    ) if False else EmptyOperator(task_id="dbt_seed")

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_seed >> dbt_run >> dbt_test

example_dbt_dag = example_dbt()
```

- [ ]  Trigger this DAG to run your DBT models

**Checkpoint**

- You should now be seeing the Jaffle Shop data set compiled correctly in your database
- This DBT pattern can be extended more thoroughly and granularly - which is outlined in part 2 + 3 of the blog post mentioned at the beginning

**Next Steps**

- Merge this dbt work into your Use Case
- Develop your dbt models further
-

**Extras / Reference**

- Reference
