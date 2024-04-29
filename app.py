from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# eestablish a connection to the MongoDB database
client = MongoClient(host='test_mongodb', port=27017, 
        username='root', password='pass', authSource="admin") 
db = client["test"]
collection = db["test_table"]

@app.route('/')
def get_records():
    all_records = collection.find()
    records = dumps(all_records)
    return records

@app.route('/insert', methods=['POST'])
def insert_record():
    new_record = {
        "user_id":111,
        "name": "yash",
    }
    result = collection.insert_one(new_record)
    return jsonify({"message": "New record inserted successfully!", "id": str(result.inserted_id)}), 201

@app.route('/delete/<user_id>', methods=['DELETE'])
def delete_record(user_id):
    query = {"user_id": int(user_id)}
    result = collection.delete_one(query)
    if result.deleted_count > 0:
        return jsonify({"message": f"Record with user_id {user_id} deleted successfully!"}), 200
    else:
        return jsonify({"message": f"No record found with user_id {user_id}"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000,host="0.0.0.0")

# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_geek():
#     return '<h1>Hello from Flask & Docker</h2>'


# if __name__ == "__main__":
#     app.run(debug=True)
