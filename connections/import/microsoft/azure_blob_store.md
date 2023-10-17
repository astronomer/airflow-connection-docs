
### Module - Azure Blob Storage DAG / Connection

**Before you start:**

- You’ll need an Azure Blob Storage Account



**Create a storage container in Azure:**

- [ ]  Create a storage container named `covid-data` which will be used by the Example DAG

    ![Untitled](../images/Untitled%2059.png)


**Obtain Storage Account Credentials:**

- [ ]  Obtain your Storage Account’s **Key:**
    - In the Azure Portal homepage, navigate to **Storage Accounts**
    - Select your existing storage account
    - On the left-hand menu of your storage account, click **Access Keys**
    - Click **Show keys** at the top of the page, then copy the **Key** (not the Connection String), which will be used in the next step
    - To illustrate where the credentials can be found:

        ![Untitled](../images/Untitled%2060.png)


**Add an Azure Blob connection in the Airflow UI:**

- [ ]  Create a ****Microsoft Azure Blob Storage Connection**** named `wasb_default` in the Airflow UI:
    - Fields to populate:
        - `Connection ID` -  `wasb_default`
        - `Connection Type` - Azure Blob Storage
        - `Blob Storage Login` - This is the name of your storage account (found in the top-left corner of the Storage Account’s page):

            ![Untitled](../images/Untitled%2061.png)

        - `Blog Storage Key` - This value was obtained in the previous “Obtain Storage Account Credentials” step above:
        - To summarize, these are the 4 fields to populate:

            ![Untitled](../images/Untitled%2062.png)


**Add Azure to your Airflow environment**

- [ ]  Add the following lines to your `requirements.txt` file:

```
apache-airflow-providers-microsoft-azure

```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the Azure provider is installed. You can restart your project using `astro dev restart`

</aside>

**Add Example DAG to your project:**

- [ ]  Add an Example DAG to your Astronomer project’s `/dags` folder
    - Example DAG

        ```python
        from airflow import DAG
        from airflow.decorators import task
        from airflow.operators.empty import EmptyOperator
        from airflow.providers.microsoft.azure.hooks.wasb import WasbHook
        from airflow.utils.task_group import TaskGroup
        from datetime import datetime, timedelta
        import requests

        endpoints = ["ca", "co", "ny", "pa", "wa"]
        date = "{{ ds_nodash }}"

        with DAG(
            "azure_blob_dag",
            start_date=datetime(2021, 1, 1),
            max_active_runs=1,
            schedule="@daily",
            tags=["azure"],
            default_args={
                "email_on_failure": False,
                "email_on_retry": False,
                "retries": 1,
                "retry_delay": timedelta(minutes=1),
            },
            catchup=False,  # enable if you don't want historical dag runs to run
        ) as dag:

            start = EmptyOperator(task_id="start")

            with TaskGroup("covid_task_group") as covid_group:
                for endpoint in endpoints:

                    @task(task_id="generate_file_{0}".format(endpoint))
                    def upload_to_azure_blob(endpoint: str, date: str) -> None:
                        # Instanstiate hook
                        azurehook = WasbHook(wasb_conn_id="wasb_default")

                        # Make request to get Covid data from API
                        url = "https://covidtracking.com/api/v1/states/"
                        filename = "{0}/{1}.csv".format(endpoint, date)
                        res = requests.get(url + filename)

                        # Take string, upload to blob using predefined method
                        azurehook.load_string(string_data=res.text, container_name="covid-data", blob_name=filename)

                    upload_to_azure_blob(endpoint=endpoint, date=date)

            finish = EmptyOperator(task_id="finish")

            start >> covid_group >> finish
        ```


**Run the DAG:**

- [ ]  Run the Example DAG
    - Un-pause the Example DAG provided above, allowing it to run


**Confirm successful blob creation:**

- [ ]  Confirm via Azure Blob Storage console that the blobs were created in the appropriate container and directories:

    ![Untitled](../images/Untitled%2063.png)


**Checkpoint:**

You now have a tested a functioning Azure Blob connection in Airflow using a `WasbHook`, and have successfully loaded data into your Azure Container.

**Next Steps:**

- Integrate various Azure Blob interactions into your workflows using your Azure Blob connection, the  `WasbHook`, and other Wasb operators such as `WasbBlobSensor`, `WasbDeleteBlobOperator`, and `WasbPrefixSensor` (links below)

- **Extras/References**


    ### Wasb

    - [Microsoft Azure Connection | Airflow OSS](https://airflow.apache.org/docs/apache-airflow-providers-microsoft-azure/stable/connections/azure.html)
    - [FileToWasbOperator | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/filetowasboperator)
    - [LocalFileSystemToWasbOperator | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/localfilesystemtowasboperator)
    - [SFTPToWasbOperator  | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/sftptowasboperator)
    - [WasbBlobSensor | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbblobsensor)
    - [WasbDeleteBlobOperator | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbdeletebloboperator)
    - [WasbHook | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbhook)
    - [WasbPrefixSensor | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbprefixsensor)
    - [WasbTaskHandler | Astronomer Registry](https://registry.astronomer.io/providers/microsoft-azure/modules/wasbtaskhandler)
