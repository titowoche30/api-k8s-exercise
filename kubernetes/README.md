# Cluster

## Creation
### Using kind
```shell
$ kind create cluster --config kubernetes/kind/kind-nodes-config.yml
```
```shell
$ kubectl cluster-info --context kind-kind
```

### Using eksctl
```shell
$ eksctl create cluster --config-file=./kubernetes/eksctl/cluster.yaml
$ aws eks update-kubeconfig --region us-east-1 --name cwoche-cluster --role-arn arn:aws:iam::649165755582:role/EKSUserRole --alias cwoche-cluster --user-alias cwoche-dev-role
```
IAM Role definitions on kubernetes/iam

## Development
### Checking cluster
```shell
$ kubectl get nodes -o wide
```

### Creating namespaces
```shell
$ kubectl create namespace cwoche-api
$ kubectl create namespace cwoche-database
$ kubectl create namespace cwoche-nginx
```


# Database
### Switching namespace
```shell
$ kubens cwoche-database
```

### Creating postgres secret
```shell
$ kubectl apply -f kubernetes/manifests/secret_postgres.yaml
```


### Installing postgres chart
```shell
$ helm repo add bitnami https://charts.bitnami.com/bitnami
$ helm show values bitnami/postgresql > postgres_values.yaml
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

# Nginx
### Switching namespace
```shell
$ kubens cwoche-nginx
```

### Creating deployment
```shell
$ kubectl apply -f kubernetes/manifests/deployment-nginx.yaml
```

### Creating service
```shell
$ kubectl apply -f kubernetes/manifests/service-nginx.yaml
```

### Binding port
```shell
$ kubectl port-forward service/nginx 80:80
```

# Extra Components

## Cluster Autoscaler

### Creating components
```shell
$ kubectl apply -f kubernetes/manifests/cluster-autoscaler-autodiscover.yaml
```

## Metrics Server

### Creating components
```shell
$ kubectl apply -f kubernetes/manifests/metrics-server-components.yaml
```

## Ingress - AWS Load Balancer Controller

### Adding helm repo
```shell
$ helm repo add eks https://aws.github.io/eks-charts
```

### Install the TargetGroupBinding CRDs
```shell
$ kubectl apply -f kubernetes/manifests/crds.yaml
```

## Install helm chart
```shell
$ helm install -f kubernetes/helm/aws_load_balancer_controller_values.yaml aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system
```

## External DNS
```shell
$ kubectl apply -f kubernetes/manifests/external-dns.yaml
```

# Destroying cluster

* Delete PVCs. The volumes on AWS won't be deleted by the cluster destruction

```shell
$ eksctl delete cluster --name cwoche-cluster --wait
```

```shell
$ kind delete cluster
```

