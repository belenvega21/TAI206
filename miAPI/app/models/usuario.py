from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    edad: int