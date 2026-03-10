from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import date
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI(title="Sistema de Gestión de Citas Médicas")

security = HTTPBasic()

citas = []

class Cita(BaseModel):
    nombre: str = Field(..., min_length=5, description="Nombre del paciente (mínimo 5 caracteres)")
    fecha: date = Field(..., description="Fecha de la cita (no puede ser menor a la fecha actual)")
    motivo: str = Field(..., max_length=100, description="Motivo de la cita (máximo 100 caracteres)")
    confirmacion: bool = Field(default=False, description="Estado de confirmación de la cita")

def verificar_credenciales(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "root")
    correct_password = secrets.compare_digest(credentials.password, "1234")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return credentials

@app.post("/citas", status_code=201)
def crear_cita(cita: Cita):
    if cita.fecha < date.today():
        raise HTTPException(status_code=400, detail="La fecha no puede ser menor a la fecha actual")
    
    citas_mismo_dia = [c for c in citas if c.nombre == cita.nombre and c.fecha == cita.fecha]
    if len(citas_mismo_dia) >= 3:
        raise HTTPException(status_code=400, detail="No se permiten más de 3 citas en el mismo día para el mismo paciente")
    
    citas.append(cita)
    return {"mensaje": "Cita creada exitosamente"}

@app.get("/citas", dependencies=[Depends(verificar_credenciales)])
def listar_citas():
    return citas

@app.put("/citas/confirmar/{nombre}/{fecha}")
def confirmar_cita(nombre: str, fecha: date):
    for cita in citas:
        if cita.nombre == nombre and cita.fecha == fecha:
            cita.confirmacion = True
            return {"mensaje": "Cita confirmada exitosamente"}
    raise HTTPException(status_code=404, detail="Cita no encontrada")

@app.delete("/citas/{nombre}/{fecha}", dependencies=[Depends(verificar_credenciales)])
def eliminar_cita(nombre: str, fecha: date):
    for cita in citas:
        if cita.nombre == nombre and cita.fecha == fecha:
            citas.remove(cita)
            return {"mensaje": "Cita eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Cita no encontrada")




## Ejecutar con:
# uvicorn main:app --reload
# Documentación