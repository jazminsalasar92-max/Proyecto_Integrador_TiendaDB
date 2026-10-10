from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "MESSI" 
header = APIKeyHeader (name="X-API-KEY")


def verify_api_Key(key: str = Depends(header)):
    if key != API_KEY: 
        raise HTTPException(status_code=401, detail="Invalid API Key")
    