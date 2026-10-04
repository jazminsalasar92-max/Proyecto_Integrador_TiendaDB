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
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    categoria: Mapped[str]
    precio: Mapped[float]
    stock: Mapped[int]
    
    
    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre, "categoria": self.categoria, "precio": self.precio, "stock": self.stock}


class Order(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[str] = mapped_column(String(50))
    total: Mapped[float]
    

    def to_dict(self) -> dict:
        return {"id": self.id, "fecha": self.fecha, "total": self.total}

class OrderItem(Base):
    __tablename__ = "items_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    cantidad: Mapped[int] 
    
   
    product: Mapped[Product] = relationship() #not a column
   
    
    def to_dict(self) -> dict:
        return {"id": self.id, "pedido_id": self.pedido_id, "producto_id": self.producto_id, "cantidad": self.cantidad}



def create_tables():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
