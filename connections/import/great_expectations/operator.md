
### Module - GreatExpectations DAG + Operators

**Before you start**

- [ ]  Have at least basic knowledge about Great Expectations
- [ ]  Review the “Integrating Airflow and Great Expectations” guide

[Integrating Airflow and Great Expectations - Airflow Guides](https://www.astronomer.io/guides/airflow-great-expectations/)

**Install Great Expectations provider**

- [ ]  Add `airflow-provider-great-expectations` to your `requirements.txt` file

```bash
$ cat requirements.txt
airflow-provider-great-expectations
```

- [ ]  Enable XCom pickling by adding the following to your `Dockerfile`:

```docker
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project using `astro dev restart`.

</aside>

**Great Expectations setup**

- [ ]  In your `include` directory create a `great_expectations` folder which will contain following sub-directories:
- `checkpoints` - with at least one [checkpoint](https://docs.greatexpectations.io/docs/guides/validation/validate_data_overview#creating-a-checkpoint)
- `expectations` - with at least one [Expectation Suite](https://docs.greatexpectations.io/docs/guides/expectations/create_expectations_overview)
- `great_expectations.yml` - a configuration file with at least one [Datasource](https://docs.greatexpectations.io/docs/tutorials/getting_started/tutorial_connect_to_data)
- Datasource setup
    - [ ]  In this example Datasource called `currencies` will be a connection to the `include/data` directory, therefore `great_expectations.yml` should look as follows:

        ```yaml
        config_version: 3.0

        datasources:
          currencies:
            module_name: great_expectations.datasource
            execution_engine:
              module_name: great_expectations.execution_engine
              class_name: PandasExecutionEngine
            class_name: Datasource
            data_connectors:
              default_inferred_data_connector_name:
                module_name: great_expectations.datasource.data_connector
                base_directory: ../data
                class_name: InferredAssetFilesystemDataConnector
                default_regex:
                  group_names:
                    - data_asset_name
                  pattern: (.*)
              default_runtime_data_connector_name:
                module_name: great_expectations.datasource.data_connector
                assets:
                  my_runtime_asset_name:
                    module_name: great_expectations.datasource.data_connector.asset
                    batch_identifiers:
                      - runtime_batch_identifier_name
                    class_name: Asset
                class_name: RuntimeDataConnector
        config_variables_file_path: uncommitted/config_variables.yml

        plugins_directory: plugins/

        stores:
          expectations_store:
            class_name: ExpectationsStore
            store_backend:
              class_name: TupleFilesystemStoreBackend
              base_directory: expectations/

          validations_store:
            class_name: ValidationsStore
            store_backend:
              class_name: TupleFilesystemStoreBackend
              base_directory: uncommitted/validations/

          evaluation_parameter_store:
            class_name: EvaluationParameterStore

          checkpoint_store:
            class_name: CheckpointStore
            store_backend:
              class_name: TupleFilesystemStoreBackend
              suppress_store_backend_id: true
              base_directory: checkpoints/

          profiler_store:
            class_name: ProfilerStore
            store_backend:
              class_name: TupleFilesystemStoreBackend
              suppress_store_backend_id: true
              base_directory: profilers/

        expectations_store_name: expectations_store
        validations_store_name: validations_store
        evaluation_parameter_store_name: evaluation_parameter_store
        checkpoint_store_name: checkpoint_store

        anonymous_usage_statistics:
          enabled: true
          data_context_id: 1412c5ca-4703-430f-b7c4-7c697c734330
        notebooks:

        ```

- Expectations setup
    - [ ]  In `great_expectations/expectations` create a file called `currencies_expectations.json` that will contain `currencies_expectations` Expectation Suite with two [expectations](https://greatexpectations.io/expectations/):
    - column count equals 2, see `expect_table_column_count_to_equal`
    - distinct values from `currency` column to be in a certain set, see `expect_column_distinct_values_to_be_in_set`

    ```json
    {
      "data_asset_type": null,
      "expectation_suite_name": "currencies_expectations",
      "expectations": [
        {
          "expectation_type": "expect_table_column_count_to_equal",
          "kwargs": {
            "value": 2
          },
          "meta": {}
        },
        {
          "expectation_type": "expect_column_distinct_values_to_be_in_set",
          "kwargs": {
            "column": "currency",
            "value_set": ["EUR", "TRY", "CHF", "GBP", "PLN"]
          },
          "meta": {}
        }
      ],
      "ge_cloud_id": null,
      "meta": {
        "great_expectations_version": "0.15.18"
      }
    }
    ```

- Checkpoint setup
    - [ ]  In `great_expectations/checkpoints` create a file called `currencies_checkpoint.yml` that will contain a checkpoint called `currencies_checkpoint`

    ```yaml
    name: currencies_checkpoint
    config_version: 1.0
    template_name:
    module_name: great_expectations.checkpoint
    class_name: Checkpoint
    run_name_template: '%Y%m%d-%H%M%S-my-run-name-template'
    expectation_suite_name:
    batch_request: {}
    action_list:
      - name: store_validation_result
        action:
          class_name: StoreValidationResultAction
      - name: store_evaluation_params
        action:
          class_name: StoreEvaluationParametersAction
      - name: update_data_docs
        action:
          class_name: UpdateDataDocsAction
          site_names: []
    evaluation_parameters: {}
    runtime_configuration: {}
    validations:
      - batch_request:
          datasource_name: currencies
          data_connector_name: default_inferred_data_connector_name
          data_asset_name: currencies.csv
          data_connector_query:
            index: -1
        expectation_suite_name: currencies_expectations
    profilers: []
    ge_cloud_id:
    expectation_suite_ge_cloud_id:

    ```

- [ ]  In your `.gitignore` file add the following lines:

```python
include/great_expectations/uncommitted/
include/great_expectations/expectations/.ge_store_backend_id
```

**Use GreatExpectationsOperator**

- [ ]  Test out `GreatExpectationsOperator`
- Create the following DAG (add `great_expectations_example.py` file to your `dags/` directory)

```python
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.decorators import task
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

_BASE_PATH = "/usr/local/airflow/include"
_FILE_LOCATION = f"{_BASE_PATH}/data"
_FILE_NAME = "currencies.csv"

default_args = {
    "owner": "cs",
    "retries": 1,
    "retry_delay": timedelta(seconds=15),
    }

with DAG(
    dag_id="great_expectations_example",
    start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
    schedule=None,
    default_args=default_args,
    ) as dag:

    @task
    def create_data():
        import os
        import pandas as pd

        data = {
            "currency": ["EUR", "TRY", "CHF", "GBP", "PLN"],
            "currency_to_usd": [1.01, 0.055, 1.04, 1.18, 0.21],
        }

        df = pd.DataFrame(data)
        if not os.path.exists(_FILE_LOCATION):
            os.makedirs(_FILE_LOCATION)
        df.to_csv(os.path.join(_FILE_LOCATION, _FILE_NAME), index=False)

    # Runs a checkpoint
    ge_run_checkpoint = GreatExpectationsOperator(
        task_id="ge_run_checkpoint",
        data_context_root_dir=f"{_BASE_PATH}/great_expectations",
        checkpoint_name="currencies_checkpoint",
        fail_task_on_validation_failure=True,  # Fail the Airflow task if the Great Expectation validation fails
    )

    @task(trigger_rule="all_done")
    def remove_file():
        import shutil
        shutil.rmtree(_FILE_LOCATION)

    create_data() >> ge_run_checkpoint >> remove_file()
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Change `expect_table_column_count_to_equal` expectation as shown below and trigger your DAG again:

```python
{
  "expectation_type": "expect_table_column_count_to_equal",
  "kwargs": {
    "value": 3
},
```

- As there are 2 columns in the `CSV` file, the expectation above will not be met
- [ ]  Check the logs of a failed `ge_run_checkpoint` task, you should see the following:

```python
[2022-08-23, 13:38:14 UTC] {taskinstance.py:1910} ERROR - Task failed with exception
Traceback (most recent call last):
  File "/usr/local/lib/python3.9/site-packages/great_expectations_provider/operators/great_expectations.py", line 162, in execute
    self.handle_result(result)
  File "/usr/local/lib/python3.9/site-packages/great_expectations_provider/operators/great_expectations.py", line 188, in handle_result
    raise AirflowException(
airflow.exceptions.AirflowException: Validation with Great Expectations failed.
```

**Checkpoint**

At this point you should:

- Understand and be able to use `GreatExpectationsOperator`

**Extras / Reference**

- References
