
### Module - KubernetesPodOperator Connection + Operators

Kubernetes is a Container Orchestration framework (similar to how Airflow is a Task Orchestration framework).  Astronomer Cloud is software that runs on Kubernetes and therefore Airflow can run Kubernetes Pods inside your Astronomer Cloud Kubernetes Cluster.

You can also launch Kubernetes Pods into external clusters for greater control, monitoring, and customization (that will, however, be outside the scope of this Module)

**Before You Start**

- Have a Kubernetes Cluster or understand your usage of the Astronomer Cloud Kubernetes cluster
- Have an existing Docker image built, and a pipeline to build it if it is your custom image
- [Have Docker Desktop (for Mac or Windows) or an equivalent running locally](https://docs.astronomer.io/astro/kubepodoperator-local#step-1-set-up-kubernetes)

****

**Add Kubernetes to your Astro project**

- [ ]  Add `apache-airflow-providers-cncf-kubernetes` to your project’s `requirements.txt` file

```bash
$ cat requirements.txt
apache-airflow-providers-cncf-kubernetes
```

<aside>
💡 If you are running Airflow locally, you’ll need to restart the project so that the HTTP provider is installed. You can restart your project using `astro dev restart`.

</aside>

**Test launching a Kubernetes Pod**

- [ ]  Add a Kubernetes Airflow Connection to your `.env` for your Local Airflow
    - However you run Kubernetes locally - Minikube, Docker Desktop, Rancher Desktop - should create an entry in `~/.kube/config`, or some similar file. Change the file referenced in the first snippet if yours is different

        <aside>
        ⚠️ **Note for Minikube on Linux:**
        If your `~/.kube/config` file mentions `~/.minikube`, you will need to mount this file into your image. You can do this by making a file called `docker-compose.override.yml`
        with the contents below (make sure you replace `MY_USER` with what is mentioned in `~/.kube/config`. You can read more about [docker-compose.override.yml here](https://docs.astronomer.io/astro/test-and-troubleshoot-locally#override-the-cli-docker-compose-file)

        ```python
        version: "3.1"
        services:
          scheduler:
            volumes:
              - /home/MY_USER/.minikube/:/home/MY_USER/.minikube/:ro

          webserver:
            volumes:
              - /home/MY_USER/.minikube/:/home/MY_USER/.minikube/:ro

        ```

        </aside>

    - **Note**: you may need to `pip install pyyaml` and you will need Python 3 to run the first snippet
    - **Note**: In the second snippet below - the connection is named `KUBERNETES`, feel free to name it anything that makes sense. Additionally, we set `in_cluster=False` and `namespace=default`
    - Run both of the following:

        ```bash
        KC=$(python -c "import sys, urllib.parse, yaml; print(urllib.parse.quote(yaml.dump(yaml.safe_load(open(sys.argv[1]))).replace('127.0.0.1', 'host.docker.internal')))" ~/.kube/config)
        ```

        ```bash
        echo "AIRFLOW_CONN_KUBERNETES='kubernetes://?extra__kubernetes__namespace=default&extra__kubernetes__kube_config=$KC'"
        ```

    - Add the output of the second snippet as an Airflow Connection to your `.env`
    - Run `astro dev restart` if your local Airflow was running, or `astro dev start` to run it and get the new connection from `.env`
- [ ]  Add a Kubernetes Airflow Connection to your Astronomer Cloud Airflow
    - [Follow this guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html#creating-a-connection-with-the-ui) to create an [Airflow Connection](https://airflow.apache.org/docs/apache-airflow/stable/concepts/connections.html).
        - This connection can be [a secret Astronomer Environmental Variable](https://docs.astronomer.io/astro/environment-variables#set-environment-variables-via-the-cloud-ui)
        - Optionally: you can add it any other way you would add a connection, such as with the Airflow UI or a Secrets Backend
    - This connection will be similar to the Local connection, but simpler, as we will already be *inside* the Kubernetes Cluster, nothing else will need to be set

        ```bash
        AIRFLOW_CONN_KUBERNETES='kubernetes://?extra__kubernetes__in_cluster=True'
        ```

- [ ]  Create a DAG called `dags/example_kpo.py`

    ```python
    from datetime import datetime

    from airflow.configuration import conf
    from airflow.decorators import dag
    from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

    @dag(
        schedule=None,
        start_date=datetime(2021, 1, 1),
        catchup=False
    )
    def example_kpo():
        KubernetesPodOperator(
            kubernetes_conn_id="kubernetes",
            namespace=conf.get('kubernetes', 'NAMESPACE'),
    				log_events_on_failure=True,
            task_id="kpo-test",
            name="kpo-test",
            image="ubuntu",
            cmds=["echo"],
            arguments=["hi"]
        )

    example_kpo_dag = example_kpo()
    ```

- [ ]  Run the DAG in the Airflow UI locally (against a local Kubernetes) and in Astronomer Cloud (in cluster)

**Checkpoint**

- You’ve now successfully run an `ubuntu` pod locally and in your Astronomer Cloud Kubernetes cluster

**Next Steps**

- Integrate the `KubernetesPodOperator` into your workload
- To run a private registry image in the `KubernetesPodOperator` , contact your Customer Success Engineer and Astronomer Support team to follow this document:

    [Run the KubernetesPodOperator on Astro | Astronomer Documentation](https://docs.astronomer.io/astro/kubernetespodoperator#run-images-from-a-private-registry)

- To run a `KubernetesPodOperator` task in an External Kubernetes Cluster, contact your Customer Success Engineer about specifics. Note that you can turn your `~/.kube/config.yaml` file into an Airflow Kubernetes Connection

**Extras / Reference**

- Reference


    ### Kubernetes

    - [Kubernetes 101 | Astronomer Guide](https://www.astronomer.io/guides/intro-to-kubernetes)
    - [Kubernetes - Hook & Operator | Astronomer Registry](https://registry.astronomer.io/providers/kubernetes)
