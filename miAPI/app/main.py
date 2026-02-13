#importaciones
from fastapi import FastAPI,status,HTTPException
from typing import Optional
import asyncio

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Calificaciones TAI",
    description="Una API simple para gestionar calificaciones en TAI",
    version="1.0."
)

usuarios=[
    {"id":1,"nombre":"Belén Vega","edad":20},
    {"id":2,"nombre":"Gabriel Villafuerte","edad":24},  
    {"id":3,"nombre":"Lu Malagon","edad":21}
          ]



#INCIO DE endpoints
@app.get("/",tags=["Inicio"])
async def HolaMundo():
    return {"mensaje": "Hola Mundo FastAPI a TAI"}

@app.get("/v1/bienvenidos",tags=["Inicio"])
async def bienvenidos():
    return {"mensaje": "Bienvenido a TAI"}

@app.get("/v1/calificaciones",tags=["Asincronia"])
async def calificaciones():
    await asyncio.sleep(2)  
    return {"mensaje": "Tu calificación en TAI es 10"}

@app.get("/v1/praetroO",tags=["Parametro obligatorio"])
async def consultaUsuarios(id: int):
    await asyncio.sleep(2)  
    return {"Usuario consultado": id}

@app.get("/v1/ParametroOP",tags=["Parametro opcional"])
async def consultaOp(id: Optional [int] = None):
    await asyncio.sleep(3)  
    if id is not None:
     for usuario in usuarios:
        if usuario["id"] == id:
            return {"Usuario consultado": id,
                    "Datos":usuario
                    }
        return {"mensaje":"Usuaroio no encontrado o no proporcionado"}
    else:
        return {"Aviso": "No se proporcionó ningún ID de usuario"}
    
 #CRUD usuarios   
@app.get("/v1/Usuarios",tags=["CRUD usuarios"])
async def consultaUsuarios():
    return {"status": "200",
            "total": len(usuarios),
            "data": usuarios}

@app.post("/v1/Usuarios",tags=["CRUD usuarios"])
async def agregar_usuarios(usuario: dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code= 400,
                detail="El ID del usuario ya existe")
    usuarios.append(usuario)
    return {"status": "200",
            "message": "Usuario agregado exitosamente",
            "datos": usuario}
        


#PUT (actualizar) 
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
    
    
    
#DELATE (eliminar) 
@app.delete("/v1/Usuarios/{id}", tags=["CRUD usuarios"])
async def eliminar_usuario(id: int):
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



# Ejecutar la aplicación con: uvicorn main:app --reload
# Acceder a la ruta: http://
#localhost:8000/v1/calificaciones



