from sqlalchemy import select, func

from models import get_session, Product, Order, OrderItem
from validation import validate_product


def list_products (category:str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Product).order_by(Product.id)
        if category is not None:
            query = query.where(Product.category == category)
        return [p.to_dict() for p in s.scalars(query)]


def get_product(product_id: int) -> dict | None:
    with get_session() as s:
        product =s.get(Product, product_id)
        return product.to_dict() if product else None
    
    
def list_orders(date: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Order).order_by(Order.id)
        if date is not None:
            query = query.where(Order.date == date)
        return [o.to_dict() for o in s.scalars(query)]
    

def get_order_items(order_id: int) -> list[dict] | None:
    with get_session() as s:
        if s.get(Order, order_id) is None:
            return None
        items = s.scalars(select(OrderItem).where(OrderItem.order_id == order_id))
        return [{**i.to_dict(), "product_name": i.product.name} for i in items]
    
    
def get_sales_summary() -> dict:
    with get_session() as s:
        total_orders = s.scalar(select(func.count(Order.id)))
        total_revenue = s.scalar(select(func.sum(Order.total))) or 0.0
        units = func.sum(OrderItem.quantity).label("units_sold")
        rows = s.execute(
            select(Product.id, Product.name, units)
            .join(OrderItem, OrderItem.product_id == Product.id)
            .group_by(Product.id)
            .order_by(units.desc())
            .limit(5)
        ).all()
        best_sellers = [
            {"product_id": r.id, "name": r.name, "units_sold": r.units_sold}
            for r in rows
        ]
        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "best_sellers": best_sellers,
        }
        

def create_product(data: dict) -> dict:
    clean = validate_product(data)
    with get_session() as s:
        product = Product(**clean)
        s.add(product)
        s.commit()
        return product.to_dict()
    
           