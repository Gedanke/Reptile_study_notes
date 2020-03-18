# -*- coding: utf-8 -*-

import requests

url = "http://httpbin.org/get"
proxies = {
    "http": "http://10.10.10.10.1080",
    "https": "http://10.10.10.10.1080"

}
r = requests.get(url=url, proxies=proxies)
print(r)
