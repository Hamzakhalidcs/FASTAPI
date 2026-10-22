import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

class Product(BaseModel):
    product : str
    price : int 

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
    
@app.post('/products_post')
def post_product(product:Product):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                
                """
                INSERT INTO products (product, price)
                VALUES (%s, %s)
                RETURNING product, price;
                """,
                   (product.product, product.price )
                )
            new_product = cur.fetchone()
    
    return {
        "message" : "product Insert Successfully",
        "Product" : {
            "product": new_product[0],
            "price" : new_product[1]
        }
    }