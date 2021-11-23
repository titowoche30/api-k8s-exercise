# Cluster
### Creating local
```shell
$ kind create cluster --config kind/kind-nodes-config.yml
```

### Setting context
```shell
$ kubectl cluster-info --context kind-kind
```

### Checking cluster
```shell
$ kubectl get nodes
```

### Creating namespaces
```shell
$ kubectl create namespace cwoche-api
$ kubectl create namespace cwoche-database
```


# Database
### Switching namespace
```shell
$ kubens cwoche-database
```

### Creating postgres secret
```shell
$ kubectl apply -f kubernetes/manifest/secret_postgres.yaml
```


### Installing postgres chart
```shell
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm show values bitnami/postgres > postgres_values.yml
- Change the global.postgresql.existingSecret with the name of the secret
$ helm install -f postgres_values.yml cwoche-postgres bitnami/postgresql
$ helm ls
```
### obs: 
PostgreSQL can be accessed via port 5432 on the following DNS names from within your cluster:

cwoche-postgres-postgresql.cwoche-database.svc.cluster.local - Read/Write connection

service_name.namespace.svc.cluster.local 


# API
### Switching namespace
```shell
$ kubens cwoche-api
```

### Creating postgres secret
```shell
$ kubectl apply -f kubernetes/manifests/secret_api.yaml
```

### Creating deployment
```shell
$ kubectl apply -f kubernetes/manifests/deployment.yaml
```

### Creating service
```shell
$ kubectl apply -f kubernetes/manifests/service.yaml
```

### Binding port
```shell
$ kubectl port-forward service/service-fastapi 8000:8000
```

### Destroying cluster
```shell
$ kind delete cluster
```
