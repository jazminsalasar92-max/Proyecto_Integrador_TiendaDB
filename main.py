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

def create_product_dict(db: Session, product_data: dict):
    db_product = models.Product(
        name=product_data.get("name"),
        category=product_data.get("category"),
        price=product_data.get("price"),
        stock=product_data.get("stock")
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product