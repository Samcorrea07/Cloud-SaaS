# CloudTask AI SaaS

Backend FastAPI para gerenciamento de tarefas com autenticacao JWT e upload de arquivos (local ou S3).

## Requisitos

- Docker
- Docker Compose

## Como rodar

1. Copie o arquivo de exemplo de variaveis de ambiente:

   ```bash
   cp .env.example .env
   ```

2. Suba os servicos:

   ```bash
   docker-compose up --build
   ```

3. A API estara disponivel em `http://localhost:8000`.

   - Documentacao interativa (Swagger): `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

## Endpoints principais

- `POST /auth/registrar` — cria um novo usuario
- `POST /auth/login` — autentica e retorna um token JWT
- `GET /tarefas` — lista as tarefas do usuario autenticado
- `POST /tarefas` — cria uma tarefa
- `GET /tarefas/{id}` — detalha uma tarefa
- `PUT /tarefas/{id}` — atualiza uma tarefa
- `DELETE /tarefas/{id}` — remove uma tarefa
- `POST /upload` — envia um arquivo (multipart/form-data) e retorna a URL

Todas as rotas de `/tarefas` e `/upload` exigem o header `Authorization: Bearer <token>`.

## Armazenamento de arquivos

Por padrao os uploads sao salvos localmente na pasta `uploads/`. Para usar Amazon S3,
defina no `.env`:

```env
STORAGE_BACKEND=s3
AWS_S3_BUCKET=seu-bucket
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```
