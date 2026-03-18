import asyncio
from app.models.usuario import UsuarioBase
from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.security.auth import verificar_peticion


router = APIRouter(
    prefix="/v1/usuarios",
    tags=["CRUD HTTP"]
)


# CRUD - CONSULTAR USUARIOS
@router.get("/", status_code=status.HTTP_200_OK)
async def consultar_usuarios():
    return {
        "total": len(usuarios),
        "data": usuarios
    }


# CRUD - AGREGAR USUARIO
@router.post("/", status_code=status.HTTP_201_CREATED)
async def agregar_usuario(usuario: UsuarioBase):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El ID del usuario ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "message": "Usuario agregado exitosamente",
        "datos": usuario
    }


# CRUD - ACTUALIZAR USUARIO
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    await asyncio.sleep(2)

    for usuario in usuarios:
        if usuario["id"] == id:
            usuario["nombre"] = usuario_actualizado.get("nombre", usuario["nombre"])
            usuario["edad"] = usuario_actualizado.get("edad", usuario["edad"])

            return {
                "message": "Usuario actualizado exitosamente",
                "data": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# CRUD - ELIMINAR USUARIO
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    await asyncio.sleep(2)

    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "message": "Usuario eliminado exitosamente",
                "data": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )