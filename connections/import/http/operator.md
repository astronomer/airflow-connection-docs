
### Module - HTTP Connection + Operators

**Add HTTP to your Astro project**

- [ ]  Add `apache-airflow-providers-http` to your project’s `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-http
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the HTTP provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create an HTTP connection**

- [ ]  Create a connection in one of the following ways:
- [Add an HTTP connection](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/connections/http.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)

```docker
export AIRFLOW_CONN_HTTP_DEFAULT='http://username:password@servvice.com:80/https?headers=header'
```

- **OR** Go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`http_default`), select `HTTP`as a connection type, and fill in appropriate fields  - you need `host` to start with, `login`, `password`, and `port` may be required as well

**Use SimpleHttpOperator**

- [ ]  Test HTTP operator
- Create the following DAG (add `test_http.py` file to your `dags` directory):

```python
docs = """
    This example sends requests to URL https://goweather.herokuapp.com/weather/NewYork. \n
    Set up an HTTP connection with parameters as follows: \n
    - Connetion ID: http_default \n
    - Connection Type: HTTP \n
    - Host: https://goweather.herokuapp.com/weather/NewYork \n
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator

with DAG(dag_id='test_http',
         start_date=datetime(2022, 7, 1),
         schedule=None,
         doc_md=docs,
         ) as dag:

    test_weather_api = SimpleHttpOperator(
        task_id='test_weather_api',
        method='GET',  # The HTTP method to use, default = “POST”.
        http_conn_id='http_default',
        endpoint='/weather/NewYork',  # The relative part of the full URL.
        headers={"Content-Type": "application/json"},  # The HTTP headers to be added to the GET request.
        log_response=True,
    )
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run
- [ ]  Check the logs of `test_weather_api` task, you should see the following:

```python
{http.py:102} INFO - Calling HTTP method
{base.py:68} INFO - Using connection ID 'http_default' for task execution.
{http.py:129} INFO - Sending 'GET' to url: https://goweather.herokuapp.com/weather/NewYork
{http.py:106} INFO - {"temperature":"+26 °C","wind":"11 km/h","description":"Partly cloudy","forecast":[{"day":"1","temperature":"+35 °C","wind":"22 km/h"},{"day":"2","temperature":"25 °C","wind":"18 km/h"},{"day":"3","temperature":" °C","wind":"17 km/h"}]}
```

**Checkpoint**

At this point you should:

- Have a working HTTP connection
- Run an example task successfully in the DAG and the logs of the task should contain the expected response

**Extras / Reference**

- References


    ### HTTP

    [HTTP Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/connections/http.html)

    [HttpHook | Astronomer Registry](https://registry.astronomer.io/providers/http/modules/httphook/)

    [HttpSensor | Astronomer Registry](https://registry.astronomer.io/providers/http/modules/httpsensor)

    [SimpleHttpOperator | Astronomer Registry](https://registry.astronomer.io/providers/http/modules/simplehttpoperator)

