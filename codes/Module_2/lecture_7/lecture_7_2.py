# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
r = requests.get(url=url)
print(r.text)
