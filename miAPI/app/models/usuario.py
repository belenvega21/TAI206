from pydantic import BaseModel, Field

# MODELO PYDANTIC
class UsuarioBase(BaseModel):
    id: int = Field(..., gt=0, example=4)
    nombre: str = Field(..., min_length=3, max_length=50, example="Vivi López")
    edad: int = Field(..., ge=0, le=120, example=22)