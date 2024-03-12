from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URL'))
db = client.get_database()
#print(db)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie = request.form['movie']
        overview = request.form['overview']
        db['movies'].insert_one({'movie':movie, 'overview': overview})
        return redirect(url_for('index'))
    movies = db['movies'].find({})
    return render_template('index.html', movies=movies)
    

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

@app.post('/delete/<movie_id>/')
def delete(movie_id):
    query = {
       "_id":ObjectId(movie_id)
    }
    result = db['movies'].delete_one(query)
    if not result.deleted_count:
        return {"message":"Failed to delete movie"}, 500
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
