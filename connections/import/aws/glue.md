
### Module - AWS Glue Connection + Operators

**Before you start**

- [ ]  Have `aws_default` [connection](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)
- [ ]  [Create a role](https://www.notion.so/Astro-Data-Engineering-e60033fca30c4e618d3b8dc51b2ee8ab) with putobject/getobject access to the bucket, as well as the Glue service role

**Use Glue operators**

- [ ]  Test out AWS Glue operator
- Create the following DAG (add `glue_example.py` file to your `dags/` directory)

```python
docs = """
This DAG shows how to interact with AWS Glue. \n
It creates a Glue Crawler and a Glue Job based on the example CSV and Spark script.
"""

from datetime import timedelta
from os import getenv

import pendulum
from airflow import DAG
from airflow.decorators import task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
from airflow.providers.amazon.aws.sensors.glue_crawler import GlueCrawlerSensor

# To be changed accordingly
GLUE_EXAMPLE_S3_BUCKET = getenv('GLUE_EXAMPLE_S3_BUCKET', 'astro-onboarding')
GLUE_DATABASE_NAME = getenv('GLUE_DATABASE_NAME', 'demo_database')
GLUE_JOB_NAME = 'demo_glue_job'
GLUE_CRAWLER_ROLE = getenv('GLUE_CRAWLER_ROLE', 'glue-demo-full-access')
GLUE_CRAWLER_NAME = 'demo_crawler'
GLUE_CRAWLER_CONFIG = {
    'Name': GLUE_CRAWLER_NAME,
    'Role': GLUE_CRAWLER_ROLE,
    'DatabaseName': GLUE_DATABASE_NAME,
    'Targets': {
        'S3Targets': [
            {
                'Path': f'{GLUE_EXAMPLE_S3_BUCKET}/glue_demo/data/input',
            }
        ]
    },
}

# Example CSV file and Spark script to operate on the CSV data.
EXAMPLE_CSV = '''
adam,5.5
chris,5.0
frank,4.5
fritz,4.0
magda,3.5
phil,3.0
'''

EXAMPLE_SCRIPT = f'''
import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext

glueContext = GlueContext(SparkContext.getOrCreate())
logger = glueContext.get_logger().addHandler(logging.StreamHandler(sys.stdout))
datasource = glueContext.create_dynamic_frame.from_catalog(
             database='{GLUE_DATABASE_NAME}', 
             table_name='input'
)

logger.info('There are %s items in the table' % datasource.count())

datasource.toDF().write.format('csv').mode("append").save('s3://{GLUE_EXAMPLE_S3_BUCKET}/glue_demo/data/output/')
'''

default_args = {
        'owner': 'cs',
        'retries': 4,
        'retry_delay': timedelta(seconds=15),
    }

with DAG(
    dag_id='glue_example',
    schedule=None,
    start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
    default_args=default_args,
    doc_md=docs,
) as dag:

    @task()  # TaskFlow API decorator for PythonOperator
    def upload_artifacts_to_s3():
        """
        Upload example Spark script that will be used by the Glue Job.
        """
        s3_hook = S3Hook()
        s3_load_kwargs = {"replace": True, "bucket_name": GLUE_EXAMPLE_S3_BUCKET}
        s3_hook.load_string(string_data=EXAMPLE_CSV, key='glue_demo/data/input/input.csv', **s3_load_kwargs)
        s3_hook.load_string(string_data=EXAMPLE_SCRIPT, key='glue_demo/scripts/etl_script.py', **s3_load_kwargs)

    crawl_s3 = GlueCrawlerOperator( # Creates, updates & triggers a Glue Crawler.
        task_id='crawl_s3',
        config=GLUE_CRAWLER_CONFIG,
        wait_for_completion=False,
    )

    wait_for_crawl = GlueCrawlerSensor(  # Waits until the state of a Glue Crawler reaches a terminal state.
        task_id='wait_for_crawl',
        crawler_name=GLUE_CRAWLER_NAME,
        mode='reschedule',
    )

    submit_glue_job = GlueJobOperator(  # Creates a Glue Job.
        task_id='submit_glue_job',
        job_name=GLUE_JOB_NAME,
        wait_for_completion=False,
        s3_bucket=GLUE_EXAMPLE_S3_BUCKET,
        script_location=f's3://{GLUE_EXAMPLE_S3_BUCKET}/glue_demo/scripts/etl_script.py',
        iam_role_name=GLUE_CRAWLER_ROLE.split('/')[-1],
        concurrent_run_limit=3,
    )

    wait_for_job = GlueJobSensor(  # Waits until the state of a Glue Job reaches a terminal state.
        task_id='wait_for_job',
        job_name=GLUE_JOB_NAME,
        run_id=submit_glue_job.output,
        mode='reschedule',
    )

    upload_artifacts_to_s3() >> crawl_s3 >> wait_for_crawl >> \
    submit_glue_job >> wait_for_job
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Go to your S3 bucket to confirm the files were created as expected - you should see:
- `input.csv` in `glue_demo/data/input/`
- `part-00000-[...].csv` in `glue_demo/data/output/`
- `etl_script.py` in `glue_demo/scripts/`

**Checkpoint**

At this point you should:

- Understand how AWS Glue operators work
- Run the example DAG and see expected output

**Extras / Reference**

- References


    ### AWS Glue

    [AWS Connection | OSS Airflow Doc](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/connections/aws.html)

    [AwsGlueJobHook | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluejobhook)

    [AwsGlueJobSensor | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluejobsensor)

    [AwsGlueJobOperator | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/gluejoboperator)

    [AwsGlueCrawlerHook | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluecrawlerhook)

    [AwsGlueCrawlerSensor | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluecrawlersensor)

    [AwsGlueCrawlerOperator | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluecrawleroperator)

    [AwsGlueCatalogHook | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluecataloghook)

    [AwsGlueCatalogPartitionSensor | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/awsgluecatalogpartitionsensor)

