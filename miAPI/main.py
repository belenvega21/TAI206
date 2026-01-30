# IMPORTACIONES
from fastapi import FastAPI
import asyncio
from typing import Optional

# INICIALIZACIÓN
app = FastAPI(
    title='Mi primera API',
    description='Belén Vega está escribiendo',
    version='1.0'
)

# LISTA DE USUARIOS
usuarios = [
    {"id": 1, "nombre": "BELÉN VEGA", "edad": 20},
    {"id": 2, "nombre": "LUPITA", "edad": 20},
    {"id": 3, "nombre": "VICTOR", "edad": 21},
]

# ENDPOINTS

@app.get("/", tags=['INICIO'])
async def HolaUPQ():
    return {"mensaje": "Hola UPQ, estoy en FastAPI"}


@app.get("/bienvenidos", tags=['INICIO'])
async def bienvenidos():
    return {"mensaje": "Bienvenidos a tu API REST"}


@app.get("/v1/calificaciones", tags=['ASINCRONIA'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje": "Tu calificación en TAI es 10"}


# PARÁMETRO OBLIGATORIO
@app.get("/v1/usuarios/{id}", tags=['PARAMETRO OBLIGATORIO'])
async def consultaUsuarios(id: int):
    await asyncio.sleep(3)
    return {
        "mensaje": "USUARIO ENCONTRADO",
        "id": id
    }


# PARÁMETRO OPCIONAL
@app.get("/v1/usuarios_op/", tags=['PARAMETRO OPCIONAL'])
async def consultaOP(id: Optional[int] = None):
    await asyncio.sleep(3)
    if id is not None: 
        for usuarios in usuarios:
            if usuarios["id"] == id:
                return { "USUARIO ENCONTRADO":id,  
                    "Datos": usuarios
                }

    if id is not None:
        return { "mensaje": "USUARIO ENCONTRADO", }

    return {
        "mensaje": "No se envió ningún ID"
    }


 