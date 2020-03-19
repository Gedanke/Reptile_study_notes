# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
r = requests.get(url=url)
print(type(r.text))
print(r.json())
print(type(r.json()))
