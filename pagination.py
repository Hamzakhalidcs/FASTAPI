"""
AI Engineering is the practice of taking existing AI model like chatgpt, claude or image 
generator and building real, working software application around them. 
Think like this 
AI Researchers / Data scientist build the egnine (Ai Model)
AI Engineers build the car around the engine(App, APi, databases, the user Interface)


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

from fastapi import FastAPI, Query,HTTPException
from classes import * 
from typing import Literal
import math


app = FastAPI()


@app.get("/products", response_model=ProductsResponse)
def get_products(
    product: str = None,
    order: Literal["asc", "desc"] = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=100)
):
    offset = (page - 1) * limit

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Query 1: Count matching products
            if product:
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM products
                    WHERE product ILIKE %s
                    """,
                    (f"%{product}%",)
                )
            else:
                cur.execute("SELECT COUNT(*) FROM products")

            total_records = cur.fetchone()[0]
            total_pages = math.ceil(total_records/limit)

            if total_pages>0 and page > total_pages:
                raise HTTPException(
                    status_code=404,
                    detail=f"Page {page} does not exist. Total available pages: {total_pages}"
                )

            # Query 2: Retrieve actual product details
            if product:
                cur.execute(
                    """
                    SELECT id, product, price
                    FROM products
                    WHERE product ILIKE %s
                    ORDER BY price {order}
                    LIMIT %s OFFSET %s
                    """.replace("{order}", order),
                    (f"%{product}%", limit, offset)
                )
            else:
                cur.execute(
                    f"""
                    SELECT id, product, price
                    FROM products
                    ORDER BY price {order}
                    LIMIT %s OFFSET %s
                    """,
                    (limit, offset)
                )

            products = cur.fetchall()

    return {
        "Products": [
            {
                "id": row[0],
                "product": row[1],
                "price": row[2]
            }
            for row in products
        ],
        "total_records": total_records,
        "total_pages": total_pages,
        "current_page": page,
        "limit": limit
    }


@app.get('/products_cursor', response_model=ProductsCursorResponse)
def get_product_cursor(
    last_id : int | None = Query(None, description="The ID of the last record from previous page"),
    limit : int = Query(3, ge=1, le=100, description="Number of records to return")
):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # if the last id is provided
            if last_id is not None:
                cur.execute(
                    """
                    SELECT id, product, price
                    FROM products
                    WHERE  id> %s
                    ORDER BY id ASC
                    LIMIT %s
                    """,
                    (last_id, limit)
                )

            # if the last_id is not provided
            else:
                cur.execute(
                    """
                    SELECT id, product, price
                    FROM products
                    ORDER BY id ASC
                    LIMIT %s
                    """,
                    (limit,)
                )
            
            products = cur.fetchall()
        
        # Get the ID of the last returned record
        next_cursor = products[-1][0] if products else None

        
        # Return the formatted response
        return{
            "Products":[
                {
                    "id" : row[0],
                    "product": row[1],
                    "price" : row[2]
                }
                for row in products
            ],
            "next_cursor" : next_cursor,
            "limit" : limit
        }

"""
A few things to understand:
- Query(1, ge=1) means the page defaults to 1 and cannot be less than 1.
- Query(3, ge=1, le=100) means 3 records per page by default, with a maximum of 100.
- offset calculates how many records PostgreSQL should skip.
"""