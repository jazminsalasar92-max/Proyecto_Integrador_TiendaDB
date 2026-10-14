from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

CLAVE = "MESSI"   # clave del grupo
header = APIKeyHeader(name="X-API-Key")

def verificar(clave: str = Depends(header)):
    if clave != CLAVE:
        raise HTTPException(status_code=401, detail="API key invalida")

app = FastAPI(dependencies=[Depends(verificar)])

@app.get("/")                
def inicio():
    return {"mensaje": "¡Hola, Mundo!"}

