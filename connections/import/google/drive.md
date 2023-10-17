
### Module - Google Drive Connection + Operators

**Before You Start**

- [ ]  Have an Astro project running locally
- [ ]  Have [Cloud SDK](https://cloud.google.com/sdk/gcloud)
- [ ]  Have a Google Cloud [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) with its email address
- [ ]  Have a [JSON service account key](https://cloud.google.com/iam/docs/creating-managing-service-accounts) for the service account
- [ ]  Grant service account access to My Drive and a chosen folder in Shared Drive

**Create a Google Cloud Platform connection**

- [ ]  Create a connection in one of the following ways:
- Go to Admin > Connections in the Airflow UI, fill in :
    - `Connection ID`: `google_cloud_default`
    - `Connection Type`: Google Cloud
    - `Keyfile JSON`: Contents of a service account key file
    - `Scopes (comma separated)`: `https://www.googleapis.com/auth/drive`
- **OR** Add a [Google Cloud Platform Connection](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

```python
export AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT='google-cloud-platform://?extra__google_cloud_platform__keyfile_dict=<your_keyfile>&extra__google_cloud_platform__scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&extra__google_cloud_platform__num_retries=5'
```

<aside>
💡 If you are running Airflow locally and chose the second way to create a connection, you’ll need to restart the project. You can restart your project using `astro dev restart`.

</aside>

**Use Google Drive operators**

- [ ]  Test out Google Drive operators
- Create the following DAG (add `gdrive_operators.py` file to your `dags/` directory)

```python
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.providers.google.cloud.transfers.gdrive_to_local import GoogleDriveToLocalOperator
from airflow.providers.google.suite.sensors.drive import GoogleDriveFileExistenceSensor

# To be changed accordingly
_CONN_ID = "google_cloud_default"
_SHARED_DRIVE_ID = "0AMSjLLqIOucwUk9PVA"
_SHARED_DRIVE_FOLDER_ID = "15DJjI0BtEEnrjr0llhL2fAtITUmicnfX"
_SHARED_DRIVE_FILE_NAME = "example.xlsx"
_MY_DRIVE_FOLDER_ID = "1VTZ4tp2dPi8YNBWriMn1JXzPhg-ey5P_"
_MY_DRIVE_FILE_NAME = "test_file.txt"

default_args = {
    "owner": "cs",
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
    }

with DAG(
    dag_id="gdrive_operators",
    start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
    schedule=None,
) as dag:

    detect_file_in_my_drive = GoogleDriveFileExistenceSensor(
        task_id="detect_file_in_my_drive",
        gcp_conn_id=_CONN_ID,
        folder_id=_MY_DRIVE_FOLDER_ID,
        file_name=_MY_DRIVE_FILE_NAME,
        mode="reschedule",
        timeout=10,
    )

    # Currently, this operator only works if you use conn_id of "google_cloud_default", can't override it
    download_from_shared_drive_to_local = GoogleDriveToLocalOperator(
        task_id="download_from_shared_drive_to_local",
        drive_id=_SHARED_DRIVE_ID,  # Required for Shared Drive files only
        folder_id=_SHARED_DRIVE_FOLDER_ID,
        file_name=_SHARED_DRIVE_FILE_NAME,
        output_file=f"/usr/local/airflow/include/{_SHARED_DRIVE_FILE_NAME}",
    )

    [detect_file_in_my_drive, download_from_shared_drive_to_local]
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `detect_file_in_my_drive` task, you should see something similar:

```python
{drive.py:80} INFO - Sensor is checking for the file test_file.txt in the folder 1VTZ4tp2dPi8YNBWriMn1JXzPhg-ey5P_
{base.py:68} INFO - Using connection ID 'google_cloud_default' for task execution.
{base.py:301} INFO - Success criteria met. Exiting.
```

- [ ]  In your `include/` directory you should see the file that was copied from the Google Drive

**Checkpoint**

At this point you should:

- Have a working Google Cloud Platform connection
- Run an example DAG using Google Drive Operators

**Extras / Reference**

- References


    ### Google Drive

    - [Google Cloud Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html)
    - [GoogleDriveHook | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/googledrivehook)
    - [GoogleDriveFileExistenceSensor | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/googledrivefileexistencesensor)
    - [GoogleDriveToGCSOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/googledrivetogcsoperator)
    - [GoogleDriveToLocalOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/googledrivetolocaloperator)
    - [GCSToGoogleDriveOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/gcstogoogledriveoperator)
