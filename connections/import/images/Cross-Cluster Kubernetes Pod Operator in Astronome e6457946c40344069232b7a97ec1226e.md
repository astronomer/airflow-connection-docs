# Cross-Cluster Kubernetes Pod Operator in Astronomer Cloud

![XCluster KPO.png](Cross-Cluster%20Kubernetes%20Pod%20Operator%20in%20Astronome%20e6457946c40344069232b7a97ec1226e/XCluster_KPO.png)

# 0) Requirements

- A network-reachable Kubernetes Cluster (*target cluster*) must be already provisioned
- A Service Account or other authentication mechanism in the target cluster
- An Astronomer Deployment created after 6/29/2022

<aside>
⚠️ This feature will only work with Astronomer Cloud Deployments **created after June 29th 2022**. Deployments created earlier will need to be ***recreated***

</aside>

# 1) Obtain or Create `KUBECONFIG`

## Option A) Creating Service Account in Target Cluster + `KUBECONFIG`

- Requires: permission to create service account, role, rolebinding (and a namespace, or an existing namespace)

```bash
# https://www.journaldev.com/52730/configuring-service-account-tokens-kubeconfig

# Create namespace
kubectl create namespace kpo-test  # <--- change this to an existing namespace or change the name

# Create service account, role, rolebinding
kubectl create serviceaccount --namespace kpo-test kpo-test
kubectl create role kpo-test --namespace kpo-test --verb=get --verb=list --verb=patch --verb=delete --verb=create --verb=watch --resource=pods --resource=pods/log
kubectl create rolebinding --serviceaccount=kpo-test:kpo-test --role=kpo-test --namespace=kpo-test kpo-test

# Fetch service account secret name and token from service account secret
SECRET=$(kubectl -n kpo-test get serviceaccount/kpo-test -o jsonpath='{.secrets[0].name}')
TOKEN=$(kubectl -n kpo-test get secret $SECRET -o jsonpath='{.data.token}' | base64 --decode)

# Create new KUBECONFIG file
touch kpo-test-kubeconfig
kubectl --kubeconfig=kpo-test-kubeconfig config set-credentials kpo-test --token=$TOKEN
kubectl --kubeconfig=kpo-test-kubeconfig config set-cluster kpo-test --server=https://????????????????????????.??.us-east-1.eks.amazonaws.com
kubectl --kubeconfig=kpo-test-kubeconfig config set-context --current kpo-test --user=kpo-test
kubectl --kubeconfig=kpo-test-kubeconfig config use-context kpo-test
```

## Option B) Using EKS KUBECONFIG or similar

- You can have `AWS` authenticate to a target EKS cluster for you, instead, if you are using EKS.
    - GKE is similar
- You will need to have AWS installed in `packages.txt` (or installed some other way)

```
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: <certificate-key>
    server: https://???????????????????.gr7.us-east-2.eks.amazonaws.com
  name: arn:aws:eks:us-east-1:?????:cluster/my_cluster

contexts:
- context:
    cluster: arn:aws:eks:us-east-1:?????:cluster/my_cluster
    user: arn:aws:eks:us-east-1:?????:cluster/my_cluster
  name: arn:aws:eks:us-east-1:?????:cluster/my_cluster
current-context: arn:aws:eks:us-east-1:?????:cluster/my_cluster
kind: Config
preferences: {}
users:
- name: arn:aws:eks:us-east-1:?????:cluster/my_cluster
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1alpha1
      args:
      - --region
      - us-east-1
      - eks
      - get-token
      - --cluster-name
      - my_cluster
      - --profile
      - default
      command: aws 
      interactiveMode: IfAvailable
      provideClusterInfo: false 
```

# 2) Create Airflow Kubernetes Connection + KPO

## Option A) Embed in Dockerfile + KPO

- Copy `KUBECONFIG` file (e.g. as produced above) into `/include`
- For this method, with a  `KubernetesPodOperator` , you will need to include

```python
KubernetesPodOperator(
    ...
    cluster_context='???',
    namespace='???',
    in_cluster=False,
		labels={"airflow_kpo_in_cluster": "False"},
    config_file='/usr/local/airflow/include/kube_config'
)
```

## Option B) Kubernetes Airflow Connection + KPO

<aside>
⚠️ This option requires `apache-airflow-providers-cncf-kubernetes==4.1.0` or greater

</aside>

- Create an Airflow Connection (via any method - in the Airflow UI, Astronomer UI as an Env variable, Dockerfile, or Secrets Backend)

```
# Get new KUBECONFIG file as url-escaped & compacted string
KC=$(python -c 'import sys, urllib.parse, yaml; print(urllib.parse.quote(yaml.dump(yaml.safe_load(open(sys.argv[1])))))' kpo-test-kubeconfig)

# Create Airflow connection named "KUBERNETES"
echo "AIRFLOW_CONN_KUBERNETES='kubernetes://?extra__kubernetes__kube_config=$KC'"
```

- For this method, with a  `KubernetesPodOperator` , you will need to include

```python
KubernetesPodOperator(
    ...
    kubernetes_conn_id="kubernetes",
    namespace='???',
    in_cluster=False,
		labels={"airflow_kpo_in_cluster": "False"},
)
```

# Final Notes

- Also worthy of mention `EksPodOperator` and `GKEStartPodOperator`

[Amazon Elastic Kubernetes Service (EKS) - apache-airflow-providers-amazon Documentation](https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/eks.html#perform-a-task-on-an-amazon-eks-cluster)

- At the next Kubernetes Provider release - `labels={"airflow_kpo_in_cluster": "False"}` will no longer be required as Airflow will set it