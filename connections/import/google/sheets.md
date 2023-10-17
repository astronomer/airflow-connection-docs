
### Module - Google Sheets Connection + Operator

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
    - `Scopes (comma separated)`: one of the following (check [here](https://developers.google.com/identity/protocols/oauth2/scopes) for more details):
        - `https://www.googleapis.com/auth/drive`
        - `https://www.googleapis.com/auth/drive.file`
        - `https://www.googleapis.com/auth/spreadsheets`
- **OR** Add a [Google Cloud Platform Connection](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

```python
export AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT='google-cloud-platform://?extra__google_cloud_platform__keyfile_dict=<your_keyfile>&extra__google_cloud_platform__scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&extra__google_cloud_platform__num_retries=5'
```

<aside>
💡 If you are running Airflow locally and chose the second way to create a connection, you’ll need to restart the project. You can restart your project using `astro dev restart`.

</aside>

**Create a spreadsheet for testing purposes**

- [ ]  Create a spreadsheet and obtain its ID from the URL
- For example, if the URL is `https://docs.google.com/spreadsheets/d/**1X57tswlaSEqzrhagfohPwA-V4fNF2Rd17lhvJSsBAas**/edit#gid=0`, the ID of the spreadsheet is `1X57tswlaSEqzrhagfohPwA-V4fNF2Rd17lhvJSsBAas`
- [ ]  Grant the service account access to the spreadsheet
- [ ]  Add some dummy data in range `Sheet1!A1:C1`
- [ ]  Grant the service account access to the spreadsheet

**Use GSheetsHook**

- [ ]  Test out GSheetsHook
- Create the following DAG (add `test_gsheets.py` file to your `dags/` directory)

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.google.suite.hooks.sheets import GSheetsHook

# To be changed accordingly
SPREADSHEET_ID = '1X57tswlaSEqzrhagfohPwA-V4fNF2Rd17lhvJSsBAas'
RANGE = 'Sheet1!A1:C1'

default_args = {
        'owner': 'cs',
        'retries': 2,
        'retry_delay': timedelta(seconds=5),
    }

with DAG(dag_id='test_gsheets',
         start_date=datetime(2022, 8, 1),
         schedule=None,
         default_args=default_args,
         ) as dag:

    @task()
    def print_contents():
        hook = GSheetsHook('google_cloud_default')
        contents = hook.get_values(
            spreadsheet_id=SPREADSHEET_ID,
            range_=RANGE,
        )
        print(contents)

    @task()
    def update_values():
        hook = GSheetsHook('google_cloud_default')
        hook.update_values(
            spreadsheet_id=SPREADSHEET_ID,
            range_=RANGE,
            value_input_option='USER_ENTERED',  # Determines how input data should be interpreted
            major_dimension='COLUMNS',  # Indicates which dimension an operation should apply to
            values=[["ready"], ["steady"], ["go"]],
            include_values_in_response=True,  # Determines if the update response should include the values of the cells that were updated
        )

    print_contents() >> update_values()
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `print_contents` task, you should see something similar (depending on the contents of your spreadsheet):

```python
{logging_mixin.py:115} INFO - [['hello', "it's", 'me']]
```

- [ ]  Check the logs of `update_values` task, you should see the following:

```python
{logging_mixin.py:115} INFO - [['ready', 'steady', 'go']]
```

- [ ]  Go to your spreadsheet and confirm the changes were implemented as expected

**Checkpoint**

At this point you should:

- Have a working Google Cloud Platform connection
- Run an example DAG using GSheetsHook

**Extras / Reference**

- References


    ### Google Sheets

    - [Google Cloud Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/connections/gcp.html)
    - [Google Sheets Operators | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/suite/sheets.html)
    - [GSheetsHook | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/gsheetshook)
    - [GoogleSheetsCreateSpreadsheetOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/googlesheetscreatespreadsheetoperator)
    - [GoogleSheetsToGCSOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/googlesheetstogcsoperator)
