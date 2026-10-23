from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError

import crud
from security import verify_api_key

app = FastAPI(title="TiendaDB API", dependencies=
[Depends(verify_api_key)])

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
    try:
            product = crud.get_product(product_id)
    except OperationalError:
            raise HTTPException(status_code=500, detail="Database error")
    if ptoduct is None:
            raise HTTPException(status_code=404, detail="Product not found")
    return product
    

@app.get("/orders/{order_id}/items")
def get_order_items(order_id: int):
    try:
        items = crud.get_order_items(order_id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")
    if items is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return items

@app.get("/orders")
def list_orders(date: str | None = None):
    try:
        return crud.list_orders(date)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/sales/summary")
def get_sales_summary():
    try:
        return crud.get_sales_summary()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/products", status_code=201)
def create_product(data: dict):
    try:
        return crud.create_product(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="product_id does not exist")