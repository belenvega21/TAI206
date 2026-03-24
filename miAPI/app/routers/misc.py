from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario
from app.models.usuario import UsuarioBase

router = APIRouter(
    prefix="/misc",
    tags=["Misc"]
)

#  AGREGAR USUARIO 
@router.post("/usuarios", status_code=status.HTTP_201_CREATED)
def agregar_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):

    # VALIDACIÓN (opcional, por nombre)
    existente = db.query(Usuario).filter(Usuario.nombre == usuario.nombre).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    # CREAR USUARIO
    nuevo = Usuario(
        nombre=usuario.nombre,
        edad=usuario.edad
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "message": "Usuario agregado desde misc",
        "data": {
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "edad": nuevo.edad
        }
    }