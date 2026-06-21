# CloudTask AI SaaS — Deploy no Kubernetes

Manifests para rodar a API em um cluster Kubernetes local
(Minikube, kind, Docker Desktop, etc.). O banco de dados é um PostgreSQL
externo (Amazon RDS), referenciado pelo `DATABASE_URL` no Secret.

## 1. Buildar a imagem com a tag certa

Os manifests usam a imagem `cloudtask-api:latest` com `imagePullPolicy: Never`,
ou seja, o cluster **não** baixa de um registry — a imagem precisa existir
localmente no nó onde o pod vai rodar.

Na raiz do projeto (onde está o `Dockerfile`):

```bash
docker build -t cloudtask-api:latest .
```

### Minikube

O Minikube usa um Docker próprio, separado do host. Antes de buildar, aponte o
Docker para dentro do Minikube:

```bash
eval $(minikube docker-env)
docker build -t cloudtask-api:latest .
```

### kind

Builde no host e carregue a imagem para dentro do cluster:

```bash
docker build -t cloudtask-api:latest .
kind load docker-image cloudtask-api:latest
```

## 2. Preencher o Secret com suas credenciais

O arquivo `k8s/secret.yaml` **não** é versionado (está no `.gitignore`), para não
expor credenciais no repositório. Use o modelo `k8s/secret.yaml.example` como base:
copie-o e preencha com as **suas próprias** credenciais (senha do RDS, `SECRET_KEY`
e as chaves AWS do seu Learner Lab) antes de aplicar.

```bash
cp k8s/secret.yaml.example k8s/secret.yaml
```

Edite `k8s/secret.yaml` substituindo os placeholders (`SUA_SENHA_AQUI`,
`SEU_ACCESS_KEY_AQUI`, etc.) pelos valores reais.

## 3. Aplicar os manifests

Aplique tudo de uma vez:

```bash
kubectl apply -f k8s/
```

Isso cria, na ordem resolvida pelo Kubernetes:

- `cloudtask-secret` (Secret) — `DATABASE_URL` (RDS), `SECRET_KEY` e credenciais AWS/S3
- `cloudtask-api` (Deployment, 2 réplicas) + `cloudtask-api` (Service NodePort) — API

Acompanhe a subida dos pods:

```bash
kubectl get pods -w
```

A API tem `readinessProbe` e `livenessProbe` em `/health`, então cada réplica só
entra em serviço depois que o `/health` responder.

## 4. Acessar a API

O Service da API é do tipo `NodePort` na porta `30080`.

### Minikube

```bash
minikube service cloudtask-api --url
```

Use a URL retornada, por exemplo:

```bash
curl $(minikube service cloudtask-api --url)/health
```

### kind / Docker Desktop

Acesse via porta do nó:

```bash
curl http://localhost:30080/health
```

Documentação interativa (Swagger): `http://<host>:30080/docs`

## Limpar tudo

```bash
kubectl delete -f k8s/
```
