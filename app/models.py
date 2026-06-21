import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class StatusTarefa(str, enum.Enum):
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"


class PrioridadeTarefa(str, enum.Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)

    tarefas = relationship("Tarefa", back_populates="usuario", cascade="all, delete-orphan")


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(Text, nullable=True)
    status = Column(Enum(StatusTarefa), default=StatusTarefa.pendente, nullable=False)
    prioridade = Column(Enum(PrioridadeTarefa), default=PrioridadeTarefa.media, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="tarefas")
