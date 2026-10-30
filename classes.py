from pydantic import BaseModel, Field
import psycopg

def get_connection():
    return psycopg.connect(
        dbname= "sql_practice",
        user="macbook_user",
        host="/tmp"
    )


class Product(BaseModel):
    product: str = Field(min_length=1)
    price: int = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    product: str
    price: int


class ProductsResponse(BaseModel):
    Products: list[ProductResponse]

class ProductCreateResponse(BaseModel):
    message: str
    Product: ProductResponse

class ProductDeleteResponse(BaseModel):
    message: str
    product: ProductResponse

