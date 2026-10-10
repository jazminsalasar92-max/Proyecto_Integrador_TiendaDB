from sqlalchemy import create_engine, event, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_FILE = "tienda.db"

# El "engine" es la conexión a la base. sqlite:/// + nombre del archivo.
engine = create_engine(f"sqlite:///{DB_FILE}")


@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    con.execute("PRAGMA foreign_keys = ON")


class Base(DeclarativeBase):
    pass

    
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    category: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    
    
    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "category": self.category, "price": self.price, "stock": self.stock}


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(50))
    total: Mapped[float]
    

    def to_dict(self) -> dict:
        return {"id": self.id, "date": self.date, "total": self.total}
    
    

class OrderItem(Base):
    __tablename__ = "order_Items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] 
    
   
    product: Mapped[Product] = relationship() #not a column
   
    
    def to_dict(self) -> dict:
        return {"id": self.id, "order_id": self.order_id, "product_id": self.product_id, "quantity": self.quantity}



def create_tables():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
