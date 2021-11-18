# Cluster
## Creating local
```shell
$ kind create cluster --config kind/kind-nodes-config.yml
```

## Checking cluster
```shell
$ kubectl get nodes
```

## Creating namespaces
```shell
$ kubectl create namespace cwoche-api
$ kubectl create namespace cwoche-database
```


# Database
## Switching namespace
```shell
$ kubens cwoche-database
```

## Creating postgres secret
```shell
$ kubectl apply -f kubernetes/secret_postgres.yaml
```


## Installing postgres chart
```shell
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm show values bitnami/postgres > postgres_values.yml
- Change the global.postgresql.existingSecret with the name of the secret
$ helm install -f postgres_values.yml cwoche-postgres bitnami/postgresql
$ helm ls
```

# API
## Switching namespace
```shell
$ kubens cwoche-api
```

## Creating postgres secret
```shell
$ kubectl apply -f kubernetes/secret_api.yaml
```

## Creating deployment
```shell
$ kubectl apply -f kubernetes/deployment.yaml
```

## Creating service
```shell
$ kubectl apply -f kubernetes/service.yaml
```

## Binding port
```shell
$ kubectl port-forward service/service-fastapi 8000:8000
```

## Rollout on deployment
```shell
$ kubectl rollout undo deployment deployment-fastapi
```

