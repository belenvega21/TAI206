from fastapi import FastAPI, HTTPException, status, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# CREAR LA APLICACIÓN
app = FastAPI(
    title="MI PRIMER API",
    description="Una API simple para gestionar calificaciones en TAI",
    version="1.0"
)


# DATOS EN MEMORIA
usuarios = [
    {"id": 1, "nombre": "Belén Vega", "edad": 20},
    {"id": 2, "nombre": "Gabriel Villafuerte", "edad": 24},
    {"id": 3, "nombre": "Lu Malagon", "edad": 21}
]


# MODELO PYDANTIC
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, example=4)
    nombre: str = Field(..., min_length=3, max_length=50, example="Vivi López")
    edad: int = Field(..., ge=0, le=121, example=22)



# ENDPOINTS DE INICIO

@app.get("/", tags=["Inicio"])
async def hola_mundo():
    return {"mensaje": "Hola Mundo FastAPI a TAI"}


@app.get("/v1/bienvenidos", tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenido a TAI"}



@app.get("/v1/calificaciones", tags=["Asincronía"])
async def calificaciones():
    await asyncio.sleep(2)
    return {"mensaje": "Tu calificación en TAI es 10"}


@app.get("/v1/ParametroO", tags=["Parámetro obligatorio"])
async def consulta_parametro_obligatorio(id: int):
    await asyncio.sleep(2)
    return {"Usuario consultado": id}


@app.get("/v1/ParametroOP", tags=["Parámetro opcional"])
async def consulta_parametro_opcional(id: Optional[int] = None):
    await asyncio.sleep(2)

    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return {
                    "Usuario consultado": id,
                    "Datos": usuario
                }
        return {"mensaje": "Usuario no encontrado"}
    else:
        return {"aviso": "No se proporcionó ningún ID de usuario"}


# CRUD - CONSULTAR USUARIOS
@app.get("/v1/Usuarios", tags=["CRUD usuarios"])
async def consultar_usuarios():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }


# CRUD - AGREGAR USUARIO Pydantic
@app.post("/v1/Usuarios", tags=["CRUD usuarios"])
async def agregar_usuario(usuario: UsuarioBase):

    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El ID del usuario ya existe"
            )

    usuarios.append(usuario.dict())

    return {
        "status": "200",
        "message": "Usuario agregado exitosamente",
        "datos": usuario
    }




#SEGURIDAD CON HTTP BASIC 
security = HTTPBasic() 
def verificar_Peticion (credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth= secrets.compare_digest(credentials.username, "admin")
    contraAuth= secrets.compare_digest(credentials.password, "belenvega")
    
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
        
    return credentials.username 
    
    
    




# CRUD - ACTUALIZAR USUARIO
@app.put("/v1/Usuarios/{id}", tags=["CRUD usuarios"])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    await asyncio.sleep(2)

    for usuario in usuarios:
        if usuario["id"] == id:
            usuario["nombre"] = usuario_actualizado.get("nombre", usuario["nombre"])
            usuario["edad"] = usuario_actualizado.get("edad", usuario["edad"])

            return {
                "status": "200",
                "message": "Usuario actualizado exitosamente",
                "data": usuario
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# CRUD - ELIMINAR USUARIO (DELATE)

@app.delete("/v1/Usuarios/{id}", tags=["CRUD usuarios"])
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_Peticion)):
    await asyncio.sleep(2)

    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "status": "200",
                "message": "Usuario eliminado exitosamente",
                "data": usuario
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )






# Ejecutar con:
# uvicorn main:app --reload
# Documentación:
# http://localhost:8000/docs
# http://localhost:8000/redoc
