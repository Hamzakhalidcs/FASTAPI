import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def get_connection():
    return psycopg.connect(
        dbname= "sql_practice",
        user="macbook_user",
        host="/tmp"
    )

@app.get('/products')
def get_products():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # cur.execute("SELECT current_database(), current_user")
            # print(cur.fetchone())
            cur.execute("SELECT * FROM products")
            products = cur.fetchall()

        return {
            "Products": products
        }