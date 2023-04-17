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

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_buckets")
def get_buckets():
    buckets = db.bucket.find()
    return jsonify([{"num": b["num"], "name": b["name"], "description": b["description"]} for b in buckets])

@app.route("/add_bucket", methods=["POST"])
def add_bucket():
    name = request.form["name"]
    description = request.form["description"]
    num = db.bucket.count_documents({})
    db.bucket.insert_one({"num": num + 1, "name": name, "description": description})
    return "success"

@app.route("/delete", methods=["POST"])
def delete_bucket():
    num = int(request.form["num"])
    db.bucket.delete_one({"num": num})
    return "success"

if __name__ == "__main__":
    # Inisialisasi database
    db.bucket.drop()  # Menghapus seluruh data dari collection "bucket" jika ada
    data = [
        {"num": 1, "name": "Belajar Python", "description": "Belajar Python untuk pemula"},
        {"num": 2, "name": "Membuat website", "description": "Mempelajari cara membuat website dengan HTML, CSS, dan JavaScript"},
        {"num": 3, "name": "Latihan olahraga", "description": "Melakukan latihan fisik secara teratur"}
    ]
    db.bucketlist.insert_many(data)  # Menambahkan data awal ke dalam collection "bucket"

    app.run(debug=True)

