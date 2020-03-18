# -*- coding: utf-8 -*-

import requests

data = {
    "name": "germey",
    "age": "25"
}
url = "http://httpbin.org/post"
r = requests.post(url=url, data=data)
print(r.text)
