from fastapi import status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

# SEGURIDAD CON HTTP BASIC
security = HTTPBasic()

def verificar_peticion(credentials: HTTPBasicCredentials = Depends(security)):
    usuarioAuth = secrets.compare_digest(credentials.username, "admin")
    contraAuth = secrets.compare_digest(credentials.password, "belenvega")
    
    if not (usuarioAuth and contraAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
        
    return credentials.username