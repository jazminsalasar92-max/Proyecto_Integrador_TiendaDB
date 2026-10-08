from sqlalchemy import select

from db import create_tables, get_session, Product, Order, OrderItem

create_tables()

with get_session() as s:
    if s.scalars(select(Product)).first() is None:  

        
        p1 = Product(nombre="Remera basica blanca", categoria="remeras", precio=12000.0, stock=30)
        p2 = Product(nombre="Remera estampada", categoria="remeras", precio=15000.0, stock=25)
        p3 = Product(nombre="Musculosa negra", categoria="remeras", precio=9000.0, stock=20)
        p4 = Product(nombre="Jean recto azul", categoria="pantalones", precio=35000.0, stock=15)
        p5 = Product(nombre="Jogger gris", categoria="pantalones", precio=28000.0, stock=18)
        p6 = Product(nombre="Short de jean", categoria="pantalones", precio=20000.0, stock=12)
        p7 = Product(nombre="Buzo con capucha", categoria="abrigos", precio=32000.0, stock=10)
        p8 = Product(nombre="Campera de jean", categoria="abrigos", precio=55000.0, stock=8)
        p9 = Product(nombre="Zapatillas urbanas", categoria="calzado", precio=60000.0, stock=10)
        p10 = Product(nombre="Ojotas", categoria="calzado", precio=8000.0, stock=40)
        products = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
        s.add_all(products)
        s.commit() 

        
        o1 = Order(fecha="2026-09-08", total=0)
        o2 = Order(fecha="2026-09-09", total=0)
        o3 = Order(fecha="2026-09-10", total=0)
        o4 = Order(fecha="2026-09-10", total=0)
        o5 = Order(fecha="2026-09-10", total=0)
        o6 = Order(fecha="2026-09-11", total=0)
        o7 = Order(fecha="2026-09-12", total=0)
        o8 = Order(fecha="2026-09-12", total=0)
        o9 = Order(fecha="2026-09-13", total=0)
        o10 = Order(fecha="2026-09-14", total=0)
        orders = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10]
        s.add_all(orders)
        s.commit()  # now every order has its id

       
        s.add_all([
            OrderItem(pedido_id=o1.id, producto_id=p1.id, cantidad=2),
            OrderItem(pedido_id=o1.id, producto_id=p4.id, cantidad=1),
            OrderItem(pedido_id=o2.id, producto_id=p9.id, cantidad=1),
            OrderItem(pedido_id=o3.id, producto_id=p1.id, cantidad=3),
            OrderItem(pedido_id=o3.id, producto_id=p7.id, cantidad=1),
            OrderItem(pedido_id=o4.id, producto_id=p2.id, cantidad=2),
            OrderItem(pedido_id=o4.id, producto_id=p10.id, cantidad=1),
            OrderItem(pedido_id=o5.id, producto_id=p5.id, cantidad=1),
            OrderItem(pedido_id=o5.id, producto_id=p1.id, cantidad=1),
            OrderItem(pedido_id=o6.id, producto_id=p8.id, cantidad=1),
            OrderItem(pedido_id=o7.id, producto_id=p4.id, cantidad=2),
            OrderItem(pedido_id=o7.id, producto_id=p3.id, cantidad=1),
            OrderItem(pedido_id=o8.id, producto_id=p9.id, cantidad=1),
            OrderItem(pedido_id=o8.id, producto_id=p10.id, cantidad=2),
            OrderItem(pedido_id=o9.id, producto_id=p6.id, cantidad=1),
            OrderItem(pedido_id=o9.id, producto_id=p2.id, cantidad=1),
            OrderItem(pedido_id=o10.id, producto_id=p7.id, cantidad=1),
            OrderItem(pedido_id=o10.id, producto_id=p1.id, cantidad=2),
        ])
        s.commit()

        for order in orders:
            items = s.scalars(select(OrderItem).where(OrderItem.pedido_id == order.id))
            order.total = sum(i.product.precio * i.cantidad for i in items)
        s.commit()

        print("Data loaded.")
    else:
        print("The database already had data.")