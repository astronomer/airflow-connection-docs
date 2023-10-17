
### Module - AWS Lambda DAG / Operators / Connection

**Before you Start**

- [ ]  You’ll need:
    - An AWS Account
    - [Lambda policy/permissions](https://docs.aws.amazon.com/lambda/latest/dg/access-control-identity-based.html) attached to an IAM role (for example, `AWSLambda_FullAccess`)
    - `aws_secret_key_id` and `aws_secret_key_access` values from the User account

**Create lambda function to be triggered from Airflow:**

- [ ]  Create a lambda function in the AWS Lambda UI
    - In the AWS UI, navigate to the AWS Lambda page:

        ![Untitled](../images/Untitled%2056.png)

    - Then, select ‘Functions’, and click ‘Create Function’:

        ![Untitled](../images/Untitled%2057.png)

    - Choose the appropriate option for creating your function, such as ‘Author from Scratch’, ‘Use a Blueprint’, etc, and choose the language to write your function in.
    - For example, using ‘Author from Scratch’ and selecting ‘Python 3.9’, create a function named `my_lambda_function` which will be called in the Example DAG below:

        ```python
        import json

        def lambda_handler(event, context):
            print("This is my dict passed in from airflow:")
            print(event)
            return {
                'statusCode': 200,
                'body': json.dumps('Hello from Lambda!')
            }
        ```


**Add an AWS Connection in the Airflow UI:**

- [ ]  Create an aws connection in the Airflow UI with the following values:

    ```yaml
    Connection Id: aws_default
    Connection Type: Amazon Web Services
    Login: <aws_access_key_id>
    Password: <aws_secret_key>
    Extra: {"region_name": "your-aws-region"}
    ```

    <aside>
    💡  * Your `aws_access_key_id` and `aws_secret_key` values can be found in the AWS UI at: IAM > Users > Select User > Security credentials

    * The ‘Extra’ field must be populated as json with the region of your aws/lambda account, such as `us-east-1`.

    </aside>


**Add Example DAG to your project:**

- [ ]  Add an Example DAG to your Astronomer project’s `/dags` folder
    - The following Example DAG will invoke the `my_lambda_function` Lambda function using the `AwsLambdaInvokeFunctionOperator`.

    Example DAG:

    ```python
    import json
    from datetime import datetime
    from airflow import DAG
    from airflow.providers.amazon.aws.operators.aws_lambda import AwsLambdaInvokeFunctionOperator

    lambda_payload = json.dumps(
        {"SampleEvent": {"SampleData": {"Name": "XYZ", "DoB": "1975-01-01"}}}
    )

    with DAG(
        dag_id="lambda_example_dag",
        start_date=datetime(2021, 1, 1),
        catchup=False,
        schedule="@once",
    ) as dag:

        invoke_lambda_task = AwsLambdaInvokeFunctionOperator(
            task_id="invoke_lambda_task",
            function_name="my_lambda_function",
            payload=lambda_payload,
            aws_conn_id="aws_default",
        )

        invoke_lambda_task
    ```


- [ ]  Un-pause and run Example DAG provided above

**Confirm successful Lambda triggering via aws console:**

- [ ]  Confirm via Lambda console/logs that the function was triggered as expected
    - In the aws console on the Lambda page, click on your function, then click Monitor
        - Recent invocations & log streams will be shown here:

        ![Untitled](../images/Untitled%2058.png)


**Checkpoint**

You now have a tested a functioning aws connection in Airflow, and have tested several methods of triggering a Lambda function via an Airflow task.

**Next Steps**

- Implement various Lambda operations into your DAG workflows
- Learn about other ways to connect and interact with Lambda, such as using the `LambdaHook` or a `boto3` client for additional flexibility (links below).

- Reference


    - [Astronomer Guide | Best Practices Calling AWS Lambda from Airflow](https://www.astronomer.io/guides/lambda-cloud)
    - [LambdaHook](https://registry.astronomer.io/providers/amazon/modules/lambdahook)
    - [AwsLambdaInvokeFunctionOperator](https://registry.astronomer.io/providers/amazon/modules/awslambdainvokefunctionoperator)
    - [Amazon Web Services Connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)
