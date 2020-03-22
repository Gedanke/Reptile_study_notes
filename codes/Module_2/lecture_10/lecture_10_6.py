# -*- coding: utf-8 -*-

import pymongo

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.test
collection = db.students

condition = {"name": "ZhangWei"}
student = collection.find_one(condition)
student["age"] = 25
result = collection.update(condition, student)
print(result)

result = collection.update(condition, {"$set": student})
print(result)

condition = {"name": "ZhangWei"}
student = collection.find_one(condition)
student["age"] = 26
result = collection.update_one(condition, {"$set": student})
print(result)
print(result.matched_count, result.modified_count)
