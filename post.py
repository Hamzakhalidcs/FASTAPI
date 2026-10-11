from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

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
