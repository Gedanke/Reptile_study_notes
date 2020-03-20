# -*- coding: utf-8 -*-

import requests

url = "https://github.com/favicon.ico"
r = requests.get(url)
with open("favicon.ico", "wb") as f:
    f.write(r.content)
