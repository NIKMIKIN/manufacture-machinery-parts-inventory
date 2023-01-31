from flask import Flask, request
from pymongo import MongoClient
from mongopass import mongopass
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)

client = MongoClient(mongopass)
db = client["crud"]
collection = db["partsInv"]

# class Part:
#     def __init__(self, _id, backOrder, cost, expiration, partName, partNumber, qty, weight):
#         self._id = _id
#         self.backOrder = backOrder
#         self.cost = cost
#         self.expiration = expiration
#         self.partName = partName
#         self.partNumber = partNumber
#         self.qty = qty
#         self.weight = weight

# part = Part
def create_app(collection):

    @app.route("/")
    def index():
        data = []

        for d in collection.find():
            data.append(d)

        return json.dumps(data, indent=4, default=json_util.default), 200

    @app.route("/part/<part_id>")
    def get_part(part_id):
        part = collection.find_one({"_id": ObjectId(part_id)})
        if part:
            return json_util.dumps(part), 200
        else:
            return json_util.dumps({"error": "Item not found."}), 404

    @app.route("/part", methods=["POST"])
    def create_part():
        # pulls request of JSON from front-end or Postman
        part = request.get_json()
        # inserts item into Mongo DB Collection
        result = collection.insert_one(part)
        # returns _id of newly inserted item
        return json_util.dumps({"_id": str(result.inserted_id)})

    @app.route("/part/<part_id>", methods=["PUT"])
    def update_part(part_id):
        part = request.get_json()
        result = collection.update_one(
            {"_id": ObjectId(part_id)}, {"$set": part})
        if result.matched_count > 0:
            return json_util.dumps({"status": "success"})
        else:
            return json_util.dumps({"error": "Item not found"}), 404

    @app.route("/part/<part_id>", methods=["DELETE"])
    def delete_part(part_id):
        result = collection.delete_one({"_id": ObjectId(part_id)})
        if result.deleted_count > 0:
            return json_util.dumps({"status": "success"})
        else:
            return json_util.dumps({"error": "Item not found"}), 404
    
    return app

app = create_app(collection)
            
if __name__ == '__main__':
    app.run(debug=True)
