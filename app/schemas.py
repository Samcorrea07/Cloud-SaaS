from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import PrioridadeTarefa, StatusTarefa


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: EmailStr


class TarefaCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: StatusTarefa = StatusTarefa.pendente
    prioridade: PrioridadeTarefa = PrioridadeTarefa.media


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[StatusTarefa] = None
    prioridade: Optional[PrioridadeTarefa] = None


class TarefaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: Optional[str] = None
    status: StatusTarefa
    prioridade: PrioridadeTarefa
    usuario_id: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
