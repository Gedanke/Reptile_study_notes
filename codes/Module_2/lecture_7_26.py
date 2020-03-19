# -*- coding: utf-8 -*-

import requests

proxies = {
    "https": "http://user:password@10.10.10.10:1080/",
}
url = "https://httpbin.org/get"
requests.get(url, proxies=proxies)
