from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth_router, tarefas_router, upload_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudTask AI SaaS")

app.include_router(auth_router.router)
app.include_router(tarefas_router.router)
app.include_router(upload_router.router)


@app.get("/health")
def health():
    return {"status": "ok"}
