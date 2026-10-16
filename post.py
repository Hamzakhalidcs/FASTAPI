from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json 
from pathlib import Path
from sqlalchemy import create_engine,  text



app = FastAPI()

database_url = "sqlite:///./products.db"
engine = create_engine(
    database_url, 
    connect_args= {"check_same_thread": False}
)

class Product(BaseModel):
    name :str
    price : float
    Category : str = "General"
    description: Optional[str] = None #Optional[str] means the value can be either a string or None.  

@app.post("/products")
def create_product(product:Product):
    return{
        "message": "Product Created",
        # "Product" : product
        "name" : product.name,
        "Price" : product.price,
        "Categroy" : product.Category,
        "Description" : product.description
    }

# @app.post("/product_data")
# def product(product_data : Product):
#     product_data = product_data.model_dump()
#     with open("product.json", "w") as file:
#         json.dump(product_data, file, indent=4)

#     return {
#         "message" : "Product Save Successfully",
#         "product" : product_data
#     }


file_path  = Path("product.json")

@app.post("/product_data_in_file")
def create_product(product: Product):
    product_data = product.model_dump()

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as file:
            products = json.load(file)
    else:
        # If the file does not exist, start with an empty list
        products = []

    products.append(product_data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)

    return {
        "message": "Product saved successfully",
        "product": product_data,
        "total_products": len(products)
    }

@app.get('/check_database')
def check_dabase():
    with engine.connect() as connection:
        result = connection.execute(text("Select 1"))
        value = result.scalar()

    return{
        "message" : "Database Connected Successfully",
        "result":value
    }