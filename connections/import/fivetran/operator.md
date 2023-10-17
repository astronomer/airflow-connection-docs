
### Module - Fivetran Connection + Operator

> Fivetran helps you centralize data from disparate sources which you can manage directly from your browser. We extract your data and load it into your data destination
>

**Before You Start**

- Have connectors available in Fivetran and have `connector_id`s available
- Familiarize yourself with the [Fivetran API Authentication Process](https://fivetran.com/docs/rest-api/getting-started#authentication)

**Add Fivetran to your Airflow Project**

- [ ]  Add `airflow-provider-fivetran` to your `requirements.txt`

    ```bash
    $ cat requirements.txt
    airflow-provider-fivetran
    ```


**Create a Fivetran Connection**

- [ ]  Generate an API Key and Secret in your [Fivetran Account Settings](https://fivetran.com/account/settings)

    ![Untitled](../images/Untitled%2067.png)

- [ ]  [Follow this guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) to create an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html).
    - This connection can be [a secret Astronomer Environmental Variable](https://docs.astronomer.io/astro/environment-variables#set-environment-variables-via-the-cloud-ui) and you can add it to your `.env` file if you want to test it locally.
        - Optionally: you can alternatively add it any other way you would add a connection, such as with the Airflow UI or a Secrets Backend
    - In the snippet below - the connection is named `FIVETRAN`, feel free to name it anything that makes sense.

    ```bash
    AIRFLOW_CONN_FIVETRAN="fivetran://<Fivetran API Key>:<Fivetran API Secret>"
    ```


**Utilizing the FivetranOperator**

- [ ]  Create the following DAG to test out the `FivetranOperator`
    - create the file at `dags/example_fivetran.py` or `dags/example_fivetran/example_fivetran.py`
    - run this locally or deploy it to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
    - Make sure to change `<FIVETRAN CONNECTOR ID>` to the `connector_id` which is in the `Connector` settings page - [more info here](https://registry.astronomer.io/providers/fivetran/modules/fivetranoperator)

    ```bash
    from airflow.decorators import dag
    from fivetran_provider.operators.fivetran import FivetranOperator
    from datetime import datetime

    @dag(schedule=None, start_date=datetime(1970, 1, 1))
    def example_fivetran():
        FivetranOperator(
            task_id="example_fivetran",
            fivetran_conn_id="fivetran",
            connector_id="<FIVETRAN CONNECTOR ID>",
        )

    example_fivetran_dag = example_fivetran()
    ```


**Checkpoint**

- At this point you have successfully connected and triggered a Fivetran workload via the `FivetranOperator` and an Airflow `Fivetran` connection

**Next Steps**

- Review the [Fivetran provider](https://registry.astronomer.io/providers/fivetran) and example DAGs
- Merge the `FivetranOperator` into your Use Case Workload

**Extras / Reference**

- [https://github.com/fivetran/airflow-provider-fivetran#configuration](https://github.com/fivetran/airflow-provider-fivetran#configuration)
- [https://registry.astronomer.io/providers/fivetran](https://registry.astronomer.io/providers/fivetran)
- [https://fivetran.com/docs/rest-api/getting-started#authentication](https://fivetran.com/docs/rest-api/getting-started#authentication)

### Module - FTP Connection + Operators

**Before You Start**

- [ ]  Have an FTP username, password and the hostname or IP of the remote machine

**Add FTP to your Astro project**

- [ ]  Add `apache-airflow-providers-ftp`

```bash
$ cat requirements.txt
apache-airflow-providers-ftp
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the FTP provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create an FTP connection**

- [ ]  Create a connection in one of the following ways:
- Add [an FTP connection](https://airflow.apache.org/docs/apache-airflow-providers-ftp/stable/connections/ftp.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

    ```python
    export AIRFLOW_CONN_FTP_DEFAULT='ftp://user:pass@localhost?passive=false'
    ```

- **OR** Go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`ftp_default`), select `FTP` as a connection type, and fill in appropriate fields: `login`, `password`, and  `host`

**Use FTPSensor**

- [ ]  Test FTP operator
- Create the following DAG (add `test_ftp.py` file to your `dags` directory):

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.ftp.sensors.ftp import FTPSensor

with DAG(
    dag_id='test_ftp',
    start_date=datetime(2022, 7, 1),
    schedule=None,
) as dag:

    wait_for_file = FTPSensor(
        task_id='wait_for_file',
        ftp_conn_id='ftp_default',
        path='/tmp/single-file/customers.csv',  # Remote file or directory path.
        mode='reschedule',  # Worker slot will be released when the criteria is not met yet and rescheduled at a later time.
        poke_interval=15,  # Time in seconds that the job should wait in between each tries.
        timeout=60,  # Time, in seconds before the task times out and fails.
    )
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run

**Checkpoint**

At this point you should:

- Have a working FTP connection
- Run an example task successfully in the DAG

**Extras / Reference**

- References


    ### FTP

    [FTP Connection | Airflow OSS Doc](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c)

    [FTPHook | Astronomer Registry](https://registry.astronomer.io/providers/ftp/modules/ftpshook)

    [FTPSensor | Astronomer Registry](https://registry.astronomer.io/providers/ftp/modules/ftpssensor)

    [FTPToS3Operator | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/ftptos3operator)

