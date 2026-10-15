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
- Datos en **SQLite**. Pueden usar **SQLAlchemy** (ORM, con la guía [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)) o **`sqlite3` con SQL directo**: las dos formas valen. **Pydantic es opcional**: el cuerpo del `POST` se puede validar con un modelo de Pydantic (`class StudentIn(BaseModel)`) o a mano en `validation.py`. Las dos formas valen.
- Repositorio en GitHub con commits de **todos** los integrantes.
- **Demo local:** la API se corre en la notebook de cada grupo con `uvicorn`. No hace falta desplegarla en la web (ver *Demo local*, abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 15/10:** los nombres de tablas, columnas y rutas en inglés pasan a ser una **recomendación**. Si quedan en español, no es un error.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params:** se recomienda que también vayan en inglés (`__tablename__ = "students"`, columna `career_id`, ruta `GET /students`), pero pueden quedar en español, como figuran en el alcance.
- Lo que sí es obligatorio: usar **el mismo nombre en todos los archivos** (`models.py`, `seed.py`, `crud.py`, `main.py`, `validation.py`). Si la tabla se llama `estudiantes` en el seed, se llama `estudiantes` en todos lados.
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Demo local (sin despliegue)

> **Actualizado el 15/10:** no se despliega a producción. La defensa es **local**, en la notebook del grupo.

`requirements.txt` debe incluir:
```
fastapi
uvicorn
python-dotenv
```
y `sqlalchemy` si lo usan.

Para levantar el proyecto desde cero (lo mismo tiene que estar en el README):
```
python -m venv venv
venv\Scripts\activate          (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```
Y abrir http://127.0.0.1:8000/docs.

- El seed se corre **una vez, antes** de levantar el servidor. No va adentro de `main.py`.
- Antes de la defensa, prueben todo esto en la notebook con la que van a presentar.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- **Algunos datos de ejemplo** en cada tabla, los suficientes para ver funcionar los endpoints. No hay mínimo ni máximo. Siempre **datos ficticios**.
- Recomendación: que los datos permitan ver los filtros en acción, por ejemplo productos de varias categorías, para que `?category=` devuelva algo distinto de la lista completa.
- Un script de carga inicial `seed.py` que crea las tablas (con `create_all` o con `CREATE TABLE IF NOT EXISTS`) y carga los datos **solo si la base está vacía**. Se ejecuta antes de levantar el servidor y, si se corre dos veces, no duplica nada.
- El archivo `.db` **puede estar en el repo**. Si lo suben, que esté actualizado (el que genera el seed actual).

### Seguridad: TODOS los endpoints van protegidos

> **Actualizado el 15/10:** se **recomienda** guardar la clave en una variable de entorno en lugar de escribirla en el código. No es obligatorio; en la defensa se puede preguntar por qué conviene hacerlo.

- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- Sin clave o con clave incorrecta → **401**. Con la clave correcta → **200** y los datos.
- **Recomendado:** guardar la clave en un archivo **`.env`** que **no se sube** (va en el `.gitignore`) y leerla con `python-dotenv`. Al repo se sube un **`.env.example`** con el nombre de la variable y sin el valor. Paso a paso en [guias/variables_de_entorno.md](guias/variables_de_entorno.md). Si la dejan como constante en `security.py`, también vale.
- Los datos son todos **ficticios**: esta API no se usa para nada real.

`security.py` con la clave en el `.env` (la forma recomendada):

```python
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()
API_KEY = os.getenv("API_KEY")
header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Depends(header)):
    if API_KEY is None or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

Y en `main.py` se protege toda la app de una vez:

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.
---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param y filtro en la consulta |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o en la consulta) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo (con un modelo de Pydantic o como `dict` validado a mano), rechazar los datos inválidos con **400** o **422**, e insertar en la base |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Seguridad (recomendado):** API key en variable de entorno (`.env`) en lugar de escrita en el código.
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
2. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
3. Defensa oral el **miércoles 28/10**: demo en vivo desde `/docs`, en local, y preguntas sobre el código. El repositorio tiene que estar al día el **miércoles 21/10**.

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

## 15/10

**📌 Cambios en las reglas** (están arriba, en *Reglas comunes*):
- **SQLAlchemy es opcional:** también vale `sqlite3` con SQL directo.
- **No hay que desplegar.** La defensa es **local**, en su notebook, el **miércoles 28/10**. El repo tiene que estar al día el **miércoles 21/10**.
- **Recomendado:** la API key en una variable de entorno (`.env`) en lugar de escrita en el código. No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Lo que hay:** mucho trabajo y de las dos. 👍 Jazmín pasó tablas, columnas y rutas a inglés, renombró `db.py` a `models.py` y armó `security.py`. Kiara reescribió el seed y avanzó con los endpoints. El seed funciona: carga 10 productos, 10 pedidos y 18 items, calcula los totales y no duplica. `requirements.txt` y `.gitignore` están bien.

**⚠️ La API no arranca.** `crud.py` empieza con cuatro imports que no tienen nada que ver con el proyecto (`from dbm import _Database`, `from email.header import Header`, `from http.client import HTTPException`, `import pstats`). Seguramente los agregó el autocompletado de VS Code. El primero no existe, y `uvicorn main:app` falla antes de empezar.

**Lo probé arreglando esos imports.** Aparecen estos problemas:
- **La clave no protege nada:** en `main.py:7` dice `depencies=` en vez de `dependencies=`. FastAPI lo ignora sin avisar, y todos los `GET` responden sin clave.
- El `POST` tiene **otra** verificación de clave, con otro header (`api-key` en lugar de `X-API-Key`). Tiene que haber una sola, la de `security.py`.
- `GET /orders/{id}/items` y `GET /orders` usan `Session`, `database.get_db` y `status`, que no existen en el proyecto. `crud.py` usa `func` sin importarlo.
- `GET /orders?date=` obliga a mandar la fecha (sin ella da 422). El filtro tiene que ser opcional: `date: str = None`.
- `GET /sales/summary` da el total facturado (566.000, correcto), pero **faltan los productos más vendidos**.
- **`POST /products` no valida nada.** Si falta un campo o el precio es `"abc"` da 500; con precio negativo o `true` lo guarda. Como no usan Pydantic, la validación va a mano: una función `validate_product(data)` en `validation.py` que revise cada campo y lance `ValueError`, y `main.py` lo convierte en 400 (ver [guias/estructura_del_proyecto.md](guias/estructura_del_proyecto.md), sección 4).
- `main.py:43-60` tiene una función repetida y código que quedó de un merge.

**Lo que falta para la entrega del 21/10**
1. Que arranque: borrar los imports basura de `crud.py`, sacar el código repetido de `main.py` y usar en todas las funciones la misma forma de abrir la sesión (`get_session()`, como en `list_products`).
2. `dependencies=` bien escrito y una sola verificación de clave. Probar el 401.
3. `validation.py` con la validación del `POST` (400 si falta un campo, si el tipo está mal, si es negativo o booleano).
4. Los más vendidos en el resumen y el filtro de fecha opcional.
5. `try/except` en todos los endpoints (hoy solo lo tiene `GET /products`).
6. **README:** no existe. Hay una guía con plantilla en `guias/`.

**Recomendación:** pasar la clave (`"MESSI"`, hoy escrita en `security.py` y en `main.py`) a un `.env` (ver *Seguridad*, arriba, y [guias/variables_de_entorno.md](guias/variables_de_entorno.md)). No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Más chico:** el título de la app dice "Pokedex Api"; quedan mensajes en español ("No encontrado", "¡Hola, Mundo!"); la tabla se llama `order_Items` (con mayúscula); la carpeta `.vscode/` no va en el repo. Los commits de Kiara se llaman todos "upload changes" o "actualice el proyecto": tienen que decir qué cambió.

Antes de cada commit, levanten la API y prueben en `/docs`.
