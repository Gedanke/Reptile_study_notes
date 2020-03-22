# -*- coding: utf-8 -*-

import pymongo

client = pymongo.MongoClient(host="localhost", port=27017)
db = client.test
collection = db.students
count = collection.find().count()
print(count)

count = collection.estimated_document_count()
print(count)

count = collection.count_documents({"age": 20})
print(count)
