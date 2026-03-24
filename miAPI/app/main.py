from fastapi import FastAPI
from app.routers import usuarios, misc
from app.data.db import base, engine
from app.data import usuario 

# CREAR LA APLICACIÓN
app = FastAPI(
    title="MI PRIMER API",
    description="Una API organizada con APIRouter",
    version="1.0"
)

# CREAR TABLAS (mejor en evento startup)
@app.on_event("startup")
def startup():
    base.metadata.create_all(bind=engine)

# INCLUIR ROUTERS
app.include_router(misc.router)
app.include_router(usuarios.router)