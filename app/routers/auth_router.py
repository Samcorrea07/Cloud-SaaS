from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import criar_token, hash_senha, verificar_senha
from app.database import get_db
from app.models import Usuario
from app.schemas import Token, UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/registrar", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar(dados: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ja cadastrado"
        )
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_token({"sub": str(usuario.id)})
    return Token(access_token=token)
