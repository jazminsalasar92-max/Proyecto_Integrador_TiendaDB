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

@app.get("/orders/{id}/items")
def read_order_items(id: int, db: Session = Depends(database.get_db)):
    items = crud.get_order_items(db, order_id=id)
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"No se encontraron ítems para la orden con ID {id}"
        )
    return items

@app.get("/orders")
def read_orders_by_date(date: str, db: Session = Depends(database.get_db)):
    orders = crud.get_orders_by_date(db, order_date=date)
    return orders
def get_sales_summary(db: Session):
    total_orders = db.query(models.Order).count()
    total_revenue = db.query(func.sum(models.Order.total)).scalar() or 0.0
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }

SECRET_API_KEY = "MESSI"

def verify_api_key(api_key: str = Header(...)):
    if api_key != SECRET_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key"
        )
    return api_key

@app.get("/sales/summary")
def get_sales_summary(db: Session = Depends(database.get_db)):
    return crud.get_sales_summary(db)

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: dict, 
    db: Session = Depends(database.get_db), 
    api_key: str = Depends(verify_api_key)
):
    return crud.create_product_dict(db, product_data)