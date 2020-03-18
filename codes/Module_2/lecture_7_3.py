# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
data = {
    "name": "germey",
    "age": 25
}
r = requests.get(url=url, params=data)
print(r.text)
