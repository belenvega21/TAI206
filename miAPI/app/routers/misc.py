from typing import Optional
from fastapi import APIRouter, HTTPException
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
import asyncio  

router = APIRouter(
    prefix="/v1",
    tags=["Varios"],
    
)

# CONSULTAR TODOS LOS USUARIOS
@router.get("/usuarios")
async def consultar_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

# CONSULTAR POR ID (OBLIGATORIO)
@router.get("/usuarios/{id}")
async def consultar_usuario(id: int):
    await asyncio.sleep(2)
    
    for usuario in usuarios:
        if usuario["id"] == id:
            return {
                "Usuario consultado": id,
                "Datos": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# CONSULTA OPCIONAL
@router.get("/usuarios")
async def consulta_opcional(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {"Datos": usuario}
        return {"mensaje": "Usuario no encontrado"}

    return {"aviso": "No se proporcionó ID"}

# AGREGAR USUARIO
@router.post("/usuarios")
async def agregar_usuario(usuario: UsuarioBase):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El ID ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado",
        "data": usuario
    }