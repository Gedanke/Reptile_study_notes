# -*- coding: utf-8 -*-

import requests

r = requests.get("http://httpbin.org/get", timeout=1)
print(r.status_code)
