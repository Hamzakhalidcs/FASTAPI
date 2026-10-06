"""
1. What an API endpoint actually is 
2. FastAPI Application
3. Get endpoints
4. Path Parameters
5. Query Parameters
6. JSON responses
7. Post Requests
8. Request Validation with pydantic
9. Error Handling 
10. Async Endpoints

To check the username of macos use uname -m and for product name and version sw_vers. 
A query parameter is additional information that we send to an API throug URL after ?
for example /products/101?category=soap

Json stand for Java Script Object Notation. It is a Standard format used for sending data 
between system, especially between a frontend and backend/API.

A Framework is a pre-built structure that provides a foundation for building software. 
it gives you a skeleton to fill in, rather than making you build every thing from scratch. 
"""

from fastapi import FastAPI

app = FastAPI()

@app.get('/home')
def about():
    return {
        "Name" : "Hamza Khalid",
        "Role" : "AI Engineer"
        }

@app.get('/profile')
def profile():
    return{
        "name" : "Hamza Khalid",
        "age" : 29, 
        "is_learning" : True,
        "Skills" : ["Python", "SQL", "POWERBI"]
    }

@app.get('/skill')
def skill():
    return {
        "Skills" :["Python", "SQL", "POWERBI"]
    }

@app.get('/experience')
def experience():
    return { 
        "Python" : "intermediate", 
        "SQL" : "Pro",
        "PowerBI" : "Beginner"
    }

@app.get('/users/{user_id}/orders/{order_id}')
def get_user(user_id:int, order_id:int):
    return {
        "user_id" : user_id,
        "order_id" : order_id
    }

@app.get('/products/{product_id}')
def product(product_id :int):
    return {
        "Product_ID" : product_id
    }

@app.get('/product_query/{product_id}')
# optional Query Parameter 
# Now path + query Parameters
def product(product_id : int,category:str, brand:str = "Any"):
    return{
        "ProductID" : product_id,
        "Category" : category,
        "Brand" : brand,
        "message" : f"Showing products from {category} category and Brand of {brand} and ProductID {product_id}"
    }
