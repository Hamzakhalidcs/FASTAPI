from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import json 
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float,text
from sqlalchemy.orm import declarative_base, sessionmaker, Session




app = FastAPI()

# DATABASE_URL = "sqlite:///./test.db"
DATABASE_URL = "sqlite:////Users/macbook_user/test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 2. Database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 3. Base class for database tables
Base = declarative_base()


# 4. Products table definition
class ProductTable(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)


# 5. Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# 6. Request data validation
class Product(BaseModel):
    name: str
    price: float


# 7. Database session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# class Product(BaseModel):
#     name :str
#     price : float
#     Category : str = "General"
#     description: Optional[str] = None #Optional[str] means the value can be either a string or None.  

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

@app.get("/products_database")
def get_products(db:Session = Depends(get_db)):
    db = SessionLocal()
    
    products = db.query(ProductTable).all()
    return [
        {
            "id" : product.id,
            "name" : product.name,
            "price" : product.price
        }
        for product in products
    ]
    
print("Database URL:", engine.url)
print("Database file:", engine.url.database)

@app.post("/products_database_post")
def create_product(
    product: Product,
    db: Session = Depends(get_db)
):
    new_product = ProductTable(
        name=product.name,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "name": new_product.name,
        "price": new_product.price
    }