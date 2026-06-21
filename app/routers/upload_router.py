from fastapi import APIRouter, Depends, File, UploadFile

from app.auth import get_usuario_atual
from app.models import Usuario
from app.storage import get_storage

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("")
def upload(
    file: UploadFile = File(...),
    usuario: Usuario = Depends(get_usuario_atual),
):
    storage = get_storage()
    url = storage.save(file)
    return {"url": url}
