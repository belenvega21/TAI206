from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class citas(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    autor: str
    anio: int = Field(gt=1450, le=datetime.now().year)
    paginas: int = Field(gt=1)
    estado: str = Field(default="disponible", pattern="^(disponible|registrado)$")

class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

class Registro(BaseModel):
    citas: str
    usuario: Usuario
    
    
    
    






