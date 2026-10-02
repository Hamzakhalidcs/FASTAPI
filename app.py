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

Remove snippet
"""

from fastapi import FastAPI

app = FastAPI()

@app.get('/home')
def about():
    return {
        "Name" : "Hamza Khalid",
        "Role" : "AI Engineer"
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