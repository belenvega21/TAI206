from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario
from app.models.usuario import UsuarioBase

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)

#  GET TODOS
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


# GET POR ID
@router.get("/{id}", status_code=status.HTTP_200_OK)
def obtener_usuario(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "data": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad
        }
    }


#  POST
@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioBase, db: Session = Depends(get_db)):

    nuevo = Usuario(
        nombre=usuario.nombre,
        edad=usuario.edad
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return {
        "message": "Usuario creado",
        "data": {
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "edad": nuevo.edad
        }
    }


# PUT 
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


# PATCH ACTUALIZA 
@router.patch("/{id}", status_code=status.HTTP_200_OK)
def actualizar_parcial(id: int, usuario_data: dict, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if "nombre" in usuario_data:
        usuario.nombre = usuario_data["nombre"]

    if "edad" in usuario_data:
        usuario.edad = usuario_data["edad"]

    db.commit()
    db.refresh(usuario)

    return {
        "message": "Usuario actualizado parcialmente",
        "data": {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "edad": usuario.edad
        }
    }


# DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_usuario(id: int, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.id == id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {
        "message": "Usuario eliminado"
    }
    
    