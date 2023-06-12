# api-k8s-exercise
A simple Python API using Postgres and K8S.

### Local development

```shell
docker run --name postgres-fastapi --rm -d -p 5432:5432 --env POSTGRES_PASSWORD=postgres postgres:13
```

```shell
cd app && uvicorn main:app --host 0.0.0.0 --port 8000
```