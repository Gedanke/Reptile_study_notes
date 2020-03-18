# -*- coding: utf-8 -*-

import requests

url = "https://www.baidu.com/"
r = requests.get(url=url)

print(r.cookies)
for key, value in r.cookies.items():
    print(key + "=" + value)
