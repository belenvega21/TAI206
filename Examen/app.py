from pprint import pp
from fastapi import FastAPI, status, Depends, HTTPException
from typing import Optional 
import asyncio
from pydantic import BaseModel

#CREACIÓN DEL API
app = FastAPI (
title="SISTEMA DE CITAS MEDICAS",
title="CITAS MEDICAS",
description="Una API simple para gestionar citas medicas",
version="1.0"
)
 
 
 
#CREACIÓN DEL CRUD

#Registro de citas
@pp.pots 



#Listar citas 
@app.post ("/citas, ")



#Consultar cita por ID
@app.get("/citas")
def listar_cita():
    return cita

@app.get("/cita/{nombre}")
def buscar_libro(nombre: str):
    for libro in cita:
        if libro.nombre.lower() == nombre.lower():
            return libro
    raise HTTPException(status_code=400, detail="Libro no encontrado")


#Eliminar citas 
@app.delete("/prestamos/{nombre}")
def eliminar_prestamo(nombre: str):
    for prestamo in prestamos:
        if prestamo.libro == nombre:
            prestamos.remove(prestamo)
            return {"mensaje": "Préstamo eliminado"}
    raise HTTPException(status_code=409, detail="Registro de préstamo no existe")





# Ejecutar con:
# uvicorn main:app --reload
# Documentación:


