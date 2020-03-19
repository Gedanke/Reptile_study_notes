# -*- coding: utf-8 -*-

import requests

proxies = {
    "http": "socks5://user:password@host:port",
    "https": "socks5://user:password@host:port",
}
url = "https://httpbin.org/get"
requests.get(url, proxies=proxies)
