"""
Pagination is important in Production APIs because returning thousand of records in one response 
can increase response time, memory usage  and network overhead.

POSTRESQL provides two clauses for pagination.
LIMIT -- how many records to return. 
OFFSET -- how many records to skip.

simple query to undersetand this concept. 
SELECT id, product, price from products order by id limit 3 offset 0 ;
SELECT id, product, price from products order by id limit 3 offset 3 ;
so it will show next 3 
"""

from fastapi import FastAPI, Query
import psycopg
from classes import * 

app = FastAPI()

@app.get("/products", response_model = ProductsResponse)
def get_products(
    product : str =None,
    page : int = Query(1, ge=1),
    limit:int = Query(3,ge=1,le=100)
):
    offset = (page - 1) * limit
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select id, product, price
                from products 
                order by id
                limit %s offset %s
                """,
                (limit, offset)
            )

            products = cur.fetchall()

    return {
        "Products" : [
            {
                "id" : row[0],
                "product" : row[1],
                "price" : row[2]
            }
            for row in products
        ]
    }

"""
A few things to understand:
- Query(1, ge=1) means the page defaults to 1 and cannot be less than 1.
- Query(3, ge=1, le=100) means 3 records per page by default, with a maximum of 100.
- offset calculates how many records PostgreSQL should skip.
"""