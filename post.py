from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import json 

app = FastAPI()

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

@app.post("/product_data")
def product(product_data : Product):
    product_data = product_data.model_dump()
    with open("product.json", "w") as file:
        json.dump(product_data, file, indent=4)

    return {
        "message" : "Product Save Successfully",
        "product" : product_data
    }
