import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()  # Lee el archivo .env

API_KEY = os.getenv("API_KEY", "MESSI")
if API_KEY is None:
    raise RuntimeError("verify_api_key")

header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Depends(header)):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")