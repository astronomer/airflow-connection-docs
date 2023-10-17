
### Module - GitHub Connection + Operators

**Before you start**

- [ ]  Have [a GitHub access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

**Add GitHub to your Astro project**

- [ ]  Add `apache-airflow-providers-github` to your `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-github
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the FTP provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create a GitHub connection**

- [ ]  Create a connection in one of the following ways:
- Add [a Github connection](https://airflow.apache.org/docs/apache-airflow-providers-github/stable/connections/github.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

    ```python
    export AIRFLOW_CONN_GITHUB_DEFAULT='github://:your_access_token@'
    ```

- OR Go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`github_default`), select `GitHub` as a connection type, and add your token in `GitHub Access Token` field

**Use GithubOperator**

- [ ]  Create the following DAG (add `interact_with_github.py` file to your `dags` directory):

```python
import logging
import pendulum
from datetime import timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.github.operators.github import GithubOperator

REPO_NAME = 'apache/airflow'  # To be changed accordingly

default_args = {
    'owner': 'cs',
    'retries': 3,
    'retry_delay': timedelta(seconds=15),
    }

with DAG(
    dag_id='interact_with_github',
    default_args=default_args,
    start_date=pendulum.datetime(2022, 8, 1, tz="UTC"),
    schedule=None,
    description='This DAG demonstrates how to interact with GitHub.',
    tags=['GitHub'],
    ) as dag:

    list_branches = GithubOperator(
        task_id='list_branches',
        github_method='get_repo',
        github_method_args={'full_name_or_id': REPO_NAME},
        result_processor=lambda repo: logging.info(list(repo.get_branches())),
    )

    list_pull_requests = GithubOperator(
        task_id='list_pull_requests',
        github_method='get_repo',
        github_method_args={'full_name_or_id': REPO_NAME},
        result_processor=lambda repo: logging.info(list(repo.get_pulls())),
    )

    list_branches >> list_pull_requests
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `list_branches` task, you should see something similar:

```python
{interact_with_github.py:36} INFO - [Branch(name="dev"), Branch(name="master")]
```

- [ ]  Check the logs of `list_pull_requests` task, you should see something similar:

```python
{interact_with_github.py:43} INFO - [PullRequest(title="Merge pull request #17 from astronomer/mg_timetables", number=18)]
```

**Checkpoint**

At this point you should:

- Have a working Github connection
- Run example tasks successfully in the DAG

**Extras / Reference**

- References


    ### Github

    [Github Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-github/stable/connections/github.html)

    [GithubHook | Astronomer Registry](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c)

    [BaseGithubRepositorySensor | Astronomer Registry](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c)

    [GithubSensor | Astronomer Registry](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c)

    [GithubTagSensor | Astronomer Registry](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c)

    [GithubOperator | Astronomer Registry](https://www.notion.so/Resource-Glossary-a45cce63a5c7468b922454fd937d4a5c)

    [PyGithub examples | Github Actions](https://github.com/PyGithub/PyGithub/tree/master/doc/examples)

