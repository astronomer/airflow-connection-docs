
### Module - Zendesk Connection + Operator

**Before you start**

- [ ]  Have a Zendesk service account
- [ ]  Create an API token

**Add Zendesk to you Astro project**

- [ ]  Add `apache-airflow-providers-zendesk` to your `requirements.txt`

```bash
$ cat requirements.txt
apache-airflow-providers-zendesk
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the Zendesk provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create an HTTP connection**

- [ ]  Create a connection in one of the following ways:
- Go to Admin > Connections in the Airflow UI, fill in:
    - `Connection ID`: `zendesk_default`
    - `Connection type`: `Zendesk`
    - `Login`: your login
    - `Password`: your password
    - `Host`: your Zendesk URL
- ****OR**** add a connection in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)
    - using login and password:

        ```docker
        export AIRFLOW_CONN_ZENDESK_DEFAULT=zendesk://<your-login>:<your-password>@<your-host>
        ```

    - using token:

        ```docker
        export AIRFLOW_CONN_ZENDESK_DEFAULT=zendesk://<your-login>%2Ftoken:<your-token>@<your-host>/https
        ```


**Use ZendeskHook**

- [ ]  Create the following DAG (add `interact_with_zendesk.py` file to your `dags` directory):

```python
import pendulum
from datetime import timedelta, datetime

from airflow import DAG
from airflow.decorators import task
from airflow.providers.zendesk.hooks.zendesk import ZendeskHook

default_args = {
    "owner": "cs",
    "retries": 3,
    "retry_delay": timedelta(seconds=15),
    }

with DAG(
    dag_id="interact_with_zendesk",
    start_date=pendulum.datetime(2022, 11, 1, tz="UTC"),
    schedule=None,
):

    @task
    def fetch_ticket_ids(**kwargs):
        hook = ZendeskHook(zendesk_conn_id="zendesk_default")
        ds = datetime.strptime(kwargs.get("ds"), "%Y-%m-%d")
        day_ago = ds - timedelta(days=1)
        tickets = hook.search_tickets(created_between=[day_ago, ds])
        for ticket in tickets:
            print(ticket)

    fetch_ticket_ids()
```

- [ ]  Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `fetch_ticket_ids` task, you should see something similar:

```python
{logging_mixin.py:137} INFO - Ticket(id=14439)
{logging_mixin.py:137} INFO - Ticket(id=14438)
{logging_mixin.py:137} INFO - Ticket(id=14437)
```

**Checkpoint**

At this point you should:

- Have a working Zendesk connection
- Run example task successfully in the DAG