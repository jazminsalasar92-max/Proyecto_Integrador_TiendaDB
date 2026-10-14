from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

import crud
from security import verify_api_Key

app = FastAPI(title="Pokedex Api", depencies=
[Depends(verify_api_Key)])

@app.get("/")                
def inicio():
    return {"mensaje": "¡Hola, Mundo!"}

@app.get("/products")
def list_products(category: str | None = None):
    try:
        return crud.list_products(category)
    except OperationalError: 
        raise HTTPException(status_code=500, detail="Database error")
    
@app.get("/products/{product_id}")
def get_product(product_id:int):
    product = crud.get_product(product_id)
    if product is None:
           raise HTTPException(status_code=404,
           detail="No encontrado")
    return product