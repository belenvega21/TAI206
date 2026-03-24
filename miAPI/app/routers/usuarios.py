from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario
from app.models.usuario import UsuarioBase

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

#  CONSULTAR USUARIOS
@router.get("/", status_code=status.HTTP_200_OK)
def leer_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()

    return {
        "total": len(usuarios),
        "data": [
            {
                "id": u.id,
                "nombre": u.nombre,
                "edad": u.edad
            } for u in usuarios
        ]
    }


#  AGREGAR USUARIO
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):

    nuevoUsuario = Usuario(
        nombre=usuario.nombre,
        edad=usuario.edad
    )

    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return {
        "message": "Usuario agregado exitosamente",
        "data": {
            "id": nuevoUsuario.id,
            "nombre": nuevoUsuario.nombre,
            "edad": nuevoUsuario.edad
        }
    }


# ACTUALIZAR USUARIO
@router.put("/{id}", status_code=status.HTTP_200_OK)
def actualizar_usuario(id: int, usuario_actualizado: UsuarioBase, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = usuario_actualizado.nombre
    usuario.edad = usuario_actualizado.edad

    db.commit()
    db.refresh(usuario)

    return {
        "message": "Usuario actualizado",
        "data": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad
        }
    }


#  ELIMINAR USUARIO
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "message": "Usuario eliminado",
        "data": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad
        }
    }