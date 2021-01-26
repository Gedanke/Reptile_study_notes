# -*- coding: utf-8 -*-

import requests

url = "https://static1.scrape.cuiqingcai.com/"
r = requests.get(url=url, verify=False)

print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)
