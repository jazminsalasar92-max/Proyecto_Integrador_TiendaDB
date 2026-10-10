from sqlalchemy import select

from db import create_tables, get_session, Product, Order, OrderItem

create_tables()

with get_session() as s:
    if s.scalars(select(Product)).first() is None:  

        
        p1 = Product(name="Remera basica blanca", category="remeras", price=12000.0, stock=30)
        p2 = Product(name="Remera estampada", category="remeras", price=15000.0, stock=25)
        p3 = Product(name="Musculosa negra", category="remeras", price=9000.0, stock=20)
        p4 = Product(name="Jean recto azul", category="pantalones", price=35000.0, stock=15)
        p5 = Product(name="Jogger gris", category="pantalones", price=28000.0, stock=18)
        p6 = Product(name="Short de jean", category="pantalones", price=20000.0, stock=12)
        p7 = Product(name="Buzo con capucha", category="abrigos", price=32000.0, stock=10)
        p8 = Product(name="Campera de jean", category="abrigos", price=55000.0, stock=8)
        p9 = Product(name="Zapatillas urbanas", category="calzado", price=60000.0, stock=10)
        p10 = Product(name="Ojotas", category="calzado", price=8000.0, stock=40)
        products = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
        s.add_all(products)
        s.commit() 

        
        o1 = Order(date="2026-09-08", total=0)
        o2 = Order(date="2026-09-09", total=0)
        o3 = Order(date="2026-09-10", total=0)
        o4 = Order(date="2026-09-10", total=0)
        o5 = Order(date="2026-09-10", total=0)
        o6 = Order(date="2026-09-11", total=0)
        o7 = Order(date="2026-09-12", total=0)
        o8 = Order(date="2026-09-12", total=0)
        o9 = Order(date="2026-09-13", total=0)
        o10 = Order(date="2026-09-14", total=0)
        orders = [o1, o2, o3, o4, o5, o6, o7, o8, o9, o10]
        s.add_all(orders)
        s.commit()  # now every order has its id

       
        s.add_all([
            OrderItem(order_id=o1.id, product_id=p1.id, quantity=2),
            OrderItem(order_id=o1.id, product_id=p4.id, quantity=1),
            OrderItem(order_id=o2.id, product_id=p9.id, quantity=1),
            OrderItem(order_id=o3.id, product_id=p1.id, quantity=3),
            OrderItem(order_id=o3.id, product_id=p7.id, quantity=1),
            OrderItem(order_id=o4.id, product_id=p2.id, quantity=2),
            OrderItem(order_id=o4.id, product_id=p10.id, quantity=1),
            OrderItem(order_id=o5.id, product_id=p5.id, quantity=1),
            OrderItem(order_id=o5.id, product_id=p1.id, quantity=1),
            OrderItem(order_id=o6.id, product_id=p8.id, quantity=1),
            OrderItem(order_id=o7.id, product_id=p4.id, quantity=2),
            OrderItem(order_id=o7.id, product_id=p3.id, quantity=1),
            OrderItem(order_id=o8.id, product_id=p9.id, quantity=1),
            OrderItem(order_id=o8.id, product_id=p10.id, quantity=2),
            OrderItem(order_id=o9.id, product_id=p6.id, quantity=1),
            OrderItem(order_id=o9.id, product_id=p2.id, quantity=1),
            OrderItem(order_id=o10.id, product_id=p7.id, quantity=1),
            OrderItem(order_id=o10.id, product_id=p1.id, quantity=2),
        ])
        s.commit()

        for order in orders:
            items = s.scalars(select(OrderItem).where(OrderItem.order_id == order.id))
            order.total = sum(i.product.price * i.quantity for i in items)
        s.commit()

        print("Data loaded.")
    else:
        print("The database already had data.")