from dbm import _Database
from email.header import Header
from http.client import HTTPException
import pstats

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