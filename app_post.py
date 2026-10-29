import psycopg
from fastapi import FastAPI, HTTPException
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

@app.put('/product_put/{product_id}')
def update_product(product_id:int, product:Product):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE products
                SET product = %s, price=%s
                WHERE id=%s
                RETURNING product, price;
                """,
                (product.product, product.price, product_id)
            )

            update_product = cur.fetchone()

            if update_product is None:
                raise HTTPException(status_code=404, detail="Product Not Found ")
            
        conn.commit()

    return {
        "message" : "Product Update Successfully",
        "Product" : {
            "Id" : product_id,
            "prodcut" : update_product[0],
            "price" : update_product[1]
        }
    }

@app.delete("/delete_products/{product_name}")
def delete_product(product_name:str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM products
                WHERE product = %s
                RETURNING product, price;
                """,
                (product_name,)

            )

            deleted_product = cur.fetchone()

        if deleted_product is None:
            # return {"message": "Product Not Found"}
            raise HTTPException(
                status_code=404,
                detail="Product Not Found"
            )
        
        return {
            "message" : "Product Deleted Successfully",
            "product": {
                "product" : deleted_product[0],
                "price" : deleted_product[1]
            }
        }