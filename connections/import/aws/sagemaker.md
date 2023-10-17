
### Module - AWS SageMaker Connection + Operators

**Before you start**

- [ ]  Log in to AWS Console
- [ ]  [Create an IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html) to execute SageMaker jobs (see [SageMaker roles](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html))
- [ ]  Create an S3 bucket in the `us-east-2` region

**IAM User AWS Connection**

- [ ]  [Create an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) (or use an existing one) with access to all relevant resources (S3, SageMaker) - choose `Access key - Programmatic access` as AWS Access Type
- [ ]  Save `Access key ID` and `Secret access key`
- [ ]  Create a connection in one of the following ways:
- Add in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)
    - [An AWS Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)

        ```docker
        export AIRFLOW_CONN_AWS_SAGEMAKER=aws://_your_aws_access_key_id_:_your_aws_secret_access_key_@
        ```

    - Your default AWS region

    ```docker
    export AWS_DEFAULT_REGION=us-east-2
    ```

- **OR** Go to Admin > Connections in the Airflow UI, fill in:
    - `Connection ID`: `aws-sagemaker`
    - `Connection Type`: Amazon Web Services
    - `AWS Access Key ID`: Your AWS access key ID
    - `AWS Secret Access Key`: Your AWS secret access key
    - `Extra` : `{"region_name": "us-east-2"}`

<aside>
💡 If you are running Airflow locally and chose the first way to create a connection, you’ll need to restart the project with `astro dev restart`.

</aside>

**Add Amazon to your Astro project**

- [ ]  Add `apache-airflow-providers-amazon` to your project’s `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-amazon
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the Amazon provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Use SageMaker operators**

- [ ]  Test out AWS SageMaker operators
- Follow `Use Case 2: Orchestrate a Full ML Pipeline` from the guide

[Using Airflow with SageMaker | Apache Airflow Guides](https://registry.astronomer.io/guides/airflow-sagemaker#use-case-2-orchestrate-a-full-ml-pipeline)

**Checkpoint**

At this point you should:

- Have the following resources created in AWS SageMaker `us-east-2` region:
    - Training Job called `train-iris`
- Understand how to orchestrate ML pipelines with AWS SageMaker
- Run the example DAG and see expected output

**Extras / Reference**

- References


    ### AWS SageMaker

    - [AWS Connection | OSS Airflow Doc](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)
    - [Train a machine learning model with SageMaker and Airflow | Astronomer Tutorial](https://registry.astronomer.io/guides/airflow-sagemaker#overview)
