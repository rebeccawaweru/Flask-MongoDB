from flask import Flask
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_database()

@app.route('/', methods=['GET'])
def hello():
    return 'Welcome to Flask + MongoDB'


@app.get('/users')
def getUsers():
    users = list(db['users'].find({}))
    if not users:
        return {"message":"Failed to get users"}, 500

    for user in users:
        user['_id'] = str(user['_id'])

    return {
        "data":users
    }, 200


if __name__ == "__main__":
    app.run(debug=True)
