# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léanlo antes de seguir programando.
El alcance completo del grupo está en el documento de alcances.

**Grupo:** Kiara Cei, Jazmín Salasar
**Tema:** TiendaDB — Productos y pedidos

---

## 23/09

**Lo que hay:** nada. ⚠️ El repositorio está **vacío, sin un solo commit**.

**Próximos pasos (urgente)**
1. Subir hoy mismo `main.py` con el "hola mundo" de FastAPI y `requirements.txt`. Aunque sea mínimo, el repo tiene que mostrar avance.
2. `seed.py` con las 3 tablas: `productos`, `pedidos`, `items_pedido`.
3. Las dos tienen que commitear: los commits muestran el aporte de cada una.

**Endpoints a entregar (Nivel A)**
- [ ] `GET /productos?categoria=libros`
- [ ] `GET /productos/{id}` (404 si no existe)
- [ ] `GET /pedidos/{id}/items`
- [ ] `GET /pedidos?fecha=2026-09-10`
- [ ] `GET /ventas/resumen` (total facturado y más vendidos)
- [ ] `POST /productos`
- [ ] Todos protegidos con `X-API-Key` (clave como constante en `main.py`)
