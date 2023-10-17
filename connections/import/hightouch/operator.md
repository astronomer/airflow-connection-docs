
### Module - Hightouch Connection + Operator

> Hightouch is a [Data Activation platform](https://hightouch.io/blog/the-data-activation-company/) that connects and orchestrates data from sources to business tools. The platform manages the varying integrations and logic to activate data models from sources.
>

**Before You Start**

- Acquire an API key from your [Workspace Settings](https://app.hightouch.io/settings)

**Add Hightouch to your Airflow Project**

- [ ]  Add `airflow-provider-hightouch` to your `requirements.txt`

    ```bash
    $ cat requirements.txt
    airflow-provider-hightouch
    ```


**Create a Hightouch Connection**

- [ ]  [Follow this guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) to create an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html).
    - [Refer to these instructions specifically for the values for the connection](https://github.com/hightouchio/airflow-provider-hightouch#configuration)
    - This connection can be [a secret Astronomer Environmental Variable](https://docs.astronomer.io/astro/environment-variables#set-environment-variables-via-the-cloud-ui) and you can add it to your `.env` file if you want to test it locally.
        - Optionally: you can alternatively add it any other way you would add a connection, such as with the Airflow UI or a Secrets Backend
    - In the snippet below - the connection is named `HIGHTOUCH`, feel free to name it anything that makes sense.

    ```bash
    AIRFLOW_CONN_HIGHTOUCH="http://:<API KEY>@https%3A%2F%2Fapi.hightouch.io"
    ```


**Utilizing the HightouchTriggerSyncOperator**

- [ ]  Create the following DAG to test out the `HightouchTriggerSyncOperator`
    - create the file at `dags/example_hightouch.py` or `dags/example_hightouch/example_hightouch.py`
    - run this locally or deploy it to Astro and hit the ▶️ `Trigger DAG` button to see a successful run

    ```bash
    from airflow.decorators import dag
    from airflow_provider_hightouch.operators.hightouch import HightouchTriggerSyncOperator
    from datetime import datetime

    @dag(schedule=None, start_date=datetime(1970, 1, 1))
    def example_hightouch():
        HightouchTriggerSyncOperator(
            task_id="example_hightouch",
            connection_id="hightouch",
            sync_id=42,
            synchronous=True,
        )

    example_hightouch_dag = example_hightouch()
    ```


**Checkpoint**

- At this point you have successfully connected and triggered a Hightouch workload via the `HightouchTriggerSyncOperator` and an Airflow `hightouch` connection

**Next Steps**

- Review the [Hightouch provider](https://registry.astronomer.io/providers/hightouch) and example DAGs
- Merge the `HightouchTriggerSyncOperator` into your Use Case Workload

**Extras / Reference**

- [https://github.com/hightouchio/airflow-provider-hightouch](https://github.com/hightouchio/airflow-provider-hightouch)
- [https://registry.astronomer.io/providers/hightouch](https://registry.astronomer.io/providers/hightouch)
