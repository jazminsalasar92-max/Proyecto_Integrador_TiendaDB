# TiendaDB API

REST API for an online clothing store: products, orders and a sales summary. Built with FastAPI and SQLite (SQLAlchemy) for the Informatica course (TDS05) at Universidad de Mendoza.

## Authors

- Jazmin Salasar
- Kiara Cei

## Requirements

- Python 3.11 or newer
- Git

## How to run it

1. Clone the repository and enter the folder:

   ```
   git clone https://github.com/Jazminsalasar92-max/Proyecto_Integrador_TiendaDB.git
   cd Proyecto_Integrador_TiendaDB
   ```


2. Create and activate a virtual enviroNment:

   ```
   python -m venv venv
   venv\Scripts\Activate
   ```


3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```


4. Copy `.env.example` as `.env` and set the API Key:

   ```
   API_KEY=your_Key
   DB_FILE=tienda.db
   ```


5. Create the database and load the sample data:

   ```
   python seed.py
   ```

6. Start the server:

 ```
 uvicorn main:app --reload
   ```

7. Open http://127.0.0.1:8000/docs



## How to use it

Every endpoint requires the API key in the X-API-Key header.
In /docs, click **Authorize** and paste the key you set in .env.

| Method | Path | Description |
|--------|------|-------------|
| GET | /products?category=remeras | List products, optionally by category |
| GET | /products/{id} | Get one product |
| POST | /products | Create a product |
| GET | /orders?date=2026-09-10 | List orders, optionally by date |
| GET | /orders/{id}/items | List the items of an order |
| GET | /sales/summary | Total orders, total revenue and best sellers |

Example:

```
curl -H "X-API-Key: your-key" http://127.0.0.1:8000/products/1
```
```json
{"id": 1, "name": "Remera basica blanca", "category": "remeras", "price": 12000.0, "stock": 30}
```

Errors: 401 without a valid key, 404 if the id does not exist,
400 if the data sent is invalid.

## Deploy

Not deployed: the project runs locally, as defined by the course.


## Use of AI

We used Claude (Anthropic) as an assistant to understand SQLAlchemy and Git,
review error messages, and help restructure `validation.py` following the course guide.


