
### Module - SFTP Connection + Operators

**Before You Start**

- [ ]  Have either [a host key](https://pysftp.readthedocs.io/en/release_0.2.9/pysftp.html#pysftp.CnOpts) or a full path of the private SSH Key file that will be used to connect to the remote host along with the password

<aside>
💡 There are two ways to connect to SFTP using Airflow (only one method can be used at a time):
    1. Use host key i.e. host key entered in extras value `host_key`.
    2. Use `private_key` or `key_file`, along with the optional `private_key_pass`.

</aside>

**Add SFTP to your Astro project**

- [ ]  Add `apache-airflow-providers-sftp` to your `requirements.txt`

```bash
$ cat requirements.txt
apache-airflow-providers-sftp
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the SFTP provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Create an SFTP connection**

- [ ]  Create a connection in one of the following ways:
- [Add an SFTP connection](https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/connections/sftp.html) in your Dockerfile, a Secrets Backend, or via [Env Variables](https://docs.astronomer.io/astro/environment-variables)
    - Connection string with `key_file`:

    ```java
    export AIRFLOW_CONN_SFTP_DEFAULT='sftp://user:pass@localhost:22?key_file=%2Fhome%2Fairflow%2F.ssh%2Fid_rsa'
    ```

    - Connection string with `host_key`:

    ```java
    export AIRFLOW_CONN_SFTP_DEFAULT='sftp://user:pass@localhost:22?host_key=AAAHD...YDWwq%3D%3D&no_host_key_check=false'
    ```

- **OR** Go to Admin > Connections in the Airflow UI, fill in `Connection ID` field (`sftp_default`), select `SFTP` as a connection type, and fill in appropriate fields: `login`, `password`, `port`, `host`, and in `extra`:
    - if using `host_key`:

    ```json
    {
       "no_host_key_check": "false",
       "allow_host_key_change": "false",
       "host_key": "AAAHD...YDWwq=="
    }
    ```

    - if using `key_file` or `private_key`:

    ```json
    {
       "key_file": "path/to/private_key",
       "no_host_key_check": "true"
    }
    ```


**Use SFTPSensor**

- [ ]  Test SFTP operator
- Create the following DAG (add `test_sftp.py` file to your `dags` directory):

```python
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.sftp.sensors.sftp import SFTPSensor

with DAG(
    dag_id='test_sftp',
    start_date=datetime(2022, 7, 1),
    schedule=None,
) as dag:

    wait_for_file = SFTPSensor(
        task_id='wait_for_file',
        sftp_conn_id='sftp_default',
        path='/tmp/single-file/customers.csv',  # Remote file or directory path.
        mode='reschedule',  # Worker slot will be released when the criteria is not met yet and rescheduled at a later time.
        poke_interval=15,  # Time in seconds that the job should wait in between each tries.
        timeout=60,  # Time, in seconds before the task times out and fails.
    )
```

- Run it locally or deploy to Astro and hit the ▶️ `Trigger DAG` button to see a successful run

**Checkpoint**

At this point you should:

- Have a working SFTP connection
- Run an example task successfully in the DAG

**Extras / Reference**

- Reference


    ### SFTP

    - [SFTP Connection | Airflow OSS Doc](https://airflow.apache.org/docs/apache-airflow-providers-sftp/stable/connections/sftp.html)
    - [SFTPToS3Operator | Astronomer Registry](https://registry.astronomer.io/providers/amazon/modules/sftptos3operator)
    - [SFTPToGCSOperator | Astronomer Registry](https://registry.astronomer.io/providers/google/modules/sftptogcsoperator)
    - [SFTPOperator | Astronomer Registry](https://registry.astronomer.io/providers/sftp/modules/sftpoperator)
    - [SFTPSensor | Astronomer Registry](https://registry.astronomer.io/providers/sftp/modules/sftpsensor)
    - [SFTPHook | Astronomer Registry](https://registry.astronomer.io/providers/sftp/modules/sftphook)
