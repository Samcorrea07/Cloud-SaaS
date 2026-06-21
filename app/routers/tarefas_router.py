from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_usuario_atual
from app.database import get_db
from app.models import Tarefa, Usuario
from app.schemas import TarefaCreate, TarefaOut, TarefaUpdate

router = APIRouter(prefix="/tarefas", tags=["tarefas"])


def buscar_tarefa(tarefa_id: int, usuario: Usuario, db: Session) -> Tarefa:
    tarefa = (
        db.query(Tarefa)
        .filter(Tarefa.id == tarefa_id, Tarefa.usuario_id == usuario.id)
        .first()
    )
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa nao encontrada"
        )
    return tarefa


@router.post("", response_model=TarefaOut, status_code=status.HTTP_201_CREATED)
def criar_tarefa(
    dados: TarefaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    tarefa = Tarefa(**dados.model_dump(), usuario_id=usuario.id)
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.get("", response_model=List[TarefaOut])
def listar_tarefas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    return db.query(Tarefa).filter(Tarefa.usuario_id == usuario.id).all()


@router.get("/{tarefa_id}", response_model=TarefaOut)
def obter_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    return buscar_tarefa(tarefa_id, usuario, db)


@router.put("/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa(
    tarefa_id: int,
    dados: TarefaUpdate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    tarefa = buscar_tarefa(tarefa_id, usuario, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual),
):
    tarefa = buscar_tarefa(tarefa_id, usuario, db)
    db.delete(tarefa)
    db.commit()
