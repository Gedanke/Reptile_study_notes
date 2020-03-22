# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.test
collection = db.students

results = collection.find().sort("name", pymongo.ASCENDING).skip(2)
print([result["name"] for result in results])

results = collection.find().sort("name", pymongo.ASCENDING).skip(2).limit(2)
print([result["name"] for result in results])

results = collection.find({"_id": {"$gt": ObjectId("5e772a2ef298962fd2b8bc75")}})
print(results)
print(list(results))
