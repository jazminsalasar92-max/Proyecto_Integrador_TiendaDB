from sqlalchemy import select

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
    
