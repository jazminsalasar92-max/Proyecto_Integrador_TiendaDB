import sqlite3

db = sqlite3.connect("tienda.db")
c = db.cursor()
c.execute("CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT, categoria TEXT, precio REAL, stock INTEGER)")
c.execute("CREATE TABLE pedidos (id INTEGER PRIMARY KEY, fecha TEXT, total REAL)")
c.execute("CREATE TABLE items_pedido (id INTEGER PRIMARY KEY, pedido_id INTEGER, producto_id INTEGER, cantidad INTEGER)")

c.executemany("INSERT INTO productos VALUES (NULL,?,?,?,?)", [
    ("Remera Oversize", "Remeras", 18500, 30),
    ("Pantalón Jean", "Pantalones", 42000, 15),
    ("Buzo Hoodie", "Buzos", 38000, 20)
])

c.execute("INSERT INTO pedidos VALUES (1, '2026-09-23', 60500)")
c.executemany("INSERT INTO items_pedido VALUES (NULL,?,?,?)", [
    (1, 1, 1), # 1 Remera ($18.500)
    (1, 2, 1)  # 1 Jean ($42.000)
])

db.commit()
db.close()
print("¡Base de datos creada y cargada!")