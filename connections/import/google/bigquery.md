
### Module - BigQuery Connection + Operators

**Service Account BigQuery Connection**

- [ ]  [Create a new Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts/create) (or retrieve the JSON for an existing Service Account with Permission)

    ![Untitled](../images/Untitled%2064.png)

- [ ]  Add Roles to your Service Account - `BigQuery User` , and `BigQuery Data Editor` then click through to `Done`

    ![Untitled](../images/Untitled%2065.png)

- [ ]  Navigate to your new Service Account, then `Keys` , then `Add Key` , then download a Service Account JSON Key File

    ![Untitled](../images/Untitled%2066.png)


**Add BigQuery Connection to Airflow via Astronomer Environmental Variables**

- [ ]  Turn your Service Account JSON into an Airflow Connection with the following snippet below.  Make sure to change `AIRFLOW_CONN_BIGQUERY` (which would be `conn_id="bigquery"`) to whatever you want your connection to be called, e.g. `AIRFLOW_CONN_MY_NEW_CONNECTION` would become a conn_id of `my_new_connection`, and change `/path/to/your/keyfile.json` to the path to the file you just downloaded

```bash
echo "AIRFLOW_CONN_BIGQUERY='google-cloud-platform://?extra__google_cloud_platform__keyfile_dict=$(python -c "import sys, json, urllib.parse; print(urllib.parse.quote(json.dumps(json.loads(open(sys.argv[1]).read()))))" /path/to/your/keyfile.json )'"
```

- [ ]  Set the output of the above command to be [a secret Astronomer Environmental Variable](https://docs.astronomer.io/astro/environment-variables#set-environment-variables-via-the-cloud-ui) and add it to your `.env` file if you want to test it locally. (Optional: you can alternatively add it any other way you would add a connection, such as with the Airflow UI or a Secrets Backend)

**Test the Connection**

- [ ]  Deploy and run this DAG to test the connection

```bash
import os
from datetime import datetime

from airflow.decorators import dag
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator

@dag(schedule=None, default_args={"retries": 0}, start_date=datetime(1970, 1, 1))
def example_bg():
    BigQueryCheckOperator(
        task_id="test",
        sql="SELECT 1;",
        use_legacy_sql=False,
        # Make sure to change this to the snake_case version of whatever your AIRFLOW_CONN_XYZ is called
        # Reference:
        # https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#storing-connections-in-environment-variables
        gcp_conn_id="bigquery"
    )

example_bg_dag = example_bg()
```

**Checkpoint**

You now have a tested and functioning BigQuery connection in Airflow, and have utilized the `BigQueryCheckOperator`

**Next Steps**

- Integrate the new Airflow Connection with your Use Case Workload
- [Review other BigQuery Operators](https://registry.astronomer.io/modules?query=bigquery&page=1) in the Astronomer Registry

**Extras / Reference**

- Reference
    - [BigQueryExecuteQueryOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/bigqueryexecutequeryoperator)
    - [Google Cloud BigQuery Operators | Airflow Doc](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/bigquery.html)
