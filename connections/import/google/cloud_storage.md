
### Module - Google Cloud Storage Connection + Operators

**Before You Start**

- [ ]  Have an Astro project running locally
- [ ]  Have [Cloud SDK](https://cloud.google.com/sdk/gcloud)
- [ ]  Have a Google Cloud [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with its email address
- [ ]  Have a [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-accounts) for the service account

**Create a Google Cloud Platform connection**

- [ ]  Create a connection in one of the following ways:
- Go to Admin > Connections in the Airflow UI, fill in :
    - `Connection ID`: `google_cloud_default`
    - `Connection Type`: Google Cloud
    - `Keyfile JSON`: Contents of a service account key file
    - `Scopes (comma separated)`: `https://www.googleapis.com/auth/cloud-platform`
- **OR** Add a [Google Cloud Platform Connection](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

```python
export AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT='google-cloud-platform://?extra__google_cloud_platform__keyfile_dict=<your_keyfile>&extra__google_cloud_platform__scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform&extra__google_cloud_platform__num_retries=5'
```

<aside>
💡 If you are running Airflow locally and chose the second way to create a connection, you’ll need to restart the project. You can restart your project using `astro dev restart`.

</aside>

**Use Google Cloud Storage operator**

- [ ]  Test out GCS operator
- Create the following DAG (add `gcs_list_objects.py` file to your `dags/` directory)

```python
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.providers.google.cloud.operators.gcs import GCSListObjectsOperator

# To be changed accordingly
GOOGLE_CLOUD_CONN = "google_cloud_default"
GCS_BUCKET = "astro-onboarding"
GCS_PREFIX = "airflow2-4"  # Can be deleted if not needed

default_args = {
    "owner": 'cs',
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
    }

with DAG(
    dag_id="gcs_list_objects",
    default_args=default_args,
    start_date=pendulum.datetime(2022, 11, 1, tz="UTC"),
    schedule=None,
    tags=["Google Cloud", "GCS"],
):
    GCSListObjectsOperator(
        task_id="list_all_objects",
        gcp_conn_id=GOOGLE_CLOUD_CONN,
        bucket=GCS_BUCKET,
        prefix=GCS_PREFIX,  # Can be deleted if not needed
    )
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Go to `Admin > Xcoms`, you should see two XComs (with your respective values):
- `storage_conf`: `{'uri': 'astro-onboarding', 'project_id': 'astronomer-success'}` - your bucket name and Google project id
- `return_value`: `['airflow2-4/', 'airflow2-4/prices.csv', 'airflow2-4/quantities.csv']`- this XCom contains the folder name and all the files found inside it

**Checkpoint**

At this point you should:

- Have a working Google Cloud Platform connection
- Run an example DAG using GCS operator

**Extras / Reference**

- References


    ### Google Cloud Storage

    - [Google Cloud Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html)
    - [GCSHook | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/gcshook)
