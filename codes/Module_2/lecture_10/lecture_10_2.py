# -*- coding: utf-8 -*-

import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.test
collection = db.students

result = collection.find_one({"name": "LiHua"})
print(type(result))
print(result)

result = collection.find_one({'_id': ObjectId('5e7739b2b0de20fb9b5a3e6a')})
print(result)

results = collection.find({"age": 20})
print(results)
for result in results:
    print(result)

results = collection.find({"age": {"$gt": 20}})
print(list(results))

results = collection.find({"name": {"$regex": "^L.*"}})
print(list(results))
