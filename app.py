import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

collection = db.data
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"]
    count = collection.find_one(sort=[("num", -1)])
    if count:
        count=count["num"]
    else:
        count=0
    num = count + 1
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0
    }
    collection.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"]
    collection.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(collection.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

@app.route("/delete", methods=["POST"])
def bucket_delete():
    delete_receive = request.form['num_delete']
    collection.delete_one(
        {'num' : int(delete_receive)},
    )
    return jsonify({'msg' : 'Delete done!'})
    
if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)