# -*- coding: utf-8 -*-

import requests

url = "https://github.com/favicon.ico"
r = requests.get(url)
print(r.text)
print(r.content)
