from flask import Flask, request
from uuid import uuid1
from bson import json_util
from pymongo import MongoClient
import os
from dotenv import load_dotenv

"""load environment variables from .env file"""
load_dotenv()
app = Flask(__name__)
"""Connect to MongoDB using URI from environment variable"""
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
collection = db['users']

"""Get all the users"""
@app.get('/getusers')
def get_users():
    users = list(collection.find({}))
    """Convert ObjectId to string for each user"""
    for user in users:
        user['_id'] = str(user['_id'])

    """return the json response"""
    return json_util.dumps(users), 200

"""test run"""
@app.route('/')
def start():
    return "Hello World"

"""Create a new user"""
@app.post('/user')
def insert_user():
    _id = str(uuid1().hex)
    content=dict(request.json)
    content.update({"_id":_id})
    
    """result = db['user'].insert_one(content)"""
    result = db.user.insert_one(content)
    if not result.inserted_id:
        return {"message":"Failed to insert"}, 500
    
    return {
        "message":"Success",
        "data":{
            "id":result.inserted_id
        }
    }, 200



"""Get user by _id <user_id>"""
@app.get('/users/<user_id>/')
def get_user(user_id):
    query = {
        "_id":user_id
    }
    user = db.user.find_one(query)
    if not user:
        return {
            "message": "User not found"
        }, 404
    
    return {
        "data":user
    }, 200

"""Delete a user"""
@app.delete('/users/<user_id>/')
def delete_user(user_id):
    query = {
        "_id":user_id
    }
    result = db.user.delete_one(query)
    if not result.deleted_count:
        return {
            "message":"Failed to delete"
        }, 500
    
    return {
        "message":"Deleted successfully"
    }, 200

"""Update a user"""
@app.put('/users/<user_id>/')
def update_user(user_id):
    query = {
        "_id": user_id
    }
    content = { "$set": dict(request.json) }
    result = db.user.update_one(query, content)

    if not result.matched_count:
        return {
            "message":"Failed to update. Record not found"
        }, 404
    elif not result.modified_count:
        return {
            "message":"No changes applied"
        }, 500
    
    return {
        "message": "Update successful"
    }, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)

"""debug parameter - is configuration option that:
1. Allows Automatic Reload - with debug mode enabled, Flask
will automatically restart the server whenever you make changes
to your Python code.
2. Enhanced Error Messages - provides more detailed error messages in the 
browser when an exception occurs
3. Debugger Pin - when debug mode is enabled, flask starts a debugger that you can attach to 
by visiting a specific URL."""