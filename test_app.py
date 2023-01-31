import sys
sys.path.insert(1, './code')
from flask import Flask, request
import os
import logging
import pytest
import mongomock
from app import create_app, collection
from pymongo import MongoClient
from mongopass import mongopass
from bson import json_util
from bson.objectid import ObjectId
import json
from pytest_mongodb.plugin import mongo_engine
from unittest.mock import patch


@patch("pymongo.collection.Collection.find")
def find(mocker):
    mocker.return_value = [{"_id": {"$oid": ObjectId},
                                    "backOrder": True,
                                    "cost($)": 599.99,
                                    "expiration": 2034-10-23,
                                    "partName": "Air Conditioner",
                                    "partNumber": 369,
                                    "qty": 15,
                                    "weight(kg)": 40

    }]
    mocker.returncode= 200
    return mocker

@patch("pymongo.collection.Collection.find")
def find_error(mocker):
    mocker.return_value = [{"error": "Item not found."}]
    mocker.returncode = 404
    return mocker

@patch("pymongo.collection.Collection.update_one")
def update(mocker):
    mocker.return_value = [{"status": "Success"}]
    mocker.returncode = 200
    return mocker

@patch("pymongo.collection.Collection.delete_one")
def delete(mocker):
    mocker.return_value = [{"status": "Success"}]
    mocker.returncode = 200
    return mocker



# app = Flask(__name__)
# client = MongoClient(mongopass)
# db = client["crud"]
# collection = db["partsInv"]

logging.basicConfig(filename='test.log', level = logging.DEBUG)
# @pytest.fixture()
# def app(collection):
#     app = create_app(collection)
#     yield app

# @pytest.mark.parametrize("input, output", [
#     (("63d1ba084a818dee6aa6c40d"), (200, "Engine")),
#     (("63d30d52e2fcc04fa9bba09a"), (200, "Washer")),
#     (("1234"), (404, "error '1234' Item not found"))
# ])
# def test_get_part(input, output):
#     logging.info("Testing get" + input)
#     response = client.get('/part/' + input)
#     assert response.status_code == output[0]
#     match response.status_code:
#         case 200:
#             jsonData = json.loads(response.data.decode("UTF-8"))
#             assert jsonData['name'] == output[1]
#         case 404:
#             response_str = response.data.decode("UTF-8")
#             assert output[1] in response_str

# @pytest.fixture(autouse = True, scope='session')
# def test_db():
#     mongodb_fixture_dir = [
#         ('63d1ba084a818dee6aa6c40d', True, 2999.99, 2032-03-23, "Engine", 943, 13, 432),
#         ('63d30d52e2fcc04fa9bba09a', False, 399.99, 2033-04-16, "Washer", 369, 11, 70),
#     ]
# @pytest.fixture()
# def client(app):
#     return app.test_client()


# def test_flask_app(app):
#     logging.info("Testing Flask app")
#     response = app.get('/')
#     logging.info("Testing GET")
#     assert response.status_code == 200

# @pytest.mark.parametrize("input, output", [
#     ({"backOrder": True,
#         "cost($)": 599.99,
#         "expiration": 2034-10-23,
#         "partName": "Air Conditioner",
#         "partNumber": 369,
#         "qty": 15,
#         "weight(kg)": 40
#     })
# ])
# def test_data_insert(self, client, input, output):
#     assert input, output

#TESTING DB AND CONNECTION
# @mongomock.patch(servers=(('mongodb+srv://nikmikin:HGB2NTxp1LAtXn3a@crud.wplx2lz.mongodb.net/?retryWrites=true&w=majority')))
# def test_get_endpoint():
#     call_endpoint('/part')

#TESTING FILES

def test_file_exists():
    logging.info(os.path.exists('./test.log'))
    assert os.path.exists('./test.log')

def test_file_contents():
    with open('./test.log', 'r') as f:
        contents = f.read()
        assert "Testing log" in contents

def test_index():
    data = find()
    assert len(data.return_value) > 0
    assert data.returncode == 200

def test_index_error():
    data = find_error()
    assert data.return_value[0]["error"] == "Item not found."
    assert data.returncode == 404

def test_update():
    data = update()
    assert data.return_value[0]["status"] == "Success"
    assert data.returncode == 200

def test_delete():
    data = delete()
    assert data.return_value[0]["status"] == "Success"
    assert data.returncode == 200