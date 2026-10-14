# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
Primero está el alcance completo del proyecto; al final, la devolución de cada semana.

**Grupo:** Kiara Cei, Jazmín Salasar
**Tema:** TiendaDB — Productos y pedidos

---

# Alcances de este proyecto

Esto es lo que hay que entregar. Lo que no está acá, no se pide.

## Reglas comunes a todos los grupos

### Stack
- Python + **FastAPI** + Uvicorn.
- Datos en **SQLite** usando **SQLAlchemy** (ORM): las tablas se definen como clases de Python y las consultas se hacen con métodos, sin escribir SQL a mano. **No se usa Pydantic**: las validaciones se hacen a mano en Python. Guía con ejemplo completo: [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md).
- Repositorio en GitHub con commits de **todos** los integrantes.
- API desplegada **en producción con Gunicorn** en Render, con URL pública y `/docs` funcionando (ver abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 08/10:** ahora va **todo en inglés**, también tablas, columnas y rutas. Reemplaza el criterio del 24/09.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params también en inglés**. Ejemplo: `class Student(Base)` con `__tablename__ = "students"`, columna `career_id` y ruta `GET /students`.
- El alcance de cada grupo lista las tablas y los endpoints en español **solo como referencia**: tradúzcanlos al inglés y usen **el mismo nombre en todos los archivos** (`db.py`, `seed.py`, `main.py`, `validation.py`).
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Despliegue a producción (Render + Gunicorn)

En tu compu desarrollás con `uvicorn main:app --reload`. En producción corre **Gunicorn** como administrador de procesos, con workers de Uvicorn adentro.

> Gunicorn **no funciona en Windows**. Localmente seguí usando `uvicorn`; Gunicorn corre en el servidor (Linux).

`requirements.txt` debe incluir:
```
fastapi
uvicorn
uvicorn-worker
gunicorn
sqlalchemy
```

En Render → **New → Web Service** → conectás el repo, y configurás:

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python seed.py && gunicorn main:app -k uvicorn_worker.UvicornWorker -w 2 -b 0.0.0.0:$PORT` |

La clave viaja en el código, así que no hay que configurar nada más en Render.

- El seed corre **una sola vez antes** de levantar Gunicorn. Si lo pusieras adentro de `main.py`, cada worker lo ejecutaría por su cuenta y podrían cargar los datos duplicados.
- El plan gratis se duerme tras ~15 min sin uso (la primera visita tarda ~1 min) y su disco se borra al reiniciar: por eso el seed.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- Unos **10 registros de ejemplo** por tabla. Siempre **datos ficticios**.
- Un script de carga inicial `seed.py` que crea las tablas (`create_all`) y carga los datos **si la base está vacía** (ver sección 9 de la guía). Se ejecuta antes de levantar el servidor. En Render el disco se borra al reiniciar: así la API siempre arranca con datos.
- El archivo `.db` **no se sube** a GitHub (agregalo al `.gitignore`); se genera solo.

### Seguridad: TODOS los endpoints van protegidos
- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- La clave se define como una constante al principio de `main.py`. Más adelante en la carrera van a ver cómo sacarla del código con variables de entorno; por ahora, así.
- Como la clave está a la vista en el repo, **los datos son todos ficticios** y no se usa esta API para nada real.
- Sin clave o con clave incorrecta → **401**.

Se protege toda la app de una vez:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

CLAVE = "clave-de-prueba-2026"   # clave del grupo
header = APIKeyHeader(name="X-API-Key")

def verificar(clave: str = Depends(header)):
    if clave != CLAVE:
        raise HTTPException(status_code=401, detail="API key invalida")

app = FastAPI(dependencies=[Depends(verificar)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.

---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param, `select(...).where(...)` |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea (`relationship` o filtro por FK) |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o con `func` de SQLAlchemy) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo como `dict`, **validar a mano** (400 si está mal) e insertar con la sesión |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Deploy:** URL pública en Render con `/docs` operativo.
- **README:** qué hace la API, lista de endpoints, cómo usar la API key, cómo correrla localmente, y declaración de uso de IA si la usaron.

## Nivel B — opcional

Existe un Nivel B que suma hasta 1 punto sobre la nota final. **No se preocupen por eso todavía:** lo vemos en clase más adelante, cuando el Nivel A esté andando.

---

## Alcance de este grupo

### Grupo 3 · TiendaDB — Productos y pedidos
**Integrantes:** Kiara Cei, Jazmín Salasar

**Tablas**
- `productos`: id, nombre, categoria, precio, stock
- `pedidos`: id, fecha, total
- `items_pedido`: id, pedido_id (FK), producto_id (FK), cantidad

**Endpoints Nivel A**
1. `GET /productos?categoria=libros`
2. `GET /productos/{id}`
3. `GET /pedidos/{id}/items`
4. `GET /pedidos?fecha=2026-09-10`
5. `GET /ventas/resumen` → total facturado y productos más vendidos
6. `POST /productos`


---

## Fuera de alcance (para todos)

No se pide y **no suma**:
- Frontend o páginas web.
- Login de usuarios, registro, JWT.
- Bases de datos externas (PostgreSQL, MySQL, etc.).
- Docker.
- Integración con IA o con el chatbot (eso corresponde a Análisis de Sistemas).
- Pagos, facturación, envío de mails, hardware real.

## Entregables

1. Repositorio GitHub: `main.py`, script de seed, `requirements.txt`, `README.md`, commits de todos.
2. URL pública en Render con `/docs` funcionando.
3. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
4. Defensa oral: demo en vivo desde `/docs` y preguntas sobre el código.

---

# Devolución semanal

## 23/09

**📌 Novedad:** la base se maneja con **SQLAlchemy** (ORM) y **sin Pydantic**; las validaciones del `POST` van a mano. Hay una guía con ejemplo completo en [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md) y el código en `guias/pokedex/`. Agreguen `sqlalchemy` a `requirements.txt`.

**Lo que hay:** nada. ⚠️ El repositorio está **vacío, sin un solo commit**.

**Próximos pasos (urgente)**
1. Subir hoy mismo `main.py` con el "hola mundo" de FastAPI y `requirements.txt`. Aunque sea mínimo, el repo tiene que mostrar avance.
2. `seed.py` con las 3 tablas: `productos`, `pedidos`, `items_pedido`.
3. Las dos tienen que commitear: los commits muestran el aporte de cada una.

## 24/09

**📌 Criterio de nombres.** Variables, funciones y clases en **inglés**; tablas, columnas y rutas como en el alcance; comentarios en inglés para la entrega final. Está detallado arriba en *Reglas comunes* y la guía ya lo aplica.

**Lo que hay:** por fin el repo tiene código. `main.py` con el "hola mundo" de FastAPI, `requirements.txt`, y `seed.py` que crea `productos`, `pedidos` e `items_pedido` con las columnas del alcance. Commits de las dos. 👍

**A corregir en `seed.py`**
- **Pasen la base a SQLAlchemy** (ver [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)): las tablas como clases, `create_all` y `add_all`. El `sqlite3` con SQL a mano ya no va.
- Faltan las claves foráneas: `items_pedido.pedido_id` y `items_pedido.producto_id` tienen que ser `ForeignKey`.
- Si lo corren dos veces rompe (`CREATE TABLE` sin `IF NOT EXISTS`) y no controla si ya hay datos. Tiene que cargar **solo si la base está vacía** (sección 9 de la guía). En Render el seed corre en cada arranque.
- Faltan datos: hay 3 productos, 1 pedido y 2 items. Se piden unos **10 por tabla**, si no los endpoints de filtro y resumen no tienen con qué probarse.

**A corregir en el repo**
- `tienda.db` está subido. Agréguenlo al `.gitignore` y sáquenlo con `git rm --cached tienda.db`. Se genera solo con el seed.
- `requirements.txt`: agreguen `uvicorn-worker`, `gunicorn` y `sqlalchemy`.

**Próximos pasos**
1. `seed.py` con SQLAlchemy, FK y ~10 registros por tabla.
2. `GET /productos?categoria=` y `GET /productos/{id}` con 404.
3. La clave con `FastAPI(dependencies=[Depends(verificar)])` (el código está arriba en este archivo).

## 08/10

**📌 Cambio de criterio: todo en inglés.** Ahora también las **tablas, columnas, rutas y query params** van en inglés, igual que el README, los docstrings y los mensajes de la API. Reemplaza lo dicho el 24/09; está detallado arriba en *Nombres en el código*. El alcance sigue listando los nombres en español solo como referencia.

**📌 Guía nueva (opcional):** [guias/variables_de_entorno.md](guias/variables_de_entorno.md), para sacar la clave del código con un `.env`.

**Lo que hay:** `db.py` con las tres tablas como clases de SQLAlchemy, con las claves foráneas y la `relationship` de `OrderItem` a `Product`. 👍 Lo probé y crea las tres tablas bien. `tienda.db` ya no está en el repo, el `.gitignore` está correcto y `requirements.txt` también.

**⚠️ Están atrasadas.** `main.py` sigue siendo el "Hola, Mundo" del 24/09: **0 de 6 endpoints** y sin API key. El último commit es del 03/10. Otros grupos ya tienen los seis endpoints andando.

**⚠️ Desde el 24/09 solo hay commits de Jazmín.** Kiara: tus commits tienen que aparecer. Es un requisito del proyecto y es lo que muestra el aporte de cada una.

**A corregir en `seed.py`**
- Sigue siendo el del 24/09, con `sqlite3` y SQL a mano, y ya no es compatible con `db.py`. Si las tablas ya existen se cae con `table productos already exists` (lo probé).
- Hay que reescribirlo usando `db.py`: importa las clases, llama a `create_tables()`, y carga los datos con `s.add_all([...])` **solo si la tabla está vacía**. Es la sección 9 de la [guía](guias/sqlalchemy_orm.md).
- Siguen siendo 3 productos, 1 pedido y 2 items. Se piden unos **10 por tabla**.

**Nombres en inglés** (criterio nuevo)
Las clases ya están bien (`Product`, `Order`, `OrderItem`). Faltan tablas, columnas y rutas:

| Hoy / alcance | Tiene que ser |
|---|---|
| tablas `productos`, `pedidos`, `items_pedido` | `products`, `orders`, `order_items` |
| `nombre`, `categoria`, `precio`, `stock` | `name`, `category`, `price`, `stock` |
| `fecha`, `total` | `date`, `total` |
| `pedido_id`, `producto_id`, `cantidad` | `order_id`, `product_id`, `quantity` |
| `GET /productos?categoria=` · `GET /productos/{id}` · `POST /productos` | `GET /products?category=` · `GET /products/{id}` · `POST /products` |
| `GET /pedidos/{id}/items` · `GET /pedidos?fecha=` | `GET /orders/{id}/items` · `GET /orders?date=` |
| `GET /ventas/resumen` | `GET /sales/summary` |

Háganlo ahora, que todavía no hay endpoints escritos: después es el doble de trabajo.

**Próximos pasos**
1. Renombrar tablas y columnas en `db.py`.
2. Reescribir `seed.py` con SQLAlchemy y ~10 registros por tabla. Probar que corre dos veces sin romper ni duplicar.
3. Agregar la API key en `main.py` (el código está arriba en *Seguridad*) y probar el 401.
4. `GET /products?category=` y `GET /products/{id}` con 404.
5. Repártanse el resto: una hace los dos de pedidos (3 y 4), la otra el resumen y el `POST` (5 y 6).
