from sqlalchemy import select
from sqlalchemy.orm import Session

from models import get_session, Product
#cuando realize validation.py agrego from validation

def list_products (category:str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Product)
        if category is not None:
            query = query.where(Product.category == category)
        return [p.to_dict() for p in s.scalars(query)]


def get_product(product_id: int) -> dict | None:
    with get_session() as s:
        product =s.get(Product, product_id)
        return product.to_dict() if product else None
import models

def get_order_items(db: Session, order_id: int):
    """
    Busca en la tabla order_items todos los registros que coincidan con el order_id recibido.
    """
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

def get_orders_by_date(db: Session, order_date: str):
    """
    Busca en la tabla orders todas las órdenes que coincidan con la fecha.
    """
    return db.query(models.Order).filter(models.Order.date == order_date).all()
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
import crud, database

API_KEY_SECRETA = "MESSI"

def verificar_api_key(api_key: str = Header(...)):
    if api_key != API_KEY_SECRETA:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida o faltante"
        )
    return api_key

# Punto 5: GET /sales/summary
@app.get("/sales/summary")
def sales_summary(db: Session = Depends(database.get_db)):
    return crud.get_sales_summary(db)

# Punto 6: POST /products (Sin validación, recibe un diccionario genérico)
@app.post("/products", status_code=status.HTTP_201_CREATED)
def add_product(
    product_data: dict, 
    db: Session = Depends(database.get_db), 
    api_key: str = Depends(verificar_api_key)
):
    return crud.create_product_dict(db, product_data)


    
