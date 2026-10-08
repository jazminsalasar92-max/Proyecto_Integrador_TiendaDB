from sqlalchemy import select
from db import create_tables, get_session, Product, Order, OrderItem

create_tables()

with get_session() as s:
    if s.scalars(select(Product)).first() is None:
        
        # 1. PASO 1: Cargar Productos (10 registros, con categoría "libros")
        p1 = Product(nombre="Remera Básica", precio=15000.0, categoria="Ropa", stock=20)
        p2 = Product(nombre="Pantalón Jean", precio=45000.0, categoria="Ropa", stock=15)
        p3 = Product(nombre="Buzo Hoodie", precio=52000.0, categoria="Ropa", stock=10)
        p4 = Product(nombre="Campera de Cuero", precio=95000.0, categoria="Ropa", stock=5)
        p5 = Product(nombre="El Principito", precio=12000.0, categoria="libros", stock=30)
        p6 = Product(nombre="Cien Años de Soledad", precio=18000.0, categoria="libros", stock=25)
        p7 = Product(nombre="Aprende Python en 7 días", precio=25000.0, categoria="libros", stock=12)
        p8 = Product(nombre="Mochila Urbana", precio=35000.0, categoria="Accesorios", stock=8)
        p9 = Product(nombre="Gorra Ajustable", precio=14000.0, categoria="Accesorios", stock=18)
        p10 = Product(nombre="Cinturón de Cuero", precio=16000.0, categoria="Accesorios", stock=14)

        s.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10])
        s.commit()  # Genera p.id

        # 2. PASO 2: Cargar Pedidos (Fechas repetidas, incluida "2026-09-10")
        o1 = Order(fecha="2026-09-10", total=75000.0)
        o2 = Order(fecha="2026-09-10", total=24000.0)
        o3 = Order(fecha="2026-09-10", total=52000.0)
        o4 = Order(fecha="2026-09-15", total=50000.0)
        o5 = Order(fecha="2026-09-15", total=45000.0)
        o6 = Order(fecha="2026-09-20", total=36000.0)
        o7 = Order(fecha="2026-09-20", total=35000.0)
        o8 = Order(fecha="2026-09-22", total=24000.0)
        o9 = Order(fecha="2026-09-25", total=95000.0)
        o10 = Order(fecha="2026-09-25", total=33000.0)

        s.add_all([o1, o2, o3, o4, o5, o6, o7, o8, o9, o10])
        s.commit()  # Genera o.id

        # 3. PASO 3: Cargar Items (Relacionando pedido_id y producto_id)
        s.add_all([
            OrderItem(pedido_id=o1.id, producto_id=p1.id, cantidad=2),
            OrderItem(pedido_id=o1.id, producto_id=p2.id, cantidad=1),
            
            OrderItem(pedido_id=o2.id, producto_id=p5.id, cantidad=2),
            
            OrderItem(pedido_id=o3.id, producto_id=p3.id, cantidad=1),
            
            OrderItem(pedido_id=o4.id, producto_id=p7.id, cantidad=2),
            
            OrderItem(pedido_id=o5.id, producto_id=p2.id, cantidad=1),
            
            OrderItem(pedido_id=o6.id, producto_id=p6.id, cantidad=2),
            
            OrderItem(pedido_id=o7.id, producto_id=p8.id, cantidad=1),
            
            OrderItem(pedido_id=o8.id, producto_id=p5.id, cantidad=2),
            
            OrderItem(pedido_id=o9.id, producto_id=p4.id, cantidad=1),
            
            OrderItem(pedido_id=o10.id, producto_id=p1.id, cantidad=1),
            OrderItem(pedido_id=o10.id, producto_id=p6.id, cantidad=1),
        ])
        s.commit()
        print("Datos cargados.")
    else:
        print("La base ya tenía datos.")