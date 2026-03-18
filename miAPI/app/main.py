from fastapi import FastAPI
from app.routers import usuarios, misc

# CREAR LA APLICACIÓN
app = FastAPI(
    title="MI PRIMER API",
    description="Una API organizada con APIRouter",
    version="1.0"
)

# INCLUIR ROUTERS
app.include_router(misc.router)
app.include_router(usuarios.router)